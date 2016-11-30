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
    dir_path = os.path.dirname(os.path.realpath(__file__))

    args = setup_parser()

    width = -1
    height = -1

    verbFlag = args.verbose
    cleanFlag = args.clean

    if not(args.path == ""):
        dir_path = os.path.join(dir_path, args.path)

    folder = args.folder

    sort_path = os.path.join(dir_path, folder)
    if verbFlag:
        print("Making sort folder "+folder+" in "+dir_path)

    try:
        os.mkdir(sort_path)
    except OSError:
        if verbFlag:
            print("Folder already exists")

    min_width = args.width
    min_height = args.height

    for root, dirs, files in os.walk(dir_path):
        if root == sort_path:
            if verbFlag:
                print("Skipping folder "+folder)
            continue
        if verbFlag:
            print("Searching "+root)
        for file in files:
            file_path = os.path.join(root, file)
            try:
                width, height = get_image_size.get_image_size(file_path)
            except get_image_size.UnknownImageFormat:
                if verbFlag:
                    print("Can't get size of "+file+" Propably not an image.")
            else:
                if (width < min_width) and (height < min_height):
                    if verbFlag:
                        print("Moving "+file)
                    shutil.move(file_path, os.path.join(sort_path, file))

    if cleanFlag:
        shutil.rmtree(sort_path)
        if verbFlag:
            print("Deleting folder: "+folder)
    else:
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
    parser = argparse.ArgumentParser(description="Move images with dimensions\
                                     smaller than the ones defined to the\
                                     folder <folder> (default: 'sorted').")

    parser.add_argument("width", type=int, help="images with width less than the\
                        value defined will be moved to the folder <folder>")

    parser.add_argument("height", type=int, help="images with height less than\
                        the value defined will be moved to the folder\
                        <folder>")

    parser.add_argument("-p", "--path", nargs='?', default='', const='',
                        help="path to the folder where you want the script to\
                        scan")

    parser.add_argument("-f", "--folder", nargs='?', default='sorted',
                        const='sorted', help="name of the folder where detected\
                        images will be moved to")

    parser.add_argument("-v", "--verbose", action="store_true", help="increase\
                         output verosity")

    parser.add_argument("-c", "--clean", action="store_true", help="delete the\
                        sorted pictures")

    return parser.parse_args()

if __name__ == '__main__':
    main()
