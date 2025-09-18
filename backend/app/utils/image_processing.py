from PIL import Image
import os
import uuid

def resize_images(image_paths, collage_type):
    resized_images = []

    if collage_type == 'horizontal':
        # Resize all images to the same height
        target_height = min(Image.open(path).height for path in image_paths)

        for path in image_paths:
            img = Image.open(path)
            aspect_ratio = img.width / img.height
            new_width = int(target_height * aspect_ratio)
            img = img.resize((new_width, target_height))
            resized_images.append(img)

    elif collage_type == 'vertical':
        # Resize all images to the same width
        target_width = min(Image.open(path).width for path in image_paths)

        for path in image_paths:
            img = Image.open(path)
            aspect_ratio = img.height / img.width
            new_height = int(target_width * aspect_ratio)
            img = img.resize((target_width, new_height))
            resized_images.append(img)

    return resized_images

from PIL import Image

def combine_images(images, collage_type, border_size, border_color, save_path):
    # Assume 'images' is a list of PIL Image objects

    widths, heights = zip(*(img.size for img in images))

    if collage_type == 'horizontal':
        total_width = sum(widths) + border_size * (len(images) - 1)
        max_height = max(heights)
        collage_image = Image.new('RGB', (total_width, max_height), border_color)

        x_offset = 0
        for img in images:
            collage_image.paste(img, (x_offset, 0))
            x_offset += img.width + border_size

    else:  # vertical
        max_width = max(widths)
        total_height = sum(heights) + border_size * (len(images) - 1)
        collage_image = Image.new('RGB', (max_width, total_height), border_color)

        y_offset = 0
        for img in images:
            collage_image.paste(img, (0, y_offset))
            y_offset += img.height + border_size

    # Save the collage at the exact provided path
    collage_image.save(save_path)


