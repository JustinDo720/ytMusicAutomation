import requests
import os


def save_thumbnail(all_thumbnails):
    new_images = []
    image_path = f'{os.getcwd()}/yt_thumbnails'

    if not os.path.exists(image_path):
        os.mkdir(image_path)

    # change dir to image_path
    os.chdir(image_path)
    # enumerate(list, starting_value)
    for count, thumbnail in enumerate(all_thumbnails, 1):
        # Each time, we will overwrite the previous image with the new one which saves us time from deleting
        file_name = f'image_{count}.jpg'
        with open(file_name, 'wb') as f:
            # We grab the bytes from the photos and write them to an actual photo placed in the image_path dir
            response = requests.get(thumbnail)
            f.write(response.content)
            new_images.append(file_name)

    return new_images