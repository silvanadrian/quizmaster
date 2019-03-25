import re

import numpy as np
import pandas as pd
from keras import utils
from keras.layers import Dense, Dropout, Activation
from keras.models import Sequential
from keras.preprocessing import text
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from collections import Counter

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', -1)


def classify_questions():
  labels = sorted(
      ['science-technology', 'for-kids', 'video-games', 'sports', 'music'])

  questions = pd.read_csv("data/train_dataset.csv", header=None,
                          encoding="iso-8859-1", sep=";",names= ['id', 'question', 'answer', 'topic'])

  REPLACE_BY_SPACE = re.compile('[/(){}\[\]|@,;]')
  BAD_SYMBOLS = re.compile('[^0-9a-z #+_]')
  STOPWORDS = set(stopwords.words('english'))


  def clean_text(text):
    text = text.lower()
    text = REPLACE_BY_SPACE.sub(' ', text)
    text = BAD_SYMBOLS.sub(' ', text)
    text = re.sub(r"\'s", " ", text)
    text = ' '.join(word for word in text.split() if
                    word not in STOPWORDS)
    return text

  questions['question'] = questions['question'].apply(clean_text)
  X = questions.question
  y = questions.topic
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,
                                                      random_state=42)

  # tokenizer
  max_words = 2000
  tokenize = text.Tokenizer(num_words=max_words, char_level=False)
  tokenize.fit_on_texts(X_train)
  x_train = tokenize.texts_to_matrix(X_train)
  x_test = tokenize.texts_to_matrix(X_test)

  # Encoder
  encoder = LabelEncoder()
  encoder.fit(y_train)
  y_train = encoder.transform(y_train)
  y_test = encoder.transform(y_test)

  num_classes = np.max(y_train) + 1
  y_train = utils.to_categorical(y_train, num_classes)
  y_test = utils.to_categorical(y_test, num_classes)


  batch_size = 64
  epochs = 4

  # Build the model
  model = Sequential()
  model.add(Dense(512, input_shape=(max_words,)))
  model.add(Activation('relu'))
  model.add(Dropout(0.5))
  model.add(Dense(num_classes))
  model.add(Activation('softmax'))
  model.compile(loss='categorical_crossentropy',
                optimizer='adam',
                metrics=['accuracy'])

  model.fit(x_train, y_train,
            batch_size=batch_size,
            epochs=epochs,
            verbose=1,
            validation_data=(x_test,y_test))

  val_score = model.evaluate(x_train, y_train,
                             batch_size=batch_size, verbose=1)
  score = model.evaluate(x_test, y_test,
                         batch_size=batch_size, verbose=1)
  print('Train acc:', val_score[1])
  print('Test accuracy:', score[1])

  # Classify topics
  generated_questions = pd.read_csv("data/crowdanswers.tsv",
                                    encoding="utf-8", delimiter="\t",
                                    na_filter=False)
  generated_questions.columns = ['id', 'question', 'answer', 'difficulty',
                                 'opinion', 'factuality']

  tokens = generated_questions['question'].apply(clean_text)

  x_predict = tokenize.texts_to_matrix(tokens)
  result = model.predict_classes(x_predict, batch_size=1)
  predicted_labels = [labels[i] for i in result]
  output = pd.DataFrame(data={"id": generated_questions["id"],
                              "question": generated_questions["question"],
                              "answer": generated_questions["answer"],
                              "difficulty": generated_questions["difficulty"],
                              "opinion": generated_questions["opinion"],
                              "factuality": generated_questions["factuality"],
                              "topic": predicted_labels})
  output.to_csv('data/classified.csv', encoding='utf-8', index=False)


#get most common item, in case of tie the first
def majority(lst):
  data = Counter(lst)
  return max(lst, key=data.get)



import os
def main():
  exists = os.path.isfile('data/classified.csv')
  if exists:
    questions = get_class_questions()

    print("Classification Module:")
    topic = input("Please enter topic: ")
    difficulty = input("Please enter difficulty: ")
    result = get_class_question(difficulty, questions, topic)
    print("Questions:")
    for index, row in result.iterrows():
      print(row['question'])
  else:
    classify_questions()


def get_class_questions():
  questions = pd.read_csv("data/classified.csv",
                          encoding="utf-8", sep=",", error_bad_lines=False)
  questions.groupby('question').filter(
      lambda x: x['factuality'].sum() < 1)
  questions = questions.groupby(['question', 'topic'], as_index=False)[
    'difficulty'].agg(majority)
  return questions


def get_class_question(difficulty, questions, topic):
  return questions[
    (questions.topic == topic) & (questions.difficulty == difficulty)]


if __name__ == "__main__": main()