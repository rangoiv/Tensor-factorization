"""
https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset?select=ratings.csv
"""

import numpy as np
from datetime import datetime

from sparse_array import NDSparseArray
from tensor_factorization import tensor_factorization, D, evaluate
from KNN_algorithm_functions import knn_algorithm, all_distances


def load_movies():
    arr = np.loadtxt(".\datasets\movies\\ratings_small.csv", delimiter=",", skiprows=1, dtype="i4,i4,f,i4")
    print("Loaded dataset")
    timestamps = [line[3] for line in arr]
    timestamps = [datetime.fromtimestamp(timestamp) for timestamp in timestamps]
    mini = min(timestamps).year
    timestamps = [(timestamp.year-mini)*12+timestamp.month for timestamp in timestamps]

    userIds = [line[0] for line in arr]
    movieIds = [line[1] for line in arr]
    ratings = [line[2] for line in arr]

    Y = NDSparseArray((max(userIds)+1, max(movieIds)+1, max(timestamps)+1))

    #data for KNN algorithm
    n = max(userIds)+1
    A = []
    for i in range(n):
        temp = []
        A.append(temp)
    for i in range(len(userIds)):
        A[userIds[i]].append((movieIds[i], ratings[i]))

    for i in range(len(userIds)):
        Y[userIds[i], movieIds[i], timestamps[i]] = ratings[i]

    return Y, A

def main():
    # LOAD DATA
    Y ,A = load_movies()
    Y_test = Y  # load_movies(".\datasets\movies\\ratings_small.csv")

    #comment block below if you don't need KNN algorithm results
    m = len(A)
    err_sum = 0
    cnt = 0
    for i in range(1,m):
        dist = all_distances(A, i)
        ret = knn_algorithm(10, i, A, dist)
        for j in range(len(A[i])):
            err_sum += abs(ret[j][1]-A[i][j][1])
            cnt += 1
    print(err_sum/cnt)

    # FACTORIZE
    # print(Y.shape)
    U, M, C, S = tensor_factorization(Y, D(27, 76, 13))

    # VERIFY
    print("Done!")
    SE = 0
    n = len(Y_test.elements)
    for i, j, k in Y_test.indexes():
        rating = Y_test[i, j, k]
        evalRating = evaluate(U, M, C, S, i, j, k)
        error = abs(rating - evalRating)
        SE += error
    MAE = SE / n
    print(MAE)

    


main()
