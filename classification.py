import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from nltk.corpus import stopwords

questions = pd.read_csv("data/train_dataset.csv", header=None, encoding="iso-8859-1", sep=";")



