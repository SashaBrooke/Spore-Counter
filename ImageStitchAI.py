import stitching
from matplotlib import pyplot as plt
import colorama
from colorama import Fore
import cv2 as cv
import sys
from PIL import Image
import time

def log(message):
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print(current_time + " [ LOG: " + message + " ]")

log("Performing grid stitch")

images = [Image.open(x) for x in [r"C:\Users\Sasha\Documents\Uni\Extension_Programming\ResearchSat\ImageStitch\PICT1.jpg", 
r"C:\Users\Sasha\Documents\Uni\Extension_Programming\ResearchSat\ImageStitch\PICT3.jpg"]]
widths, heights = zip(*(i.size for i in images))

total_width = sum(widths)
max_height = max(heights)

new_im = Image.new('RGB', (total_width, max_height))

x_offset = 0
for im in images:
    new_im.paste(im, (x_offset,0))
    x_offset += im.size[0]

new_im.save(r"C:\Users\Sasha\Documents\Uni\Extension_Programming\ResearchSat\ImageStitch\StitchedFiles\test.jpg")

log("Grid stitch success")