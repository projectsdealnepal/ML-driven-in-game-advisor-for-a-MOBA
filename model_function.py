import pickle
import pandas as pd
import numpy as np
import joblib
'''We have to send the list of features here in MopaModel function.
The List of features are "time", "hero_id","item_0",
"item_1","item_2","item_3","item_4","item_5","gold_t"
''' 
def MopaModel(x,*args,**kwargs):
    dataset1 = pd.read_csv('MLdata.csv')
    dataset=dataset1.iloc[:,1:]
    #print(dataset)
    dataset = dataset.astype({"key": str})
    #print(dataset.head())
    # #Creating the dependent variable class
    factor = pd.factorize(dataset['key'])
    dataset.key = factor[0]
    definitions = factor[1]
    #pickled_model = pickle.loads(open("", 'rb'))
    with open('model1.pkl', 'rb') as p:
     pickled_model = joblib.load(p)
    #Reverse factorize (converting y_pred from 0s,1s and 2s to Real Item Name)
    reversefactor = dict(zip(range(99),definitions))
    y_pred = pickled_model.predict(x)
    y_pred = np.vectorize(reversefactor.get)(y_pred)
    return (y_pred)

#Example of testing Data in a model function above 
# a=MopaModel([[55,-82,129,50,1,178,73,36,73]])
# print(a)


