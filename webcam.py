# module to handle choosing which webcam we are able to use and gather images for it
# raise a ValueError if anything goes wrong
import subprocess
import pygame.camera as pc
import pygame.image as pi
from PIL import Image


def process_image(camera, path):
    print("[*] processing image")
#     im = Image.open(path)
#     im = im.convert("L")
#     # set anything closer to black to full black, closer to white to full white
#     # im = im.point(lambda x: 0 if x < 128 else 255, "1")
#     # try to set it to black if it's closer and leave alone if not
#     im = im.point(lambda x: 0 if x < 128 else x, "1")
# #     # only need crop if we used pygame, cuz fsweb handles it for us
#     # if camera.is_laptop_cam:
#     #     crop_size = camera.crop_size
#     #     crop_start = camera.crop_start
#     #     image.crop(a, b, c, d)
#     im.save(path)


def take_pygame_image(camera, dest_path):
    i = camera.get_image()
    pi.save(i, dest_path)


def take_fsweb_image(device, crop_size, crop_start, file_path):
    print("Taking fswebcam image")
    command = "fswebcam"
    options = " -d %s --no-banner -r 640x480 --greyscale" % device
    if crop_size:
    # example
    #   --crop 320x240    Crops the center 320x240 area of the image.
    #   --crop 10x10,0x0  Crops the 10x10 area at the top left corner of the image.
        options += " --crop %s,%s" % (crop_size, crop_start)
    options += " --save %s" % file_path
    print("Running command: %s" % (command + options))
    output = subprocess.check_output(
        command + options, encoding="UTF-8", shell=True)
    # fswebcam doesn't use any error codes, so test if file was created
    subprocess.check_call(["test", "-e", file_path])


class Camera(object):

    def __init__(self, is_laptop_cam, device, crop_start, crop_size):
        self.crop_start = crop_start
        self.crop_size = crop_size
        self.device = device
        self.is_laptop_cam = is_laptop_cam
        if is_laptop_cam:
            # use pygame
            try:
                pc.init()
                self.camera = pc.Camera(device)
                self.camera.start()
            except Exception as e:
                raise ValueError("Unable to setup pygame %s" % e)

    def take_photo(self, file_path):
        try:
            if self.is_laptop_cam:
                take_pygame_image(self.camera, file_path)
            else:
                take_fsweb_image(self.device, self.crop_size,
                                 self.crop_start, file_path)
            process_image(self, file_path)
        except Exception as e:
            raise ValueError("Unable to take/or save photo %s" % e)
