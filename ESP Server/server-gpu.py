import os
import re
import sys
import time
import json
import errno
import socket
import signal
import logging
import argparse
import modelingApi
from subprocess import Popen
#from setproctitle import *
from multiprocessing import Process, Value, log_to_stderr
import csv
import esppy
from esppy.plotting import StreamingImages

def start_project():

    astore_file=args.model
    schema_file=args.schema

    def createYoloLabelString(file):
        regex = re.compile(r'^ *(.*?): *(.*?) *(\(.*?\))?$')
        astore_map = {}
        current_map='' #input_map: or output_map:
        with open(file, newline = '') as source:
            reader = csv.reader(source, delimiter='\t')
            for row in reader:
                if row[0] == 'input-map:':
                    astore_map[row[0]]=['id*:int64']
                    current_map=row[0]
                elif row[0] == 'output-map:':
                    astore_map[row[0]]=['id*:int64','_image_:blob']
                    #astore_map[row[0]].append('_image_:blob')
                    current_map=row[0]
                else:
                    line=regex.findall(row[0])
                    if line:
                        if len(line[0]) == 3:
                            astore_map[current_map].append(line[0][0].replace(" ", "")+":"+line[0][1].replace(" ", ""))
        return astore_map['output-map:']

    #host = os.environ['ESPHOST']
    #port = os.environ['ESPPORT']
    #host = 'espserver.esp19w25.local'
    #port = 30001

    # connect to the esp server
    try:
        esp = esppy.ESP('127.0.0.1', args.httpport)
    except Exception as e:
        print("Can't connect to ESP server: ")
        print(e)

    logger.info(esp.server_info)

    #creating an empty project
    logger.info("### Creating Project ###")
    detectionProject = esp.create_project('detectionProject')


    #adding source window
    src = esp.SourceWindow(schema=('id*:int64', 'image:blob'),
                              index_type='empty', insert_only=True)
    detectionProject.windows['w_data'] = src


    #adding resize window
    resize = esp.calculate.ImageProcessing(schema=('id*:int64', '_image_:blob'), function="resize", width=416, height=416)
    resize.set_inputs( imageInput='image:blob')
    resize.set_outputs( imageOutput='_image_:blob')
    detectionProject.windows['resized'] = resize


    #define a request window to inject the astore model to the reader window
    model_request = esp.SourceWindow(schema=('req_id*:int64', 'req_key:string', 'req_val:string'),
                                    index_type='empty', insert_only=True)
    detectionProject.windows['w_request'] = model_request


    #define a model reader window
    model_reader = esp.ModelReaderWindow()
    detectionProject.windows['w_reader'] = model_reader

    labelList = createYoloLabelString(schema_file)
    #logger.info(labelList)
    scorer = esp.ScoreWindow()
    scorer.schema = labelList
    scorer.add_offline_model(model_type='astore')
    detectionProject.windows['w_score'] = scorer

    #connecting the windows
    src.add_target( resize, role='data')
    resize.add_target( scorer, role='data')
    model_request.add_target( model_reader, role='request')
    model_reader.add_target( scorer, role='model')

    logger.info("### Loading Project ###")
    #load the project
    esp.load_project(detectionProject)
    #print(detectionProject.to_xml(pretty=True))


    logger.info("### Loading Model ###")
    #send the load model signal
    logger.info("Loading " + astore_file)
    pub = model_request.create_publisher(blocksize=1, rate=0, pause=0,
                                   dateformat='%Y%m%dT%H:%M:%S.%f', opcode='insert', format='csv')

    pub.send('i,n,1,"action","load"\n')
    pub.send('i,n,2,"type","astore"\n')
    pub.send('i,n,3,"reference","' + astore_file + '"\n')
    pub.send('i,n,4,usegpuesp,1\n')
    pub.send('i,n,5,NDEVICES,1\n')
    pub.send('i,n,6,DEVICE0,0\n')
    pub.send('i,n,7,,\n')
    pub.close()

    logger.info("### Project Started ###")

# Wait for the ESP server to start
def wait_for_esp(pid):
    while not esp_port_in_use(True):
        time.sleep(2)
        try:
            os.getpgid(pid)
        except:
            logger.error('ESP failed to start')
            sys.exit(1)


# Check if the ESP ports are in use
def esp_port_in_use(log):
    ready = True
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', args.pubsub))
    if result == 0:
        sock.close()
    else:
        if log:
            logger.debug('ESP server not listening')
        ready = False
    return ready

# If any child process dies then terminate the others
def wait_for_shutdown():
    while True:
        try:
            pid, status = os.wait()
            logger.warn(pids[pid] + ' stopped with status ' + str(status) + ', stopping other processes...')
            sys.exit(1)
        except OSError as err:
            if err.errno != errno.EINTR:
                raise


# Stop all child processes
def stop_child_processes():
    for pid, name in pids.items():
        try:
            logger.warn('Terminating ' + name + ': ' + str(pid))
            os.kill(pid, signal.SIGTERM)
        except OSError:
            logger.debug('Failed to terminate: ' + pids[pid])

if __name__ == '__main__':
    # Read command line options
    argparser = argparse.ArgumentParser(description='Object Detection')
    argparser.add_argument('-m', dest='model', help='model (ASTORE) file', required=True)
    argparser.add_argument('-s', dest='schema', help='model schema file', required=True)
    argparser.add_argument('-p', dest='pubsub', help='ESP pubsub port number', type=int, required=True)
    argparser.add_argument('-a', dest='httpport', help='ESP http port number', type=int, required=False)
    argparser.add_argument('-d', dest='debug', help='enable debug', action="store_true")

    args = argparser.parse_args()

    # Enable debug
    logger = log_to_stderr()
    esp_log_level = 'fatal'
    if args.debug:
        logger.setLevel(logging.DEBUG)
        logging.getLogger(modelingApi.getLoggingHandler()).setLevel(logging.DEBUG)
        esp_log_level = 'trace'
    else:
        logger.setLevel(logging.WARN)
        logging.getLogger(modelingApi.getLoggingHandler()).setLevel(logging.FATAL)

    espOptions = ''
    if args.httpport > 0:
        espOptions = ' -http ' + str(args.httpport)


    # To avoid connecting to an already running ESP server check the ports are not in use
    if esp_port_in_use(False):
        logger.error('Unable to start ESP - port in use')
        sys.exit(1)

    # Dictionary of child process IDs
    pids = {}
    signal.signal(signal.SIGTERM, lambda signum, frame: sys.exit(0))

    try:
        pid = Popen(['bash', '-c', 'exec ${DFESP_HOME}/bin/dfesp_xml_server -loglevel esp=' + esp_log_level + espOptions + ' -pubsub ' + str(args.pubsub)]).pid
        pids[pid] = 'ESP Server'
        wait_for_esp(pid)
        start_project()

        wait_for_shutdown()

    # Clean up any child processes before exit
    except KeyboardInterrupt:
        stop_child_processes()
        sys.exit(0)
    except SystemExit:
        stop_child_processes()
        raise
