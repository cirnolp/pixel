"""
README:

Anwendung (standalone):
- Python installieren
- einen Ordner erstellen und das Script dort als Textdatei speichern, die Textdatei benennen in place.py
- cmd in dem Pfad öffnen
- pip install Pillow schreiben
- das Bild in den gleichen Ordner packen, und so skalieren, dass ein Pixel etwa 100x100 Pixel groß ist.
- die place.py Datei öffnen und die Pixelgröße in WIDTH_OF_PIXEL und HEIGHT_OF_PIXEL anpassen
- die Links oberste Koordinate raussuchen und entsprechend in TOP_LEFT_X und TOP_LEFT_Y eingeben
- den Dateinamen des Bildes ersetzen (INPUT_FILE)
(- optional: den Dateinamen der Output-Datei ersetzen (OUTPUT_FILE))
- das Script mit python place.py in cmd ausführen
"""
from argparse import ArgumentParser, Namespace

parser = ArgumentParser(description='Creates a Pixelgrid with Coordinates based on user input')
parser.add_argument('inputfile', type=str, help='Source File')
parser.add_argument('xCoord', type=int, help='X Coordinate of top left pixel')
parser.add_argument('yCoord', type=int, help='Y Coordinate of top left pixel')
parser.add_argument('--width', type=int, help='Width of single Pixel on Image', default='100')
parser.add_argument('--height', type=int, help='Height of single Pixel on Image', default='100')
parser.add_argument('-o', '--outputfile', type=str, help='Define Output file name')

args: Namespace = parser.parse_args()
WIDTH_OF_PIXEL = args.width
HEIGHT_OF_PIXEL = args.height
TOP_LEFT_X = args.xCoord
TOP_LEFT_Y = args.yCoord
OFFSET_LEFT = 0
OFFSET_TOP = 0
INPUT_FILE = args.inputfile 
OUTPUT_FILE = "output.png" if not args.outputfile else args.outputfile
IGNORE_COLORS = []

from PIL import Image
from PIL import ImageFont, ImageDraw

im = Image.open(INPUT_FILE)
width, height = im.size

draw = ImageDraw.Draw(im)
font = ImageFont.truetype("RobotoMono.ttf", 24)

num = 0

for i in range(OFFSET_LEFT, width, WIDTH_OF_PIXEL):
    for j in range(OFFSET_TOP, height, HEIGHT_OF_PIXEL):
        pixelColor = im.getpixel((i + WIDTH_OF_PIXEL//2, j + HEIGHT_OF_PIXEL//2))
        if pixelColor not in IGNORE_COLORS:
            num += 1
            draw.line(((i, j), (i + WIDTH_OF_PIXEL, j)), fill="black", width=1)
            draw.line(((i, j), (i, j + HEIGHT_OF_PIXEL)), fill="black", width=1)
            textColor = (46, 204, 113)
            if pixelColor[0] < 0x80 and pixelColor[1] > 0xb0 and pixelColor[2] < 0x80:
                textColor = (255, 255, 255)
            draw.text((i+3, j+3), f"Nr.{num}\nx{TOP_LEFT_X + (i//WIDTH_OF_PIXEL)}\ny{(TOP_LEFT_Y + j//HEIGHT_OF_PIXEL)}", font=font, fill=textColor)

im.save(OUTPUT_FILE)