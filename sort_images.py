"""
sort_images.py
====================

    :Name:        sort_images
    :Purpose:     extract image dimensions given a file path

    :Author:      Nick Panagopoulos

    :Created:     29/11/2016
    :Copyright:   (c) Nick Panagopoulos 2016
    :Licence:     MIT

"""

import argparse
import os
import shutil

import get_image_size


def main():
    # Get arguments
    args = setup_parser()

    # Initialise image width and height
    width = -1
    height = -1

    # Get verbose flag from arguments
    verbFlag = args.verbose
    # Get clean flag from arguments
    cleanFlag = args.clean
    # Get folder where sorted images will be moved to from arguments
    folder = args.folder
    # Get min width and height from arguments
    min_width = args.width
    min_height = args.height

    # Set the path to search
    if not(args.path == ""):
        # Get path from arguments
        dir_path = args.path
    else:
        # Get path from where the script was run from
        dir_path = os.path.dirname(os.path.realpath(__file__))

    # Setup the path where sorted images will be moved to
    sort_path = os.path.join(dir_path, folder)
    if verbFlag:
        print("Making sort folder "+folder+" in "+dir_path)

    # Create the sorted folder if it does not already exist
    try:
        os.mkdir(sort_path)
    except OSError:
        if verbFlag:
            print("Folder already exists")

    # Check which sort mode will be used based on arguments given
    if (min_width == -1) and (min_height == -1):
        # No proper arguments where given
        print("Please enter proper arguments. (-h for usage)")
        return
    elif min_width == -1:
        # Sort images only by height
        flagSort = "height"
    elif min_height == -1:
        # Sort images only by width
        flagSort = "width"
    elif args.either:
        # Sort images by width OR height
        flagSort = "either"
    else:
        # Sort images by width AND height
        flagSort = "both"

    # Search the dir_path for images
    for root, dirs, files in os.walk(dir_path):
        # Skip the folder where sorted images will be moved to
        if root == sort_path:
            if verbFlag:
                print("Skipping folder "+folder)
            continue
        if verbFlag:
            print("Searching "+root)
        for file in files:
            valid = False
            # Get current file's path
            file_path = os.path.join(root, file)
            # Get current file's width and height, if it's an image
            try:
                width, height = get_image_size.get_image_size(file_path)
            except get_image_size.UnknownImageFormat:
                if verbFlag:
                    print("Can't get size of "+file+" Propably not an image.")
            else:
                # Check the image's size based on the sort mode used
                if flagSort == "height":
                    if height < min_height:
                        valid = True
                elif flagSort == "width":
                    if width < min_width:
                        valid = True
                elif flagSort == "either":
                    if (width < min_width) or (height < min_height):
                        valid = True
                elif flagSort == "both":
                    if (width < min_width) and (height < min_height):
                        valid = True
                if valid:
                    # Move the image to the predefined folder
                    if verbFlag:
                        print("Moving "+file)
                    shutil.move(file_path, os.path.join(sort_path, file))

    if cleanFlag:
        # Delete sorted folder and its contents
        shutil.rmtree(sort_path)
        if verbFlag:
            print("Deleting folder: "+folder)
    else:
        # Delete sorted folder if it's empty
        try:
            os.rmdir(sort_path)
            if verbFlag:
                print("Deleting empty folder: "+folder)
        except OSError:
            # Raises error if not empty
            pass

    if verbFlag:
        print("Action completed.")


def setup_parser():
    parser = argparse.ArgumentParser(description="""Move images with dimensions smaller than the ones defined to the folder <folder> (default: 'sorted').
    --width W: Images with width smaller than W will be sorted.
    --height H: Images with height smaller than H will be sorted.
    --width W --height H: Images with width smaller than W AND height smaller than H will be sorted.
    --width W --height H --either: Images with width smaller than W OR height smaller than H will be sorted.""", formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument("--width", type=int, default="-1", help="images with width less than the value defined will be moved to the folder <folder>")

    parser.add_argument("--height", type=int, default="-1", help="images with height less than the value defined will be moved to the folder <folder>")

    parser.add_argument("--either", action="store_true", help="when providing both width and height arguments use this to make the sorter check if image width OR height is smaller than the defined values")

    parser.add_argument("-p", "--path", nargs='?', default='', const='',
                        help="path to the folder where you want the script to scan")

    parser.add_argument("-f", "--folder", nargs='?', default='sorted',
                        const='sorted', help="name of the folder where detected images will be moved to")

    parser.add_argument("-v", "--verbose", action="store_true", help="increase output verosity")

    parser.add_argument("-c", "--clean", action="store_true", help="delete the sorted pictures")

    return parser.parse_args()

if __name__ == '__main__':
    main()
