import os
from PIL import Image
import io

# Optional: Background remover if rembg is installed
try:
    from rembg import remove
    REMBG_AVAILABLE = True
except ImportError:
    REMBG_AVAILABLE = False
    print("Warning: rembg not installed. Background removal will be skipped.")


# Remove background from all letter images
def preprocess_letters_with_rembg(folder):
    if not REMBG_AVAILABLE:
        print("Skipping background removal; rembg not installed.")
        return

    for file in os.listdir(folder):
        if file.lower().endswith((".jpg", ".jpeg", ".png")):
            input_path = os.path.join(folder, file)
            with open(input_path, 'rb') as i:
                input_data = i.read()
            output_data = remove(input_data)
            output_img = Image.open(io.BytesIO(output_data)).convert("RGBA")
            newname = os.path.splitext(file)[0] + ".png"
            output_img.save(os.path.join(folder, newname))
            print(f"Processed and saved {newname}")


# Function to write handwriting to a unique new image file
def write_handwriting(
    text,
    folder='handwriting_letters',
    output_folder='generated_handwriting',
    max_width=3508,
    max_height=2480,
    space_between_words=50,
    line_height=120
):
    os.makedirs(output_folder, exist_ok=True)

    # Create a new unique filename each time
    index = len(os.listdir(output_folder)) + 1
    output_img = os.path.join(output_folder, f"output_handwriting_{index}.jpg")

    canvas = Image.new("RGB", (max_width, max_height), (255, 255, 255))
    y_offset = 50  # Top margin

    lines = text.strip().split('\n')
    for line in lines:
        x_offset = 50  # Left margin
        i = 0
        while i < len(line):
            char = line[i]
            if char == ' ':
                x_offset += space_between_words
                i += 1
                continue
            img_path = os.path.join(folder, f"{char}.png")
            if os.path.exists(img_path):
                img = Image.open(img_path)
            else:
                img = Image.new("RGBA", (30, line_height), (255, 255, 255, 0))

            canvas.paste(img, (x_offset, y_offset + (line_height - img.height)), img)
            x_offset += img.width
            i += 1
        y_offset += line_height

    canvas.save(output_img, "JPEG")
    print(f"✅ Handwriting image saved as {output_img}")


# Folder containing letter PNGs
letters_folder = "handwriting_letters"

# Example usage — creates a new file each time text is changed
write_handwriting(
    "THIS PROJECT IS MADE BY AVI",
    folder=letters_folder
)
