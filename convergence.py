import os

import pandas as pd
import numpy as np
from classification import classify_questions
from random import randint
from collections import Counter

answers = {
  "for-kids": {"false": 0, "true": 0},
  "science-technology": {"false": 0, "true": 0},
  "video-games": {"false": 0, "true": 0},
  "music": {"false": 0, "true": 0},
  "sports": {"false": 0, "true": 0},
}


#get most common item, in case of tie the first
def majority(lst):
  data = Counter(lst)
  return max(lst, key=data.get)


def main():
  exists = os.path.isfile('data/classified.csv')
  if exists:
    questions = pd.read_csv("data/classified.csv",
                            encoding="utf-8", sep=",")
    answers_to_questions = pd.read_csv("data/question_answer.csv",
                                       encoding="utf-8", sep=";")
    answers_to_questions.columns = ['question', 'answer']
    print(answers_to_questions.head())
    questions = questions.groupby('question').filter(
        lambda x: x['factuality'].sum() < 1)
    questions = questions.drop_duplicates(subset='question', keep="last")
    questions = questions.groupby(['topic'])

    # Threshold for skipping a topic when too many questions have been answered wrongly
    threshold = -2

    print("Convergence Module:")
    for i in range(100):
      for n, g in questions:
        if np.mean(
            [answers[n].get("false"), answers[n].get("true")]) < threshold:
          continue
        random_topic_question = g.sample(n=1, replace=True,
                                         random_state=randint(0, 10000))
        question = random_topic_question['question'].to_string(index=False)
        answer = answers_to_questions[
          answers_to_questions["question"].str.contains(question)][
          "answer"].to_string(index=False)
        print(question)
        print("Topic:", n)
        print("Secret:", answer)
        user_answer = input("Please give an answer:")
        false_answer = answer.strip().lower() != user_answer.strip().lower()
        if false_answer:
          answers[n]["false"] = answers[n].get("false") - 1
        else:
          answers[n]["true"] = answers[n].get("true") + 1
  else:
    classify_questions()


if __name__ == "__main__": main()
