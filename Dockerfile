from ubuntu:18.04

RUN apt-get update && apt install -y python3-minimal python3-pip tesseract-ocr libtesseract-dev \
    && pip3 install pytesseract pygame Pillow

RUN apt-get install -y fswebcam