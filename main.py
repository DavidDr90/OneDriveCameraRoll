from os import listdir
from os.path import isfile, join
from pprint import pprint
from PIL import Image
import datetime
import os
from PIL import Image
from PIL.ExifTags import TAGS
import re
import shutil


def get_date_of_creation(file_name):
    image = Image.open(file_name)
    # extract EXIF data
    exifdata = image.getexif()
    # iterating over all EXIF data fields
    for tag_id in exifdata:
        # get the tag name, instead of human unreadable tag id
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)
        if tag == "DateTime":
            # decode bytes
            if isinstance(data, bytes):
                data = data.decode()
            return data.split(' ')[0]


def get_modified_date(file_path):
    # file modification timestamp of a file
    m_time = os.path.getmtime(file_path)
    # convert timestamp into DateTime object
    dt_m = datetime.datetime.fromtimestamp(m_time)
    return str(dt_m.date()).replace('-', ':')


def get_date_from_file_name(file_path):
    file_name = os.path.basename(file_path)
    if '-' not in file_name:
        return None
    temp_list = re.findall(r"[\d+-]", file_name)  # get only the date and time part
    date_string = ''.join(temp_list)
    temp_list = date_string.split('-')
    date_string = ':'.join(temp_list[:3])
    return date_string


def move_file_to_folder(file_name, year_folder, month_folder):
    folder_path = os.path.dirname(file_name)
    folder_path = os.path.join(folder_path, year_folder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    folder_path = os.path.join(folder_path, month_folder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    print(f"Image: {file_name}\tyear: {year_folder}\tmonth: {month_folder}\t\tMove to: {folder_path}")
    shutil.move(file_name, folder_path)


if __name__ == "__main__":
    print("Start")
    path = r"C:\Users\david\OneDrive\Pictures\Camera Roll"

    all_image_files = []
    for file in os.listdir(path):
        if not file.endswith(".mp4"):  # filter movies
            all_image_files.append(os.path.join(path, file))

    for image_path in all_image_files:
        try:
            date = get_date_of_creation(image_path)
            if not date:
                date = get_date_from_file_name(image_path)
                if not date:
                    date = get_modified_date(image_path)

            if not date:
                continue

            dt = datetime.datetime.strptime(date, '%Y:%m:%d')
            print(f"{image_path:40}: {date}\t\tyear: {dt.year}\tmonth: {dt.month}")
            move_file_to_folder(image_path, str(dt.year), str(dt.month))
        except Exception as e:
            print(f"Error. file: {image_path}. message: {str(e)}")
