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
import get_image_size

supported_types = ".png .jpeg .jpg .gif .bmp .ico .tiff .tif"


def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))

    args = setup_parser()

    width = -1
    height = -1

    if not(args.path == ""):
        dir_path = os.path.join(dir_path, args.path)

    for root, dirs, files in os.walk(dir_path):
        for file in files:
            try:
                width, height = get_image_size.get_image_size(os.path.join
                                                              (root, file))
            except get_image_size.UnknownImageFormat:
                print("Can't get size of "+file+" Propably not an image.")
            else:
                print(width, height)


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

    return parser.parse_args()

if __name__ == '__main__':
    main()
