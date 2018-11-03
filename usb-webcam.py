# a script to handle using the usb webcam  we have because
# pygame sucks and doesn't support it
import subprocess

def main():
    device = "/dev/video1"
    crop_values = "GGGxGGG,GGxGG"
    # check the --crop option of fswebcam, possibly also swap channels
    # jpg giving better output and actually functioning with options, png failing
    # PLAN: !!!!!! first iteration, use camera to just get the name because that will be enough work on it's own..
    # can take pic, use fswebcam to crop
    # also has some options we can check with inverting/greyscale, but that might not be as helpful because
    # we deal with white and black text equally
    command1 = "fswebcam -d %s -r 640x480 --crop %s --no-banner --save photos.png" %(device,crop_values)
    output1 = subprocess.check_output(command1, encoding="UTF-8", shell=True)
    print(output1)


if __name__ == "__main__":
    main()