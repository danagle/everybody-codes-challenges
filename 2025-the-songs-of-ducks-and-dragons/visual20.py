from pathlib import Path
from PIL import Image

# color palette (RGB)
PALETTE = {
    'T': (255, 255, 255),  # white
    '#': (128, 128, 128),  # gray
    '.': (0, 0, 0),        # black
}

def _get_bounds_from_dense(grid):
    """Return height, width for a dense grid (list of rows)."""
    h = len(grid)
    w = max(len(row) for row in grid) if h else 0
    return h, w

def _get_bounds_from_sparse(grid_dict):
    """Return (min_r, min_c, max_r, max_c) for a sparse dict-grid."""
    rows = [r for r, _ in grid_dict.keys()]
    cols = [c for _, c in grid_dict.keys()]
    if not rows:
        return 0, 0, -1, -1
    return min(rows), min(cols), max(rows), max(cols)

def create_bitmap_from_dense(grid, out_path="grid.png", scale=10, palette=PALETTE, bg='.') -> None:
    """
    Create a PNG from a dense grid (list of strings or list of lists).
    - grid: sequence of rows (strings or lists). rows may be different lengths.
    - out_path: output PNG filename.
    - scale: pixel size of one cell (integer >= 1).
    """
    h, w = _get_bounds_from_dense(grid)
    if h == 0 or w == 0:
        raise ValueError("Empty grid")

    img = Image.new("RGB", (w * scale, h * scale), palette.get(bg, (0,0,0)))
    pixels = img.load()

    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            color = palette.get(ch, palette.get(bg, (0,0,0)))
            if scale == 1:
                pixels[c, r] = color
            else:
                x0, y0 = c * scale, r * scale
                for y in range(y0, y0 + scale):
                    for x in range(x0, x0 + scale):
                        pixels[x, y] = color

    img.save(out_path)

def create_bitmap_from_sparse(grid_dict, out_path="grid_sparse.png", scale=10, palette=PALETTE, bg='.') -> None:
    """
    Create a PNG from a sparse grid represented as a dict {(r,c): ch}.
    - grid_dict: mapping from (row, col) -> character
    - out_path: output PNG filename
    - scale: pixel size of one cell
    """
    min_r, min_c, max_r, max_c = _get_bounds_from_sparse(grid_dict)
    if min_r > max_r:
        raise ValueError("Empty grid_dict")

    h = max_r - min_r + 1
    w = max_c - min_c + 1

    img = Image.new("RGB", (w * scale, h * scale), palette.get(bg, (0,0,0)))
    pixels = img.load()

    for (r, c), ch in grid_dict.items():
        rr = r - min_r
        cc = c - min_c
        color = palette.get(ch, palette.get(bg, (0,0,0)))
        if scale == 1:
            pixels[cc, rr] = color
        else:
            x0, y0 = cc * scale, rr * scale
            for y in range(y0, y0 + scale):
                for x in range(x0, x0 + scale):
                    pixels[x, y] = color

    img.save(out_path)


def load_triangular_grid(filepath: str):
    """Read the 2-D triangular grid from the input text file."""
    grid_dict = {}
    lines = Path(filepath).read_text(encoding="utf-8").strip().splitlines()

    for r, row in enumerate(lines):
        for c, cell in enumerate(row.strip('.')):
            grid_dict[r, c] = cell

    return grid_dict


def part2(filepath: str = "../input/everybody_codes_e2025_q20_p2.txt"):
    grid = Path(filepath).read_text(encoding="utf-8").strip().replace('E', 'T').replace('S', 'T').splitlines()
    create_bitmap_from_dense(grid, out_path="e2025_q20_p2.png", scale=3)

part2()
