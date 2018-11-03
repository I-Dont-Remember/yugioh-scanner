# module to handle choosing which webcam we are able to use and gather images for it
# raise a ValueError if anything goes wrong
import subprocess
import pygame.camera as pc
import pygame.image as pi
from PIL import Image


def process_image(camera, path):
    crop_size = camera.crop_size
    crop_start = camera.crop_start
    image = Image.open(path)
    # only need crop if we used pygame, cuz fsweb handles it for us
    if camera.is_laptop_cam:
        image.crop(a, b, c, d)
    image.save(path)


def take_pygame_image(camera, dest_path):
    i = camera.get_image()
    pi.save(i, dest_path)


def take_fsweb_image(device, crop_size, crop_start, dest_path):
    command = "fswebcam"
    options = " -d %s -r 640x480" % device
    if crop_size:
        options += " --crop %s,%s" % (crop_size, crop_start)
    options += "--save %s" % dest_path
    output = subprocess.check_output(
        command + options, encoding="UTF-8", shell=True)


class Webcam(object):

    def __init__(self, is_laptop_cam, device, crop_start, crop_size):
        self.crop_start = crop_start
        self.crop_size = crop_size
        self.device = device
        self.is_laptop_cam = is_laptop_cam
        if is_laptop_cam:
            # use pygame
            try:
                pc.init()
                # TODO: check device exists
                self.camera = pc.Camera(device)
                self.camera.start()
            except Exception as e:
                raise ValueError("Unable to setup pygame %s" % e)

    def get_image(self, dest_path):
        # TODO: check dest path
        try:
            if self.is_laptop_cam:
                take_pygame_image(self.camera, dest_path)
            else:
                take_fsweb_image(self.device, self.crop_size,
                                 self.crop_start, dest_path)
            return dest_path
        except Exception as e:
            raise ValueError("Unable to take/or save photo %s" % e)

    def get_cropped_image(self, dest_path):
         # TODO: check dest path
        try:
            self.get_image(dest_path)
            process_image(self.camera, dest_path)
            return dest_path
        except Exception as e:
            raise ValueError("Unable to take/or save cropped photo %s" % e)
