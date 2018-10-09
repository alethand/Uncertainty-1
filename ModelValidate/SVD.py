from numpy.linalg import svd
import numpy as np



def svdAlg(movieRatings):
    U, singularValues, V = svd(movieRatings)
    # settingN = 2
    # print "U"
    # print(U)
    # print("-----------")
    # print "singularValues"
    # print(singularValues)
    # print("-----------")
    # print "V"
    # print(V)

    # print("---------------------------")
    # # U1 = U[:, :settingN]
    # # singularValues1 = singularValues[:settingN]
    # # V1 = V[:settingN, :]
    # print "U1"
    # print(U1)
    # print("-----------")
    # print "singularValues1"
    # print(singularValues1)
    # print("-----------")
    # print "V1"
    # print(V1)
    # print("--------------------------")


    # Sigma = np.vstack([
    #     np.diag(singularValues),
    #     np.zeros((
    #         len(movieRatings) -
    #         len(singularValues),
    #         len(V[0]
    #             if V != []
    #                and
    #                isinstance(V[0],list)==
    #                True
    #             else [0]))),
    # ])


    # print "Sigma"
    # print(Sigma)
    # print("-----------")
    # Sigma1 = np.diag(singularValues1)
    # print "Sigma1"
    # print(Sigma1)
    # print("--------------------------")
    # print(np.round(movieRatings - np.dot(U, np.dot(Sigma, V)), decimals=10))
    # print("-----------")
    #
    # print(np.round(movieRatings - np.dot(U1, np.dot(Sigma1, V1)), decimals=10))

    # a = np.array([singularValues[0],singularValues[0]])
    # return a
    return singularValues

    # return U, [singularValues], V








# movieRatings = [
#     [2, 5, 3, 2, 7, 8, 9, 1],
#     [1, 2, 1, 2, 4, 5, 1, 12],
#     [4, 1, 1, 9, 1, 12, 2, 7],
#     [3, 5, 2, 4, 1, 4, 5, 5],
#     [5, 3, 1, 7, 7, 9, 1, 4],
#     [4, 5, 5, 9, 1, 3, 3, 6],
#     [2, 4, 2, 8, 4, 3, 2, 8],
#     [2, 2, 5, 4, 6, 8, 1, 7],
# ]
#
# U, singularValues, V = svd(movieRatings)
# settingN = 2
# print "U"
# print(U)
# print("-----------")
# print "singularValues"
# print(singularValues)
# print("-----------")
# print "V"
# print(V)
#
# print("---------------------------")
# U1 = U[:, :settingN]
# singularValues1 = singularValues[:settingN]
# V1 = V[:settingN, :]
# print "U1"
# print(U1)
# print("-----------")
# print "singularValues1"
# print(singularValues1)
# print("-----------")
# print "V1"
# print(V1)
# print("--------------------------")
#
#
# Sigma = np.vstack([
#     np.diag(singularValues),
#     np.zeros((len(movieRatings)-len(singularValues), len(V[0] if V != [] else 0))),
# ])
# print "Sigma"
# print(Sigma)
# print("-----------")
# Sigma1 = np.diag(singularValues1)
# print "Sigma1"
# print(Sigma1)
# print("--------------------------")
# print(np.round(movieRatings - np.dot(U, np.dot(Sigma, V)), decimals=10))
# print("-----------")
#
# print(np.round(movieRatings - np.dot(U1, np.dot(Sigma1, V1)), decimals=10))
