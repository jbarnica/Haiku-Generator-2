"""Generates a random twitter profile based upon a 5/7/5 random bit shift (inversion to add colour)"""
from PIL import Image
import random
HEIGHT, WIDTH = 400, 400
WIDTH = 400

def setPixel(shift):
    return ~(random.randint(0,256) >> shift) & 0xFF

image = Image.new('RGB', (HEIGHT,WIDTH), color='black')

for pixel in range(HEIGHT * WIDTH):
    x = int(pixel / WIDTH)
    y = pixel % WIDTH
    r = random.randint(0,256)
    g = random.randint(0,256)
    b = random.randint(0,256)
    if pixel % 3 == 2:
        r = setPixel(1)
        g = setPixel(1)
        b = setPixel(1)
    else:
        r = setPixel(3)
        g = setPixel(3)
        b = setPixel(3)        
    image.putpixel((x,y), (r,g,b))   
image.save("haikubot.png")