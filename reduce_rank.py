from scipy import *
from numpy.linalg import svd
import argparse
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert a matrix to a lower rank matrix.')
    parser.add_argument('matrix', help='the path of the <matrix>.npy file')
    parser.add_argument('k', type=int, help='how many singular values to retain in the reduced matrix.')

    args = parser.parse_args()
    matrix_path = args.matrix
    k = args.k

    # load matrix from file
    matrix_array = load(matrix_path)

    # calculate:
    #   U_transpose = [u_1 u_2 ... u_n]^T (unitary)
    #   singular_values = [sigma_1 sigma_2 ... sigma_n] (singular values of A)
    #   V = AUD^-1  (unitary)
    V, singular_values, U_transpose = svd(matrix_array)

    # keep the k largest singular values
    singular_values = singular_values[:k]

    # make a diagonal matrix from the singular values
    D = diag(singular_values)

    # truncate the matrices V and U^T so that they have the right dimensions
    # for the VDU^T multiplication to work.
    V = V[:,:k]
    U_transpose = U_transpose[:k,:]

    # calculate A of rank k by A = VDU^T.
    # use numpy.matrix instead of arrays so that * operator overloads as matrix multiply
    A_k = matrix(V)*matrix(D)*matrix(U_transpose)

    # save A_k to file
    filename = os.path.splitext(matrix_path)[0]+'-reduced'
    save(filename, A_k)

    print 'writing rank reduced matrix to {}'.format(filename+'.npy')
    print 'Largest singular value {}'.format(singular_values[0])
    print 'Least singular value {}'.format(singular_values[-1])

