
# coding: utf-8

# In[395]:

#! /usr/bin/env python


# Please see EnronFraud_ML.docx for more details on the dataset and approches.
# 
# Let's first import some libraries and modules.

# In[396]:

import sys
import pickle
import pandas as pd
import numpy as np
import warnings
sys.path.append("../tools/")
from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data
from sklearn.metrics import *
from poi_functions import *
from sklearn.grid_search import GridSearchCV

warnings.filterwarnings('ignore')



# In[397]:

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)


# Here, I'll convert the dictionary to a pandas dataframe to do some feature engineering.

# In[398]:

# Convert the dictionary to a pd dataframe
df = pd.DataFrame.from_records(list(data_dict.values()))
employees = pd.Series(list(data_dict.keys()))

# set the index of df to be the employees series:
df.set_index(employees, inplace=True)

# Drop the email_address column because it has no use for us
if 'email_address' in df:
    del df['email_address']
    
### The first feature must be "poi". Make this happen
poi = df['poi']
df.drop(labels=['poi'], axis=1, inplace = True)
df.insert(0, 'poi', poi)

from sklearn.preprocessing import LabelEncoder

# Change the datatype to float. 
df = df.apply(lambda x: pd.to_numeric(x, errors='coerce')).copy() 

#convert booleans to int
for c in df.columns:
    if df[c].dtype == 'bool':
        lbl = LabelEncoder()
        lbl.fit(list(df[c].values))
        df[c] = lbl.transform(list(df[c].values))

df.head()


# Let's explore the data a bit.

# In[399]:

#Get some basic information
print df.info()
missing = df.isnull().sum(axis=0).reset_index()
# Get the number of missing values
missing.columns = ['column_name', 'missing_count']
missing = missing.ix[missing['missing_count']>0]
missing = missing.sort_values(by='missing_count')
print missing.head()

row_missing = df.isnull().sum(axis=1).reset_index()
row_missing.columns = ['column_name', 'missing_count']
row_missing = row_missing.sort_values(by='missing_count', ascending=False)
print row_missing.head()


# How many poi do we have here:

# In[400]:

df['poi'].sum()


# Let's take a quick look at the employees name.

# In[401]:

df.index


# There is an employee named 'TOTAL' which contains the sum of all values from other employees. There is another employee named 'THE TRAVEL AGENCY IN THE PARK'. These are our outlier, let's remove them. 

# In[402]:

df = df.drop(['TOTAL', 'THE TRAVEL AGENCY IN THE PARK'])


# Rescale the financial features. Note that this helps NB algorithm but apparently hurts DecisionTree a bit. 

# In[403]:

from sklearn.preprocessing import MinMaxScaler
df = df.fillna(0)
features = list(df.columns.values)
other_features = ['poi', 'to_messages','shared_receipt_with_poi',
                    'from_messages', 'from_poi_to_this_person', 'from_this_person_to_poi']
financial_features = remove_from_list(features, other_features)

scaler = MinMaxScaler()
df[financial_features] = scaler.fit_transform(df[financial_features])


# After a few iterations, I realized that we need to create some new features to make a good models. Here I create two new features. 1) the portion of emails that a person sent to a poi, 2) the portion of emails that a person received from a poi. Intuitevely, these two must be very important. 

# In[404]:

### Create new feature(s)
df['to_poi_ratio'] = df['from_this_person_to_poi']/df['from_messages']
df['from_poi_ratio'] = df['from_poi_to_this_person']/df['to_messages']
df = df.fillna(0)


# Prepare the data for compatibility with sklearn.

# In[405]:

labels = df['poi'].values
features = df.drop(['poi'], axis = 1).values


# Do a first round of feature selection. Here I use SelectKBest to get the score of all features. I'll then drop the features that have score of 2 or smaller.

# In[406]:

from sklearn.feature_selection import SelectKBest
# Create a SelectKBest object.
select = SelectKBest(k=features.shape[1])
features = select.fit_transform(features, labels)
#Get and print the scores
KBest_scores = select.scores_
print KBest_scores
# Find important features
important_features = df.drop(['poi'], axis = 1).columns.values[np.where(KBest_scores > 10)]
# Find features that will be dropped.
dropped_features = df.drop(['poi'], axis = 1).columns.values[np.where(KBest_scores <= 10)]
#Print some information
print ("Important features", important_features)
print ("Number of important features", len(important_features))
print ("Number of dropped features: ", len(dropped_features))
#Drop less important features
for feature in dropped_features:
    df = df.drop(feature, axis =1)


# Convert the dataframe back to a dictionary, and split them again.

# In[407]:

# create a list of column names:
features_list = df.columns.values

# create a dictionary from the dataframe
data_dict = df.to_dict('index')
### Store to my_dataset for easy export below.
my_dataset = data_dict

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

### Try a varity of classifiers
from sklearn.cross_validation import train_test_split
features_train, features_test, labels_train, labels_test =     train_test_split(features, labels, test_size=0.3, random_state=42)


# Instead of assigning different names to my classifiers I put them into "if clauses". That way we can turn them on/off quickly.  

# In[408]:

# NaiveBayes 
if True:
    from sklearn.naive_bayes import GaussianNB
    clf = GaussianNB()
    clf.fit(features_train, labels_train)
    evaluate_clf(clf, features_test, labels_test, 'NB')


# In[409]:

# Decision Tree
if False:
    from sklearn import tree
    param_grid = {
            'min_samples_split': [2, 5, 10],
            'max_features': [5, 10, len(features_list)-1]
            }
    clf = GridSearchCV(tree.DecisionTreeClassifier(random_state = 42), param_grid)
    clf = clf.fit(features_train, labels_train)
    print "Best estimator found by grid search for DecisionTree:"
    print clf.best_estimator_
    evaluate_clf(clf, features_test, labels_test, 'DecisionTree')


# In[410]:

# Support Vector Machine
if False:
    from sklearn import svm
    param_grid = {
            'C': [1e3, 5e3, 1e4, 5e4, 1e5]
            }
    clf = GridSearchCV(svm.SVC(kernel='linear', class_weight='balanced'), param_grid)
    clf = clf.fit(features_train, labels_train)
    print "Best estimator found by grid search for SVM:"
    print clf.best_estimator_
    evaluate_clf(clf, features_test, labels_test, 'SVM')


# In[411]:

# Random Forest
if False:
    from sklearn.ensemble import RandomForestClassifier
    param_grid = {
            'n_estimators': [5, 10, 50]
            }
    clf = GridSearchCV(RandomForestClassifier(min_samples_split= 2, criterion='entropy', random_state=42), param_grid)
    clf = clf.fit(features_train, labels_train)
    print "Best estimator found by grid search for RandomForest:"
    print clf.best_estimator_
    evaluate_clf(clf, features_test, labels_test, 'RandomForest')


# In[412]:

### Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)

