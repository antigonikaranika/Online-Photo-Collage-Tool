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

from PIL import Image, ImageColor

def add_border_to_image(img, border_size, border_color):
    bordered_img = Image.new(
        'RGB',
        (img.width + 2 * border_size, img.height + 2 * border_size),
        border_color
    )
    bordered_img.paste(img, (border_size, border_size))
    return bordered_img


def combine_images(images, collage_type, border_size, border_color, save_path):
    if not images:
        raise ValueError("No images provided.")

    # Convert hex to RGB
    try:
        border_rgb = ImageColor.getrgb(border_color)
    except ValueError:
        raise ValueError("Invalid border color format.")

    # Add inner border to each image
    bordered_images = [add_border_to_image(img, border_size, border_rgb) for img in images]

    widths, heights = zip(*(img.size for img in bordered_images))

    if collage_type == 'horizontal':
        total_width = sum(widths) + 2 * border_size  # extra left/right padding
        max_height = max(heights) + 2 * border_size  # extra top/bottom padding

        collage_image = Image.new('RGB', (total_width, max_height), border_rgb)

        x_offset = border_size  # start after left border
        for img in bordered_images:
            y_offset = (max_height - img.height) // 2
            collage_image.paste(img, (x_offset, y_offset))
            x_offset += img.width

    else:  # vertical
        max_width = max(widths) + 2 * border_size  # extra left/right padding
        total_height = sum(heights) + 2 * border_size  # extra top/bottom padding

        collage_image = Image.new('RGB', (max_width, total_height), border_rgb)

        y_offset = border_size  # start after top border
        for img in bordered_images:
            x_offset = (max_width - img.width) // 2
            collage_image.paste(img, (x_offset, y_offset))
            y_offset += img.height

    collage_image.save(save_path)





