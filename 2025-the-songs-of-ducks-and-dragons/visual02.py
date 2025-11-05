"""
Visual generated from Quest 2 Part 3.
"""
import itertools
import numpy as np
from pathlib import Path
from PIL import Image
import re
import tqdm


def read_data(filepath="../input/everybody_codes_e2025_q02_p3.txt"):
    text = Path(filepath).read_text().strip()
    return list(map(int, re.findall(r"-?\d+", text)))

    
def add(a, b):
    x1, y1 = a
    x2, y2 = b
    return [x1 + x2, y1 + y2]


def multiply(a, b):
    x1, y1 = a
    x2, y2 = b
    return [x1*x2-y1*y2, x1*y2+y1*x2]


def divide(a, b):
    x1, y1 = a
    x2, y2 = b
    return [int(x1 / x2), int(y1 / y2)]


def create_image(left_x, top_y):
    # Set background and foreground colours
    background = np.array([0, 0, 0])
    engraved = np.array([255, 0, 255])

    bitmap = [[background for _ in range(1_001)] 
              for _ in range(1_001)]

    for x_delta, y_delta in tqdm.tqdm(list(itertools.product(range(1_001), range(1_001)))):
        A = [left_x + x_delta, top_y + y_delta]
        result = [0, 0]
        is_engraved = True
        for _ in range(100):
            result = multiply(result, result)
            result = divide(result, [100_000, 100_000])
            result = add(result, A)
            if any(abs(num)>1_000_000 for num in result):
                is_engraved = False
                break
        if is_engraved:
            bitmap[x_delta][y_delta] = engraved

    image = Image.fromarray(np.array(bitmap).astype(np.uint8), "RGB")
    image.save("e2025_q02_output.png")


if __name__ == "__main__":
    top_left = read_data()
    create_image(*top_left)
