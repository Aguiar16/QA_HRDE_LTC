import pickle
# import cPickle
import numpy as np
import operator

# esse arquivo gera o modelo_glove.pkl utilizando o arquivo glove e o modelo_dic.pkl

def loadGloveModel(gloveFile):
    print "Loading Glove Model"
    f = open(gloveFile,'r')
    model = {}
    for line in f:
        splitLine = line.split()
        word = splitLine[0]
        embedding = [float(val) for val in splitLine[1:]]
        model[word] = embedding
    print "Done.",len(model)," words loaded!"
    return model



def cal_coverage_num(voca):

    has_cnt = 0
    total_cnt = 0
    
    for token in voca.keys():
        
        total_cnt += voca[token]
        
        if glove.has_key( token ):
            has_cnt += voca[token]
        else:
            ("")

    print 'coverage_num : ' + str( ( has_cnt/ float( total_cnt ) ) ) 



def cal_coverage(voca):

    cnt = 0
    for token in voca.keys():
        if glove.has_key( token ):
            ("")
        else:
            cnt = cnt + 1

    print '# missing token : ' + str(cnt)
    print 'coverage : ' + str( 1 - ( cnt/ float(len(voca)) ) ) 



def create_glove_embedding(voca):

    # sorting voca dic by value
    sorted_voca = sorted(voca.items(), key=operator.itemgetter(1))
    
    list_glove_voca = []

    cnt = 0

    for token, value in sorted_voca:

        if glove.has_key( token ):
            list_glove_voca.append( glove[token] )
        else:
            if token is '_PAD_':
#             if token is '':    # pad case
                list_glove_voca.append( np.zeros(300) )  
            else:
                list_glove_voca.append( np.random.uniform(-0.25, 0.25, 300).tolist() )
                cnt = cnt + 1  

    print 'coverage : ' + str( 1 - ( cnt/ float(len(voca)) ) )
    return list_glove_voca

glove = loadGloveModel('../data/embedding/glove_s300.txt')

# ### ubuntu-v2 case

voca = pickle.load( open('../data/corona/corona_dic.pkl', 'r') )

cal_coverage(voca)
cal_coverage_num(voca)
list_glove_voca = create_glove_embedding(voca)

pickle.dump( np.asarray(list_glove_voca), open('../data/corona/corona_glove.pkl', 'w'))









