
# example topic: ws52134/cam002/motion/snapshot

import paho.mqtt.client as mqtt
from darkflow.net.build import TFNet
import os
import cv2
import tensorflow as tf
import numpy as np
import datetime
from PIL import Image
from io import BytesIO

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print( "Connected with result code "+str(rc) )
    topic = os.getenv('MQTT_TOPIC')

    if topic is not None:
        client.subscribe(topic)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print( "on_message: " + str(msg.topic) )

    try:
        payload = BytesIO(msg.payload)
        snapshot = Image.open(payload)
        image = cv2.cvtColor(np.array(snapshot), cv2.COLOR_RGB2BGR)
    
        starttime = datetime.datetime.now()
        result = tfnet.return_predict(image)
        endtime = datetime.datetime.now()
        
        # publish full result
        client.publish( msg.topic + "/detection", str(result) )
        
        # publish detailed result - e.g. one mqtt message per detected object type
        labels = list(set([entry["label"] for entry in result]))

        for l in labels:
            l_topic = msg.topic + "/detection/" + l
            l_result = [ entry for entry in result if entry["label"] == l ]
            client.publish( l_topic, str(l_result) )
            
    except:
        print("Unexpected error:", str(sys.exc_info()[0]))

user = os.getenv('MQTT_USERNAME')
pwd  = os.getenv('MQTT_PASSWORD')
host = os.getenv('MQTT_HOST') or '127.0.0.1'
port = os.getenv('MQTT_PORT') or 1883

options = {"model": "/darkflow/cfg/yolo.cfg", "load": "/yolo.weights",  "threshold": 0.3}
tfnet = TFNet(options)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

if (user is not None) and (pwd is not None):
    client.username_pw_set(user, pwd)
client.connect(host,  port, 60)

client.loop_forever()
