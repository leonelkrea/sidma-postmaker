from PIL import Image, ImageDraw

def extend_post():
    # Load the generated image
    img = Image.open('sidma_tech_post.png')
    
    # 1. Resize the 1024x1024 image to 1080x1080
    img_resized = img.resize((1080, 1080), Image.Resampling.LANCZOS)
    
    # 2. Create a new canvas of 1080x1350 with the background color
    # Let's use the average top/bottom color: RGB (22, 6, 45) -> Hex #16062d
    bg_color = (22, 6, 45)
    canvas = Image.new('RGB', (1080, 1350), bg_color)
    
    # 3. Paste the resized image in the center (y = 135)
    canvas.paste(img_resized, (0, 135))
    
    # 4. Smoothly blend the top boundary (y = 135) and bottom boundary (y = 1215)
    # We will copy the top row of the image (y=135) and fade it upwards
    # We will copy the bottom row of the image (y=1214) and fade it downwards
    draw = ImageDraw.Draw(canvas)
    
    # Blend top
    top_row = [img_resized.getpixel((x, 0)) for x in range(1080)]
    for y in range(135):
        # Calculate interpolation factor (0.0 at y=0, 1.0 at y=135)
        factor = y / 135.0
        for x in range(1080):
            r = int(bg_color[0] * (1 - factor) + top_row[x][0] * factor)
            g = int(bg_color[1] * (1 - factor) + top_row[x][1] * factor)
            b = int(bg_color[2] * (1 - factor) + top_row[x][2] * factor)
            canvas.putpixel((x, y), (r, g, b))
            
    # Blend bottom
    bottom_row = [img_resized.getpixel((x, 1079)) for x in range(1080)]
    for y in range(1215, 1350):
        # Calculate interpolation factor (1.0 at y=1215, 0.0 at y=1349)
        factor = 1.0 - (y - 1215) / 135.0
        for x in range(1080):
            r = int(bg_color[0] * (1 - factor) + bottom_row[x][0] * factor)
            g = int(bg_color[1] * (1 - factor) + bottom_row[x][1] * factor)
            b = int(bg_color[2] * (1 - factor) + bottom_row[x][2] * factor)
            canvas.putpixel((x, y), (r, g, b))
            
    # Save the extended image
    canvas.save('sidma_tech_post.png', 'PNG')
    print("Post extended and saved successfully as 1080x1350!")

if __name__ == '__main__':
    extend_post()
