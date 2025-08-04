from PIL import Image

def png_to_ico(png_path, ico_path, size=(256, 256)):
    img = Image.open(png_path)
    img.save(ico_path, format='ICO', sizes=[size])
    print(f"Converted '{png_path}' to '{ico_path}' with size {size}")

# Example usage:
png_to_ico('codeforces.png', 'codeforces.ico', size=(32, 32))