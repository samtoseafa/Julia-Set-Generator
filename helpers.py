import itertools
import matplotlib as plt
from collections import defaultdict
from PIL import Image, ImageDraw
from math import log, log2, floor, ceil


def generate_julia(c, z0):
    global max_iterations
    max_iterations = 80
    z, n = z0, 0
    while abs(z) <= 2 and n < max_iterations:
        z = z**2 + c
        n += 1
    return max_iterations if n == max_iterations else n + 1 - log(log2(abs(z)))


def linear_interpolation(color_1, color_2, t):
    return color_1 * (1 - t) + color_2 * t


def generate_julia_images():
    histogram, values = defaultdict(lambda: 0), {}
    width, height = 400, 400
    saturation = 255
    real_start, real_end = -1, 1
    imaginary_start, imaginary_end = -1.2, 1.2
    complex_values = [
        complex(0.285, 0.01),
        complex(-0.7269, 0.1889),
        complex(-0.8, 0.156),
        complex(-0.4, 0.6),
    ]
    for j, c in enumerate(complex_values):
        for x, y in itertools.product(range(width), range(height)):
            # convert pixel coordinates to complex coordinates
            z0 = complex(
                real_start + (x / width) * (real_end - real_start),
                imaginary_start + (y / height) * (imaginary_end - imaginary_start),
            )
            # determine the number of iterations
            iterations = generate_julia(c, z0)
            values[(x, y)] = iterations
            if iterations < max_iterations:
                histogram[floor(iterations)] += 1
        total = sum(histogram.values())
        hues, h = [], 0

        for i in range(max_iterations):
            h += histogram[i] / total
            hues.append(h)
        hues.append(h)

        image = Image.new("HSV", (width, height), (0, 0, 0))
        draw = ImageDraw.Draw(image)

        for x, y in itertools.product(range(width), range(height)):
            iterations = values[(x, y)]
            # determine the color of the points
            hue = 255 - int(
                255
                * linear_interpolation(
                    hues[floor(iterations)], hues[ceil(iterations)], iterations % 1
                )
            )
            value = 255 if iterations < max_iterations else 0
            draw.point([x, y], (hue, saturation, value))
        image.convert("RGB").save(f"julia_variation{j + 1}.png", "PNG")

