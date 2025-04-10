import os
import sys
from PIL import Image

def convert_png_to_webp(root_dir):
    converted_count = 0
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith(".png"):
                png_path = os.path.join(dirpath, filename)
                webp_path = os.path.splitext(png_path)[0] + ".webp"
                try:
                    with Image.open(png_path) as img:
                        img.save(webp_path, "WEBP")
                    print(f"Converted: {png_path} -> {webp_path}")
                    converted_count += 1
                except Exception as e:
                    print(f"Error converting {png_path}: {e}")
    return converted_count

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert_png_to_webp.py <directory>")
        sys.exit(1)
    
    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print(f"Directory '{directory}' not found.")
        sys.exit(1)
    
    total_converted = convert_png_to_webp(directory)
    print(f"Conversion completed. Total PNG files converted: {total_converted}")
