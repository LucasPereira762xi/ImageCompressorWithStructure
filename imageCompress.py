import os
from PIL import Image

def compress_image(file_path, output_path, max_size_kb):
    with Image.open(file_path) as img:
        img_format = img.format
        img.thumbnail((img.width, img.height))
        quality = 85
        while True:
            with open("temp_image.jpg", "wb") as temp_file:
                img.save(temp_file, format=img_format, quality=quality)
            if os.path.getsize("temp_image.jpg") <= max_size_kb * 999:
                break
            quality -= 5
            if quality < 5:
                break
        img.save(output_path, format=img_format, quality=quality)

def process_directory(root_dir, target_dir, max_size_kb):
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(subdir, file)
            relative_path = os.path.relpath(subdir, root_dir)
            output_subdir = os.path.join(target_dir, relative_path)
            os.makedirs(output_subdir, exist_ok=True)
            output_path = os.path.join(output_subdir, file)
            try:
                compress_image(file_path, output_path, max_size_kb)
                print(f"Compressed: {file_path} -> {output_path}")
            except Exception as e:
                print(f"Could not compress {file_path}: {e}")

root_directory = "catalog"
target_directory = "compressed-catalog"
max_size_kb = 1024  # 1 MB

process_directory(root_directory, target_directory, max_size_kb)
