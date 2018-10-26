import pygame.camera as pc
import pygame.image as pi
import argparse
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import sys
import os
import pytesseract


def preprocess_image(file_path, processed_fp):
    im =  Image.open(file_path)
    im = im.convert("L")
    # set anything closer to white to full black, closer to black to full white
    im = im.point(lambda x: 255 if x<128 else 0, "1")
    im.save(processed_fp)

# resources
# https://www.learnopencv.com/deep-learning-based-text-recognition-ocr-using-tesseract-and-opencv/
# https://www.pyimagesearch.com/2018/09/17/opencv-ocr-and-text-recognition-with-tesseract/
# https://stackoverflow.com/questions/37745519/use-pytesseract-to-recognize-text-from-image#37750605  
def main():
    parser = argparse.ArgumentParser(description="Time to D-D-D-Duel.")
    parser.add_argument("saveDir", help="Directory to save photos to.")
    parser.add_argument("--prefix", default="ygh-photo", help="File prefix for each numbered photo.")
    parser.add_argument("--psm", type=int, default=6, help="psm argument for tesseract tool.")
    args = parser.parse_args()

    prefix = args.prefix
    save_dir = args.saveDir
    psm = args.psm

    if not os.path.exists(save_dir):
        os.mkdir("./%s" % save_dir)

    # setup camera
    try:
        pc.init()
        webcam = pc.Camera(pc.list_cameras()[0])
        webcam.start()
    except Exception as e:
        print("Error encountered when setting up webcam, check it's not already in use.")
        print(e)
        raise SystemExit
    
    i = webcam.get_image()
    pi.save(i, "./photo.png")
    # let user select when to take each photo, number them consecutively.
    count = 0
    while True:
        input()
        img = webcam.get_image()
        file_path =  "%s/%s%d.png" % (save_dir,prefix,count)
        pi.save(img, file_path)
        print("---> Processing image %s" % file_path)
        try:
            processed_fp =  "%s/processed-%s%d.png" % (save_dir,prefix,count)
            preprocess_image(file_path, processed_fp)
            # Define config parameters.
            # '-l eng'  for using the English language
            # '--oem 1' for using LSTM OCR Engine
            # psm 6 = words as a text line?
            config = ("-l eng --oem 1 --psm %d" % psm)
            text = pytesseract.image_to_string(Image.open(file_path), config=config)
            print("-----text found-------")
            print(text)
            print("----------------------")
        except UnicodeEncodeError:
            print("[!] had an issue encoding to Unicode.")
        count += 1

    pc.quit()


if __name__ == "__main__":
    main()