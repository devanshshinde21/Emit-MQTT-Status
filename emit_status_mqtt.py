import paho.mqtt.client as mqtt
from pymongo import MongoClient
from threading import Thread, Event
import datetime
import random
import pika
import json
import time


# RabbitMQ credentials
RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5672
RABBITMQ_QUEUE = 'mqtt_queue'
RABBITMQ_USER = 'guest'
RABBITMQ_PASSWORD = 'guest'

# MQTT broker credentials
MQTT_BROKER = 'localhost'
MQTT_PORT = 1883
MQTT_TOPIC = 'test/topic'

# MongoDB Connection
mongo_client = MongoClient(host='localhost', port=27017, username='root', password='mongodb', authMechanism='SCRAM-SHA-256')

mongodb_name = mongo_client['mqtt_status']
collection_name = 'mqtt_status_info'
keep_alive_time = 10


def on_connect(client, userdata, flags, rc):
    """
    This function works for call back the
    :param client: MQTT Client instance
    :param userdata: User defined additional data which is provided when creating client instance
    :param flags: It is a repsone flag which sent by the broker
    :param rc: It is a connection result code. Indicated success/failure status.
    :return:
    """
    print(f"Connected to MQTT broker with result code {rc}")
    client.subscribe(MQTT_TOPIC)


def receive_message(client=None, userdata=None, msg=None):
    """
    Generally this function works for handel the MQTT receiving messages and forward it to RabbitMQ.
    :param client: MQTT client instance
    :param userdata: User-defined data
    :param msg: Containing MQTT message
    :return:
    """
    print(f"Received message from MQTT topic {msg.topic}: {msg.payload.decode()}")
    # Connect to RabbitMQ and publish the message
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
    channel.basic_publish(exchange='', routing_key=RABBITMQ_QUEUE, body=msg.payload.decode())
    print(f"Message published to RabbitMQ queue {RABBITMQ_QUEUE}")
    connection.close()

    message = json.loads(msg.payload.decode())
    unique_id = message.get('unique_id')
    end_time = datetime.datetime.now().strftime("%H:%M:%S")
    if unique_id:
        exist = mongodb_name[collection_name].find_one({"_id": unique_id})
        if exist:
            mongodb_name[collection_name].update_one(exist, {"$set": {"end_time": end_time}})


def mqtt_publish(stop_event):
    """
    Basically this function work for publish messages to MQTT topic at regular time interval.
    And stor the status value and starting time and ending time on mongo DB collection.
    :return:
    """
    mqtt_client = mqtt.Client()
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, keep_alive_time)
    count = 0
    while True:
        if count == keep_alive_time:
            break
        status_value = random.randint(0, 6)
        start_time = datetime.datetime.now().strftime("%H:%M:%S")
        unique_id = f"record_id:{datetime.datetime.now().strftime("%d%m%Y%H%M%S")}"

        message = {
            'unique_id': unique_id,
            'status': status_value
        }
        mongodb_name[collection_name].insert_one({'_id': unique_id, "start_time": start_time, "status": status_value})

        mqtt_client.publish(MQTT_TOPIC, json.dumps(message))

        print(f"Published message to MQTT topic {MQTT_TOPIC}: {message}")
        time.sleep(1)
        count += 1



def start_processing_mqtt_messages():
    """
    This is a main function which start functionality to sent MQTT messages to broker.
    """
    stop_event = Event()

    # Initialize the MQTT client for receiving messages
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = receive_message

    # Start the MQTT client loop in a separate thread
    mqtt_thread = Thread(target=lambda: mqtt_client.connect(MQTT_BROKER, MQTT_PORT, keep_alive_time) or mqtt_client.loop_forever())
    mqtt_thread.start()

    # Start publishing messages to the MQTT broker
    mqtt_publish_thread = Thread(target=mqtt_publish, args=(stop_event,))
    mqtt_publish_thread.start()

    # # Wait for both threads to complete
    mqtt_thread.join()
    mqtt_publish_thread.join()


start_processing_mqtt_messages()