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


def main():
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

    args = parser.parse_args()

if __name__ == '__main__':
    main()
