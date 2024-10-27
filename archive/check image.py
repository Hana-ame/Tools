import os
from PIL import Image

def check_images(directory):
    incomplete_images = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                file_path = os.path.join(root, file)
                try:
                    with Image.open(file_path) as img:
                        a = img.load()  # Verify that it is, in fact, an image
                        print(a)
                except (IOError, SyntaxError) as e:
                    print(f"Image {file_path} is incomplete or corrupted.")
                    incomplete_images.append(file_path)
    return incomplete_images

def check_image(fn):
    try:
        with Image.open(fn) as img:
          # img.verify()
          a = img.load()  # Verify that it is, in fact, an image
          # print(a)
    except (IOError, SyntaxError) as e:
        print(f"Image {fn} is incomplete or corrupted.")
        # incomplete_images.append(fn)

if __name__ == "__main__":
    check_image('yes.jpg')
    check_image('no.jpg')
    check_image('no2.jpg')
    check_image('no3.jpg')
    
    # directory = input("Enter the directory path containing the images: ")
    # incomplete_images = check_images(directory)
    # if incomplete_images:
    #     print("\nThe following images are incomplete or corrupted:")
    #     for img in incomplete_images:
    #         print(img)
    # else:
    #     print("All images are complete and not corrupted.")
