"""Generates a random twitter profile based upon a 5/7/5 random bit shift (inversion to add colour)"""
from PIL import Image
import random
HEIGHT, WIDTH = 400, 400
NAME = "haikubot.png"

def set_pixel(shift):
    '''shifts it to 5 or 7 bits - Haikus, HA! 
    and inverts it to keep it from being too dark'''
    return ~(random.randint(0,256) >> shift) & 0xFF

def create_image():
    return Image.new('RGB', (HEIGHT,WIDTH), color='black')

def save_image(image):
    image.save(NAME)

def process_image(image):
    for pixel in range(HEIGHT * WIDTH):
        x = int(pixel / WIDTH)
        y = pixel % WIDTH
        shift = 1 if pixel % 3 == 2 else 3
        image.putpixel((x,y), (set_pixel(shift), set_pixel(shift), set_pixel(shift)))
    return image

if __name__ == "__main__":    
    image = create_image()
    process_image(image)
    save_image(image)