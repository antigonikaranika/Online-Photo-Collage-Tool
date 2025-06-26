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

def combine_images(resized_images, collage_type, border_size, border_color, output_dir='static/collages'):
    os.makedirs(output_dir, exist_ok=True)

    if collage_type == 'horizontal':
        total_width = sum(img.width for img in resized_images) + border_size * (len(resized_images) - 1)
        max_height = max(img.height for img in resized_images)
        collage = Image.new('RGB', (total_width, max_height), border_color)

        x_offset = 0
        for img in resized_images:
            collage.paste(img, (x_offset, 0))
            x_offset += img.width + border_size

    elif collage_type == 'vertical':
        max_width = max(img.width for img in resized_images)
        total_height = sum(img.height for img in resized_images) + border_size * (len(resized_images) - 1)
        collage = Image.new('RGB', (max_width, total_height), border_color)

        y_offset = 0
        for img in resized_images:
            collage.paste(img, (0, y_offset))
            y_offset += img.height + border_size

    # Generate unique ID for collage
    collage_id = str(uuid.uuid4())
    collage_filename = f'collage_{collage_id}.jpg'
    collage_path = os.path.join(output_dir, collage_filename)
    collage.save(collage_path)

    return collage_id, collage_path

