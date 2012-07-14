from scipy import *
import argparse
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert an image into a matrix. The output is a binary file <img>.npy in the same directory as the input image.')
    parser.add_argument('img', help='the path of your image file')

    args = parser.parse_args()
    img_path = args.img

    img_array = misc.imread(img_path)
    
    save(os.path.splitext(img_path)[0]+'-matrix', img_array)

