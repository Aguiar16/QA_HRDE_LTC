from pre_processing import *
import pickle
import csv
from Vocab import *
# create dictionary

def read_train(dic, file_name):

    print 'data read : ' + file_name

    f = open(file_name, 'r')
    csvReader = csv.reader(f)
    for row in csvReader:
        
        for i in xrange(2):
            for token in row[i].split(" "):
                
                token = token.lower().strip()
                
                dic_ori[token] += 1
        
    f.close()
    
    return dic

def read_test(dic, file_name):

    print 'data read : ' + file_name

    f = open(file_name, 'r')
    csvReader = csv.reader(f)
    
    count = 0
    
    for row in csvReader:

        if count == 0:
            for i in xrange(2):
                for token in row[i].split(" "):
                    
                    token = token.lower().strip()
                    
                    dic[token] += 1
        else:
            for token in row[1].split(" "):
                
                    token = token.lower().strip()
                    
                    dic[token] += 1

        count = count +1
        if count == 10:
            count = 0
    
    return dic

# ### ubuntu-v2

dic_ori = defaultdict(int)

dic_ori = read_train(dic_ori, '../data/corona/train.csv')

dic_ori = read_test(dic_ori, '../data/corona/valid.csv')

pickle.dump( dic_ori, open('../data/corona/dic_ori.pkl', 'w')  )


# ## reducing dictionary

pp = PRE_PROCESSING()

dic_ori = pickle.load( open('../data/corona/dic_ori.pkl', 'r') )
pp.frequency_ori = dic_ori
dic = pp._apply_mincut(3)

voca = {}
voca['_PAD_'] = len(voca)
voca['_UNK_'] = len(voca)

for word in dic.keys():
    voca[word] = len(voca)    
    

pickle.dump( voca, open('../data/corona/corona_dic.pkl', 'w')  )

# ### convert data to index format

dic = pickle.load(open('../data/corona/corona_dic.pkl', 'r') )

v = Vocab(dic)


train_data = []

f = open('../data/corona/train.csv', 'r')
# f = open('../data/samsungQA/train.csv', 'r')
csvReader = csv.reader(f)
for row in csvReader:
    train_data.append(row)
f.close()

val_data = []

f = open('../data/corona/valid.csv', 'r')
# f = open('../data/samsungQA/valid.csv', 'r')
csvReader = csv.reader(f)
for row in csvReader:
    val_data.append(row)
f.close()

test_data = []

f = open('../data/corona/test.csv', 'r')
# f = open('../data/samsungQA/test.csv', 'r')
csvReader = csv.reader(f)
for row in csvReader:
    test_data.append(row)
f.close()

def find_index(word, dic):
    
    word = word.lower().strip()
    
    if dic.has_key(word):
        return dic[word]
    else:
        return dic['_UNK_']

def create_data_index(dataset):
    data_set = {}

    context = []
    for sent in dataset:
        context.append( [ find_index(x, dic) for x in sent[0].split(' ')] )

    response = []
    for sent in dataset:
        response.append( [find_index(x, dic) for x in sent[1].split(' ')] )

    label = [ x[2] for x in dataset ]

    data_set['c'] = context
    data_set['r'] = response
    data_set['y'] = label

    len(data_set)
    
    return data_set


train_set = create_data_index(train_data)

valid_set = create_data_index(val_data)

test_set = create_data_index(test_data)

pickle.dump( [train_set, valid_set, test_set], open('../data/corona/corona_data.pkl', 'w') )


train_set_test = {}
valid_set_test = {}
test_set_test = {}

train_set_test['c'] = train_set['c'][:500]
train_set_test['r'] = train_set['r'][:500]
train_set_test['y'] = train_set['y'][:500]

valid_set_test['c'] = valid_set['c'][:5000]
valid_set_test['r'] = valid_set['r'][:5000]
valid_set_test['y'] = valid_set['y'][:5000]

test_set_test['c'] = test_set['c'][:5000]
test_set_test['r'] = test_set['r'][:5000]
test_set_test['y'] = test_set['y'][:5000]

pickle.dump( [train_set_test, valid_set_test, test_set_test], open('../data/corona/corona_data_test.pkl', 'w') )
# pickle.dump( [train_set_test, valid_set_test, test_set_test], open('../data/samsungQA/SA_data_test.pkl', 'w') )



