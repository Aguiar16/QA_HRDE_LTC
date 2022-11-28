from flask import Flask,request
import csv, json, ast, pickle,os
from collections import OrderedDict
import pandas as pd

keys = ["context","answer 0","answer 1","answer 2","answer 3","answer 4","answer 5","answer 6","answer 7","answer 8","answer 9"]  

app = Flask(__name__)


@app.route('/bot', methods = ['GET'])
def bot():
    return "Hello", 200


@app.route('/bot', methods = ['POST'])
def bot_response():
    questionJson = request.get_json()
    questionJson = ast.literal_eval(json.dumps(questionJson))
    questionJson = OrderedDict(sorted(questionJson.items()))
    # questionJsonKeys= list(reversed(questionJson))
    # print(questionJson)
    # save_question(questionJson)
    formatQuestion()

    return "OK",200

def save_question(dicts):
    with open('src/corona/botAPI.csv', 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = dicts)
        # writer.writeheader()
        writer.writerow(dicts)

    # (pd.DataFrame.from_dict(data=dicts).to_csv('src/corona/botAPI.csv'))

def find_index(word, dic):
    
    word = word.lower().strip()
    
    if dic.has_key(word):
        return dic[word]
    else:
        return dic['_UNK_']
def create_data_index(dataset):
    dic = pickle.load(open('../data/corona/corona_dic.pkl', 'r') )
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
    
    return data_set

def formatQuestion():
    test_data = []
    f = open('src/corona/botAPI.csv', 'r')
    csvReader = csv.reader(f)
    for row in csvReader:
        test_data.append(row)
    f.close()

    test_set = create_data_index(test_data)
    pickle.dump(test_set, open('src/corona/corona_data.pkl', 'w') )
    # print(test_set)
    os.system(" python API_RDE.py")
    # test_data = pickle.load(open('src/corona/corona_data.pkl', 'r') )
    # print(test_set)
    # # 
    # # initializing key 
    # data_key = 'data'
    
    # # Unnest single Key Nested Dictionary List
    # # Using loop + items()
    # res = dict()
    # for sub in test_list:
    #     for key, val in sub.items():
    #         res[key] = sub[key][data_key]


if __name__ == '__main__':
    app.run(debug=True)
