from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB

import pickle
from pathlib import Path
import os

data_folder = Path("./clsfr/")

logreg = None
with open(data_folder / "LogReg.pkl", 'rb') as fl:
    logreg = pickle.load(fl)

vectorizer = None
with open(data_folder / 'vectorizer.pkl', 'rb') as fl:
    vectorizer = pickle.load(fl)

vectorizerTfidf = None
with open(data_folder / 'vectorizerTfidf.pkl', 'rb') as fl:
    vectorizerTfidf = pickle.load(fl)

svmTfidf = None
with open(data_folder / 'svmTfidf.pkl', 'rb') as fl:
    svmTfidf = pickle.load(fl)

rfTfidf = None
with open(data_folder / 'RandomForestClassifierTfidf.pkl', 'rb') as fl:
    rfTfidf = pickle.load(fl)

NBTfidf = None
with open(data_folder / 'MultinomialNBTfidf.pkl', 'rb') as fl:
    NBTfidf = pickle.load(fl)

LogRegTfidf = None
with open(data_folder / 'LogRegTfidf.pkl', 'rb') as fl:
    LogRegTfidf = pickle.load(fl)

