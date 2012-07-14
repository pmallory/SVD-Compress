from scipy import *
from numpy.linalg import svd
import argparse
import os

def reduce(array, k):
    """Given a multidimensional array, return equally sized array of reduced rank.
    
    array: what we're reducing. 3d and higher arrays are split into multiple 2d arrays
           which are reduced separately.
    k: the rank of the reduced matrix/matrices
    """
    # how many 2d arrays we have
    if len(unpacked_matrices.shape) is 2:
        channel_count = 1
    else:
        channel_count = unpacked_matrices.shape[2]

    # keep up with rank reduced matrices
    rank_reduced_matrices = []
    # keep track of greatest and least singular value of each channel
    gls = {}

    # Calculate the SVD of each color channel
    for channel_number in range(channel_count):
        if channel_count is 1:
            # if there's only one color channel, use it
            matrix = unpacked_matrices
        else:
            # otherwise slice one m x n matrix 
            matrix = unpacked_matrices[:,:,channel_number]

        # calculate:
        #   V = AUD^-1  (unitary)
        #   singular_values = [sigma_1 sigma_2 ... sigma_n] (singular values of A)
        #   U_transpose = [u_1 u_2 ... u_n]^T (unitary)
        V, singular_values, U_transpose = svd(matrix)

        # keep the k largest singular values
        singular_values = singular_values[:k]

        # make a diagonal matrix from the singular values
        D = diag(singular_values)

        # truncate the matrices V and U^T so that they have the right dimensions
        # for the VDU^T multiplication to work.
        V = V[:,:k]
        U_transpose = U_transpose[:k,:]

        # calculate A_k with A = VDU^T. treat our numpy.arrays as matrices so
        # matrix multiplication works. 
        A_k = asmatrix(V)*asmatrix(D)*asmatrix(U_transpose)

        # add this row reduced matrix to the collection
        rank_reduced_matrices.append(A_k)

        # record this channel's greatest and least singular values
        gls[channel_number] = (singular_values[0], singular_values[-1])

    if channel_count is 1:
        # if there's only one color channel that's our image
        composite_array = rank_reduced_matrices[0]
    else:
        # otherwise combine each channel's A_k into one multidimensional array
        composite_array = [array for array in rank_reduced_matrices]

    # print SVD stats
    for k, v in gls.iteritems():
        print 'Channel {}:'.format(k)
        print '\tGreatest singular value: {}'.format(v[0])
        print '\tLeast singular value: {}\n'.format(v[1])

    return composite_array

if __name__ == '__main__':
    # define command line arguments
    parser = argparse.ArgumentParser(description='Convert a matrix to a lower rank matrix.')
    parser.add_argument('matrix', help='the path of the <matrix>.npy file')
    parser.add_argument('k', type=int, help='how many singular values to retain in the reduced matrix.')

    # parse arguments
    args = parser.parse_args()
    matrix_path = args.matrix
    k = args.k

    # load matrices from file. What we're getting is a multidimensional array
    # composed of 2d arrays where each RGBA channel is it's own 2d
    # array. Grayscale images are only one array deep.
    unpacked_matrices = load(matrix_path)
    
    reduced_matrices = reduce(unpacked_matrices, k)

    # save row reduced matrices to a file
    filename = os.path.splitext(matrix_path)[0]+'-reduced'
    save(filename, reduced_matrices)

    print 'writing rank reduced matrix to {}\n'.format(filename+'.npy')


