
from sklearn.metrics import *


def evaluate_clf(clf, features_test, labels_test, name):
    '''
    This function takes a classifier (clf), test features (features_test),
    and test labels (labels_test) along with the method name (name) and 
    prints out some evaluation metrics. Note that you should run tester.py
    for an extensive evaluation.
    '''
    print ('Accuracy for', name, 'is: ', clf.score(features_test, labels_test))
    pred = clf.predict(features_test)
    print ('precision for', name, 'is: ', precision_score(pred, labels_test))
    print ('recall for' , name, 'is: ', recall_score(pred, labels_test))
    
def remove_from_list(orig_list, my_list):
    '''
    This function takes two lists and removes the items of the 
    second list(my_list) from the original list (orig_list)
    '''
    for item in my_list:
        if item in orig_list:
            orig_list.remove(item)
    return orig_list

