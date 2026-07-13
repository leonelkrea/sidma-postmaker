from PIL import Image, ImageDraw, ImageFont
import os

output_dir = "/Volumes/ARC Reactor/Code Projects SSD/SIDMA/content_manager/public"
width, height = 819, 1024

def create_placeholder(prefix, slide_num, total):
    img = Image.new('RGB', (width, height), color = (20, 30, 48))
    d = ImageDraw.Draw(img)
    text = f"{prefix}\nSlide {slide_num} / {total}\n[IMAGE PLACEHOLDER]"
    
    # Try to use a decent font, fallback to default
    try:
        font = ImageFont.truetype("Arial", 40)
    except IOError:
        font = ImageFont.load_default()
        
    text_bbox = d.textbbox((0, 0), text, font=font)
    text_w = text_bbox[2] - text_bbox[0]
    text_h = text_bbox[3] - text_bbox[1]
    
    d.text(((width-text_w)/2, (height-text_h)/2), text, font=font, fill=(100, 255, 218), align="center")
    
    img.save(os.path.join(output_dir, f"{prefix}_slide_{slide_num}.png"))

# A25 (7 slides)
for i in range(1, 8):
    create_placeholder("A25", i, 7)

# A27 (6 slides)
for i in range(1, 7):
    create_placeholder("A27", i, 6)

print("Placeholders generated.")
