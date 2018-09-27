FROM tensorflow/tensorflow:1.5.0

RUN apt-get update && apt-get install -y \
    python-pip \
    cython \
    git \
    libsm6 \
    libxext6 \
    libxrender-dev \
    wget

RUN cd "/" && \
    wget -nv "https://pjreddie.com/media/files/yolo.weights"

RUN pip install --upgrade pip
RUN pip install opencv-python paho-mqtt

RUN cd "/" && \
    git clone https://github.com/thtrieu/darkflow.git &&\
    cd darkflow && \
    pip install . 

# From https://github.com/thtrieu/darkflow/issues/168
RUN cd "/" && \
    cd darkflow && \
    python setup.py build_ext --inplace

ADD yolo_mqtt_server.py /darkflow
WORKDIR /darkflow
CMD ["python", "/darkflow/yolo_mqtt_server.py"]
