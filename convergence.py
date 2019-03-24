import os

import pandas as pd
import numpy as np
from classification import classify_questions
from random import randint

answers = {
          "for-kids": {"false" : 0, "true" : 0},
          "science-technology": {"false" : 0, "true" : 0},
          "video-games": {"false" : 0, "true" : 0},
          "music": {"false" : 0, "true" : 0},
          "sports": {"false" : 0, "true" : 0},
          }


def main():
  exists = os.path.isfile('data/classified.csv')
  if exists:
    questions = pd.read_csv("data/classified.csv",
                            encoding="utf-8", sep=",", error_bad_lines=False)
    questions = questions.groupby('question').filter(
      lambda x: x['factuality'].sum() < 1)
    questions = questions.drop_duplicates(subset='question', keep="last")
    questions = questions.groupby(['topic'])

    threshold = -2

    print("Convergence Module:")
    while True:
      for n,g in questions:
        if np.mean([answers[n].get("false"), answers[n].get("true")]) < threshold:
          continue
        random_topic_question = g.sample(n=1, replace=True, random_state=randint(0, 10000))
        question = random_topic_question['question'].to_string(index=False)
        answer = random_topic_question['answer'].to_string(index=False)
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
    print("hello")
    classify_questions()


if __name__ == "__main__": main()