from PIL import Image, ImageDraw
import sys
import os

def extend_post(input_path, output_path=None):
    if output_path is None:
        output_path = input_path

    img = Image.open(input_path)

    # Resize to 1080x1080
    img_resized = img.resize((1080, 1080), Image.Resampling.LANCZOS)

    # Canvas 1080x1350 with brand background
    bg_color = (22, 6, 45)
    canvas = Image.new('RGB', (1080, 1350), bg_color)

    # Paste image centered vertically
    canvas.paste(img_resized, (0, 135))

    # Blend top edge
    top_row = [img_resized.getpixel((x, 0)) for x in range(1080)]
    for y in range(135):
        factor = y / 135.0
        for x in range(1080):
            r = int(bg_color[0] * (1 - factor) + top_row[x][0] * factor)
            g = int(bg_color[1] * (1 - factor) + top_row[x][1] * factor)
            b = int(bg_color[2] * (1 - factor) + top_row[x][2] * factor)
            canvas.putpixel((x, y), (r, g, b))

    # Blend bottom edge
    bottom_row = [img_resized.getpixel((x, 1079)) for x in range(1080)]
    for y in range(1215, 1350):
        factor = 1.0 - (y - 1215) / 135.0
        for x in range(1080):
            r = int(bg_color[0] * (1 - factor) + bottom_row[x][0] * factor)
            g = int(bg_color[1] * (1 - factor) + bottom_row[x][1] * factor)
            b = int(bg_color[2] * (1 - factor) + bottom_row[x][2] * factor)
            canvas.putpixel((x, y), (r, g, b))

    canvas.save(output_path, 'PNG')
    print(f"Extended and saved: {output_path} (1080x1350)")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python extend_image.py <input.png> [output.png]")
        sys.exit(1)
    inp = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else inp
    extend_post(inp, out)
