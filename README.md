# Yu-Gi-Oh Card Scanner

## Usage

To change the device passed to our Docker container, change the videoDevice env variable `videoDevice=/dev/video0 make run-shell`.

## Tesseract Usage

Use the included Makefile to handle building the image, running a shell, or other useful tasks.

## Camera Setup

In current state, can only handle the card name. The card number is too small and hard to pickup for
either webcam we are currently using, so we will have to come up with an enhancement to make this work.

Build your apparatus for scanning with the card area delineated and mounted webcam. To preprocess the image,
we use our image capture tool to crop just the name of card. Finding the correct points to crop can be frustrating,
unless you use a tool like Gwenview, Edit->Crop->Advanced Settings and it shows you coordinates and size needed to match
what you'd want to crop the image down to.

With the cropped image, we should be able to easily pass it along to Tesseract for processing.

## TCGplayer Client

Since it doesn't exist in a decent state from our initial searches, we shall start a basic version of a Python client library. This is a good opportunity to see more of how Python works under the hood.

Inspiration repos:

-   https://github.com/slackapi/python-slackclient
-   https://github.com/mattlisiv/newsapi-python
-   https://github.com/PokemonTCG/pokemon-tcg-sdk-python
