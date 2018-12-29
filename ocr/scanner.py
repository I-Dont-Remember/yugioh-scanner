import webcam
import argparse
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import sys
import os
import pytesseract


# resources
# https://www.learnopencv.com/deep-learning-based-text-recognition-ocr-using-tesseract-and-opencv/
# https://www.pyimagesearch.com/2018/09/17/opencv-ocr-and-text-recognition-with-tesseract/
# https://stackoverflow.com/questions/37745519/use-pytesseract-to-recognize-text-from-image#37750605

def ocr(file_path, psm):
    print("OCR on %s" % file_path)
    try:
        # Define config parameters.
        # '-l eng'  for using the English language
        # '--oem 1' for using LSTM OCR Engine
        # psm 6 = words as a text line?
        config = ("-l eng --oem 1 --psm %d" % psm)
        text = pytesseract.image_to_string(
            Image.open(file_path), config=config)
        print("-----text found-------")
        print(text)
        print("----------------------")
    except UnicodeEncodeError:
        print("[!] had an issue encoding to Unicode.")

def main():
    parser = argparse.ArgumentParser(description="Time to D-D-D-Duel.")
    parser.add_argument("saveDir", help="Directory to save photos to.")
    parser.add_argument("--prefix", default="ygh-photo",
                        help="File prefix for each numbered photo.")
    parser.add_argument("--psm", type=int, default=6,
                        help="psm argument for tesseract tool.")
    args = parser.parse_args()

    prefix = args.prefix
    save_dir = args.saveDir
    psm = args.psm

    if not os.path.exists(save_dir):
        os.mkdir("./%s" % save_dir)

    # Crop Example
    #   --crop 320x240    Crops the center 320x240 area of the image.
    #   --crop 10x10,0x0  Crops the 10x10 area at the top left corner of the image.
    camera = webcam.Camera(False, "/dev/video1", "299x300", "150x50")
    # let user select when to take each photo, number them consecutively.
    count = 0
    print("[*] if an image was decoded incorrectly, input 't' to try again...")
    while True:
        file_path = "%s/%s-%d.jpg" % (save_dir, prefix, count) 
        try:
            camera.take_photo(file_path)
        except ValueError as e:
            print(e)
            continue

        ocr(file_path, psm)
        i = input()
        if i == "t":
            print("[*] trying again for #%d" % count)
        else:
            count += 1


if __name__ == "__main__":
    main()
