import os
import re
import sys
import time
import argparse
import csv
def createYoloLabelString(file):
        regex = re.compile(r'^ *(.*?): *(.*?) *(\(.*?\))?$')
        astore_map = {}
        current_map='' #input_map: or output_map:
        with open(file, newline = '') as source:
            reader = csv.reader(source, delimiter='\t')
            for row in reader:
                #print(row)
                if row[0] == 'input-map:':
                    astore_map[row[0]]=['id*:int64']
                    current_map=row[0]
                elif row[0] == 'output-map:':
                    astore_map[row[0]]=['id*:int64','_image_:blob']
                    #astore_map[row[0]].append('_image_:blob')
                    current_map=row[0]
                else:
                    #print(row[0])
                    line=regex.findall(row[0])
                    if line:
                        if len(line[0]) == 3:
                            astore_map[current_map].append(line[0][0].replace(" ", "")+":"+line[0][1].replace(" ", ""))
        return astore_map['output-map:']


if __name__ == '__main__':
    # Read command line options
    argparser = argparse.ArgumentParser(description='Schema Reader')
    argparser.add_argument('-s', dest='schema', help='model schema file', required=True)

    args = argparser.parse_args()

    out=createYoloLabelString(args.schema)
    print(out)
