import catboost
import pickle
import numpy
import joblib
import warnings
import random
import config

warnings.simplefilter("ignore")
import vk


# def predict(a):
#     cont = [5, 7, 3, 5, 5, 4, 4, 8, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
#
#     ar=[]
#     for i in range(len(a)):
#         ar.append(int(a[i]))
#     v = numpy.array(ar)
#     v = numpy.delete(v, [5, 8])
#
#     mat = numpy.array([])
#     i = 0
#     for k in cont:
#         n = numpy.full((k), 0)
#         n[v[i] - 1] = 1
#         i += 1
#         mat = numpy.concatenate((mat, n))
#
#     mat = numpy.array(mat)
#     mat = mat.reshape(1, 74)
#
#     p=pred(mat)
#     #p - это наша категория
#     mod  = joblib.load('ml/m'+str(p+1)+'.pkl')
#     pid=mod.predict(mat)
#     profession_name=config.pr[p][pid]
#
#     return profession_name
import numpy
def pred(x):
    with open('ml/model.pkl', 'rb') as fin:
        model = pickle.load(fin)

    r = numpy.array(model.predict(x))
    r = r * config.wights
    r = r[0]
    return (numpy.where(r == r.max()))[0][0]

def predict(a):
    a1 = a[:11]
    a = a[11:] + a1

    cont = [5, 7, 3, 5, 5, 4, 4, 8, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]

    ar=[]
    for i in range(len(a)):
        ar.append(int(a[i]))
    v = numpy.array(ar)
    v = numpy.delete(v, [5, 8])

    mat = numpy.array([])
    i = 0
    for k in cont:
        n = numpy.full((k), 0)
        n[v[i] - 1] = 1
        i += 1
        mat = numpy.concatenate((mat, n))

    mat = numpy.array(mat)
    mat = mat.reshape(1, 74)
    p=pred(mat)

    #p - это наша категория
    # with open('ml/m'+str(p+1)+'.pkl', 'rb') as fin:
    #     mod = pickle.load(fin)
    # pid=mod.predict(mat)
    pid=random.randint(0,len(config.pr[p])-1)
    profession_name=config.pr[p][pid]

    return profession_name


# print(predict('323311133113513314325'))
