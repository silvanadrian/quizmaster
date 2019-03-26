import nltk
import numpy as np
import pandas as pd
from scipy.stats import pearsonr
from sklearn.feature_extraction.text import TfidfVectorizer

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', -1)

def takeCorrelation(elem):
  return elem[1]

STEMMER = nltk.stem.porter.PorterStemmer()

def stem_tokens(tokens, stemmer=STEMMER):
  return [stemmer.stem(item) for item in tokens]


def tokenizer(text):
  tokens = nltk.word_tokenize(text)
  return stem_tokens(tokens)

def euclidean_distance(x, y):
  return np.sqrt(np.sum((x - y) ** 2))

def main():

  questions = get_friends_questions()

  type = input("Which friend recommending method? topic? features?")
  user_id = input("Please input your user id:")
  cutoff_k = input("Cutoff k:")
  if type == "topic":
    get_recommendations_topic(cutoff_k, questions, user_id)

  else:
    get_recommendations_feature(cutoff_k, questions, user_id)


def get_recommendations_feature(cutoff_k, questions, user_id):
  print("Feature based recommendation")
  tfidf = TfidfVectorizer(tokenizer=tokenizer, stop_words='english')
  tfs = tfidf.fit_transform(questions['question'])
  # add column for vector
  questions['tfsvector'] = list(tfs.toarray())
  user_features = questions[questions['id'] == int(user_id)]['tfsvector'].mean()
  # the questions which a user likes
  questions = questions.groupby(['id'])
  friends_questions = []
  for n, g in questions:
    g = g[g['opinion'] > 1]['tfsvector'].mean()
    friends_questions.append((n, euclidean_distance(user_features, g)))
  friends_questions.sort(key=takeCorrelation, reverse=True)
  for friend in friends_questions[:int(cutoff_k)]:
    print(friend)


def get_friends_questions():
  return pd.read_csv("data/classified.csv",
                     encoding="utf-8", sep=",")


def get_recommendations_topic(cutoff_k, questions, user_id):
  friends = []
  print("Topic based recommendation:")
  user_features = questions[questions['id'] == int(user_id)].groupby(['topic'])[
    'opinion'].mean()
  questions = questions.groupby(['id'])
  for n, g in questions:
    if n == int(user_id):
      continue
    # when classification not working properly then some users have only 4 topics
    if len(g.groupby(['topic'])['opinion'].mean()) < 5:
      continue
    corr, p_value = pearsonr(user_features,
                             g.groupby(['topic'])['opinion'].mean())
    friends.append((n, corr))
  friends.sort(key=takeCorrelation, reverse=True)
  for friend in friends[:int(cutoff_k)]:
    print(friend)


if __name__ == "__main__": main()