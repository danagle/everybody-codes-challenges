from PIL import Image

def grid_to_image(path, scale=20):
    # Read the grid
    grid = [
        [int(ch) for ch in line.strip()]
        for line in open(path)
        if line.strip()
    ]

    h, w = len(grid), len(grid[0])

    # Create image (8-bit grayscale)
    img = Image.new("L", (w, h))
    for r in range(h):
        for c in range(w):
            # Scale digit (0–9) to full grayscale (0–255)
            val = grid[r][c] * 28  # 9*28 ≈ 252
            img.putpixel((c, r), val)

    # Optional upscale for visibility
    if scale != 1:
        img = img.resize((w*scale, h*scale), Image.NEAREST)

    return img


# Example usage:
img = grid_to_image("../input/everybody_codes_e2025_q12_p3.txt", scale=2)
img.show()
img.save("e2025_q12_p3.png")
