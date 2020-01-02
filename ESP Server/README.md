# Deploy Models in ESP

The aim of this project is to deploy Deep Neural Network Model and serve it using API.

## Setup Environment

1. Install SAS ESP

2. Setup python and install this application using the following script

  ```
  sudo mkdir /app
  sudo chown $USER /app
  cd /app
  git clone https://github.com/sukmmi/espdeploy.git
  bash espdeploy/install.sh
  . ~/.bashrc
  conda activate iotdemo
  ```
3. Update image size as required by Model in server.py

  ```
  resize = esp.calculate.ImageProcessing(schema=('id*:int64', '_image_:blob'), function="resize", width=224, height=224)
  ```

4. (Optional - only if you are using new model)Schema for model in repository is already created. Create new Schema file for new model using the following tool.

  ```
  bash espdeploy/util/read_astore_schema.sh espdeploy/astore/new_model.astore > new_schema.txt
  ```

## Deploy and Start ESP

  ```
  cd espdeploy
  bash deploy.sh -a 30003 -p 30004 -m astore/resnet50_caffe.astore -s astore/schema.txt -d
  ```


## Score
 ```
 cd espdeploy/score
 python score_img_classification.py -i img.jpg
 ```
