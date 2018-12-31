# Yu-Gi-Oh Card Scanner

## Usage

Repo uses Pipenv to manage dependencies, see their instructions for setting up a virtual env on an existing project.

`manual.py`: Basic version for while I can't get Tesseract working like I want. Loop for user input of the card number & display info about it & save it to a CSV. Can be used either by inputting card numbers one at a time or by passing a file of numbers.

Eventually this process should be automatic, using Tesseract to pull the text from card pictures rather than human input.

![Usage of the manual script](assets/yugioh-manual-scanner.png?raw=true "Example")


`ocr`: Variety of scripts in the process of trying to get Object Character Recognition working.  We've gotten close many times, but haven't reached the consistency necessary to use it over a human.  Currently using an old webcam mounted over the card, but it's possible the next step is to find a way to get higher quality photos rather than trying to process low quality ones to work.


## Tesseract Usage

Use the included Makefile to handle building the image, running a shell, or other useful tasks.

To change the device passed to our Docker container, change the videoDevice env variable `videoDevice=/dev/video0 make run-shell`.

## Camera Setup

Card number is the most important part, and though small more consistent than the card name. Card number is always black text on a variety of background colors whereas the name can be white as well.

Build your apparatus for scanning with the card area delineated and mounted webcam. To preprocess the image,
we use our image capture tool to crop just the name of card. Finding the correct points to crop can be frustrating,
unless you use a tool like Gwenview, Edit->Crop->Advanced Settings and it shows you coordinates and size needed to match
what you'd want to crop the image down to.

With the cropped image, it should be able to easily pass it along to Tesseract for processing.

## TCGplayer Client

Since it doesn't exist in a decent state from our initial searches, I started a basic version of a Python client library. This is a good opportunity to see more of how Python works under the hood.

Inspiration repos:

-   https://github.com/slackapi/python-slackclient
-   https://github.com/mattlisiv/newsapi-python
-   https://github.com/PokemonTCG/pokemon-tcg-sdk-python

## https://yugiohprices.docs.apiary.io/ Client

These prices seemed to be wildly different & much more unlikely than what was coming from TCG, so development of this ended rather quickly.