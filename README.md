# Emit-MQTT-Status

# MQTT to RabbitMQ and MongoDB Integration

This project demonstrates the integration of MQTT, RabbitMQ, and MongoDB. The first script handles the MQTT client setup, message publishing, and message forwarding to RabbitMQ. The second script sets up a FastAPI server to fetch and display status count of stored data in MongoDB based on two parameter, Ex:- start_time and end_time.

## Prerequisites

- Python 3.8+
- RabbitMQ
- MongoDB
- Required Python packages: `paho-mqtt`, `pymongo`, `pika`, `fastapi`, `uvicorn`, `pandas`,`mosquitto`, `Mongo DB Compass`

## Installation

1. Clone the repository:

   ```bash
   git clone git@github.com:devanshshinde21/Emit-MQTT-Status.git
   cd Emit-MQTT-Status
   
2. Install the required Python packages using below command

   pip install -r requirements.txt

3. Setup for mosquitto using below command
   - sudo apt update
   -  sudo apt install mosquitto mosquitto-clients
   -  sudo systemctl enable mosquitto
   -  sudo systemctl start mosquitto

4. By default, Mosquitto works out of the box, So you may want to configure it for specific needs
   - Configuration file you may found at this path "/etc/mosquitto/mosquitto.conf"
   - then Open the conf file and add below mentioned two lines at the end of the file
         listener 1883
         allow_anonymous true
   - Then use keys to ctrl+X then it will ask to save the buffer, Then Press Y.
   - Now the confgis is set in the file.
     
5. After making changes to the configuration file, restart Mosquitto using below commands
   sudo systemctl restart mosquitto
 
## NOW YOU CAN RUN THE BELOW SCRIPTS
## MQTT to RabbitMQ and MongoDB Script
- About emit_status_mqtt.py file   
  This script helps to connects with MQTT broker, publishes messages to a specified topic, and forwards received messages to RabbitMQ.
  Additionally, it stores message statuses and timestamps for unique id in MongoDB.
- This script is run directly.
   
## Fast API Script
- About fetch_status_count_rest_api.py script
  This script sets up a FastAPI server that provides an endpoint to fetch data from MongoDB based on start and end times.
- Using below command you can start the Fast API server
- uvicorn fecth_status_count_rest_api:app --reload
   
