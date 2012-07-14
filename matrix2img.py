from scipy import *
import argparse
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert a matrix into an image. The output is a png in the same directory as the input matrix.')
    parser.add_argument('matrix', help='the path of your matrix file')

    args = parser.parse_args()

    matrix_path = args.matrix

    data = load(matrix_path)

    misc.imsave(os.path.splitext(matrix_path)[0]+'-output.png', data)
