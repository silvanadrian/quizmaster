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

labels = sorted(
    ['science-technology', 'for-kids', 'video-games', 'sports', 'music'])

pd.set_option('display.max_columns', None)  # or 1000
pd.set_option('display.max_rows', None)  # or 1000
pd.set_option('display.max_colwidth', -1)


def classify_questions():
  global REPLACE_BY_SPACE_RE, BAD_SYMBOLS_RE, STOPWORDS
  questions = pd.read_csv("data/train_dataset.csv", header=None,
                          encoding="iso-8859-1", sep=";")
  questions.columns = ['id', 'question', 'answer', 'topic']
  REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]|@,;]')
  BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
  STOPWORDS = set(stopwords.words('english'))

  def clean_text(text):
    text = text.lower()  # lowercase text
    text = REPLACE_BY_SPACE_RE.sub(' ',
                                   text)  # replace REPLACE_BY_SPACE_RE symbols by space in text
    text = BAD_SYMBOLS_RE.sub('', text)
    text = re.sub(r"\'s", " ", text)
    text = ' '.join(word for word in text.split() if
                    word not in STOPWORDS)  # delete stopwors from text
    return text

  questions['question'] = questions['question'].apply(clean_text)
  X = questions.question
  y = questions.topic
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,
                                                      random_state=42)
  train_posts = X_train
  train_tags = y_train
  test_posts = X_test
  test_tags = y_test
  max_words = 1000
  tokenize = text.Tokenizer(num_words=max_words, char_level=False)
  tokenize.fit_on_texts(train_posts)  # only fit on train
  x_train = tokenize.texts_to_matrix(train_posts)
  x_test = tokenize.texts_to_matrix(test_posts)
  encoder = LabelEncoder()
  encoder.fit(train_tags)
  y_train = encoder.transform(train_tags)
  y_test = encoder.transform(test_tags)
  num_classes = np.max(y_train) + 1
  y_train = utils.to_categorical(y_train, num_classes)
  y_test = utils.to_categorical(y_test, num_classes)
  batch_size = 32
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
                metrics=['categorical_accuracy'])

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
  generated_questions = pd.read_csv("data/crowdanswers.tsv",
                                    encoding="utf-8", delimiter="\t",
                                    na_filter=False)
  generated_questions.columns = ['id', 'question', 'answer', 'difficulty',
                                 'opinion', 'factuality']

  generated_questions['question'].apply(clean_text)
  x_predict = tokenize.texts_to_matrix(generated_questions['question'])
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


from collections import Counter

#get most common item, in case of tie the first
def majority(lst):
  data = Counter(lst)
  return max(lst, key=data.get)



import os
def main():
  exists = os.path.isfile('data/classified.csv')
  if exists:
    questions = pd.read_csv("data/classified.csv",
                            encoding="utf-8", sep=",", error_bad_lines=False)
    questions.groupby('question').filter(
      lambda x: x['factuality'].sum() < 1)
    questions = questions.groupby(['question', 'topic'], as_index=False)['difficulty'].agg(majority)

    print("Classification Module:")
    topic = input("Please enter topic: ")
    difficulty = input("Please enter difficulty: ")
    result = questions[
      (questions.topic == topic) & (questions.difficulty == difficulty)]
    print("Questions:")
    print(result.question.head(10).to_string())
  else:
    classify_questions()


if __name__ == "__main__": main()