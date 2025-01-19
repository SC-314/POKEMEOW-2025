import random
from PIL import Image, ImageDraw, ImageFilter, ImageGrab
import numpy as np
import matplotlib.pyplot as plt
import os
import shutil

def brighten_white_with_tint(tint, tint_strength=0.5):
    '''
    Affects the tint of the different colours
    '''
    original_color = (255, 255, 255)  # Always white
    tinted_color = [
        int(original_color[i] * (1 - tint_strength) + tint[i] * tint_strength)
        for i in range(3)
    ]
    final_color = [min(max(0, value), 255) for value in tinted_color]
    return tuple(final_color)

def color_non_transparent_parts(image, color):
    '''
    Function name
    '''
    color_image = Image.new("RGBA", image.size, color + (255,))
    colored_image = Image.composite(color_image, image, image)
    return colored_image

def make_captcha_other():
    '''
    Create the artificial captcha
    '''

    numbers = []
    for j in ['Bold', 'Italic']:
        for i in range(10):
            numbers.append(Image.open(f'./venv/DONT_ACCESS/Number images/{j}/{i}.png'))

    total_numbers = random.randint(3,6)


    # global colours
    canvas_size = (random.randint(100,200), random.randint(100,200))
    canvas_colour = (random.randint(81, 177), random.randint(76, 177), random.randint(96, 188))
    draw_colour = brighten_white_with_tint((random.randint(81, 177), random.randint(76, 177), random.randint(96, 188)), tint_strength=0.4)
    canvas = Image.new("RGB", canvas_size, canvas_colour)
    positions = []
    solution =[]
    sols = []

    for i in range(total_numbers): # paste a random coloured number at a random position
        random_number = random.randint(0,19)
        sols.append(random_number % 10)
        solution.append([random_number % 10])
        img = numbers[random_number]
        coloured_img = color_non_transparent_parts(img, draw_colour)
        x = int(i * canvas.size[0]/total_numbers) + random.randint(0, int(canvas.size[0]/total_numbers-img.size[0]))
        y = random.randint(0, canvas.size[1]-coloured_img.size[1])
        solution[i].append((2*x+img.size[0])/2)
        solution[i].append((2*y+img.size[1])/2)
        solution[i].append(img.size[0])
        solution[i].append(img.size[1])
        canvas.paste(coloured_img, (x, y), coloured_img)

    line_factor = 5
    canvas_line_size = tuple(line_factor * np.array(canvas_size))
    canvas_line = Image.new("RGBA", canvas_line_size)

    draw = ImageDraw.Draw(canvas_line)

    for _ in range(7): # draw random lines on a new canvas
        width = random.randint(2,3)
        line_start = (random.randint(0, canvas_line.size[0]), random.randint(0, canvas_line.size[1]))
        line_end = (random.randint(0, canvas_line.size[0]), random.randint(0, canvas_line.size[1]))
        draw.line([line_start, line_end], fill=draw_colour, width=width*line_factor)

    for _ in range(3): # draw the coloured lines
        width = random.randint(2,4)
        line_start = (canvas_line.size[0]+1000, random.randint(0, canvas_line.size[1]))
        line_end = (random.randint(0, canvas_line.size[0]), random.randint(0, canvas_line.size[1]))
        colour = (np.random.randint(57,237), np.random.randint(60,238), np.random.randint(26,245)) # colours[random.randint(0, len(colours)-1)]
        draw.line([line_start, line_end], fill=colour, width=3*line_factor)

    canvas_line = canvas_line.resize(canvas_size) # resize the newly made canvas to the size of the original one
    canvas.paste(canvas_line, canvas_line)

    return canvas, solution

captcha = make_captcha_other()

image_name = ""

for sol_data in captcha[1]:
     print(sol_data)
     image_name += str(sol_data[0])

image_path = f"./venv/.YOU_CAN_CHANGE/gennerated_imgs/{image_name}.png"
img = captcha[0]

img.save(image_path)

print(image_path)