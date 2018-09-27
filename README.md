# MQTT interface to Yolo for e.g. Xiaomi Dafang camera hacks

Some clever people have found ways to hack Xiaomi Fang / Dafang cameras. After the hack they implement motion detection and send snapshots of a scene via MQTT. See here for further information:

https://github.com/EliasKotlyar/Xiaomi-Dafang-Hacks

After studying object detection based on Yolo I thought about integrating this with one of my Dafang cameras. When the camera detects motion, it pushes a jpeg to an MQTT topic like

  home/cam001/motion/snapshot

. The app in this repository subscribes to such topics (you can specify an MQTT topic including wildcards), runs the Yolo network and publishes detect objects on additional topics:

  home/cam001/motion/snapshot/detection         --> payload contains information on all detected objects
  home/cam001/motion/snapshot/detection/person  --> payload contains information on detected persons in the image
  home/cam001/motion/snapshot/detection/bike    --> payload contains information on detected bikes in the image

This would enable a smart home solution such as home assistant to subscribe to specific topics and e.g. send notifications whenever a person is detected.


# How to build

I use docker. To build a container, please clone this repository, cd into the directory and run

  docker build -t yolo-mqtt-server .

This should build the container which you can then run like this:

  docker run -v -t -e MQTT_HOST='192.168.1.2' -e MQTT_USERNAME='ha' -e MQTT_PASSWORD='secret' -e MQTT_TOPIC='home/+/motion/snapshot' yolo-mqtt-server

The first three environment settings (host, user, password) should be self explanatory. The MQTT_TOPIC setting controls to which topic the app subscribes to. You can use wildcards to subscribe to multiple cameras. 
