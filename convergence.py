from collections import Counter
from random import randint

import numpy as np
import pandas as pd

pd.set_option('display.max_columns', None)  # or 1000
pd.set_option('display.max_rows', None)  # or 1000
pd.set_option('display.max_colwidth', -1)  # or 199

answers = {
  "for-kids": {"false": 0, "true": 0},
  "science-technology": {"false": 0, "true": 0},
  "video-games": {"false": 0, "true": 0},
  "music": {"false": 0, "true": 0},
  "sports": {"false": 0, "true": 0},
}

skipped = []

#get most common item, in case of tie the first
def majority(lst):
  data = Counter(lst)
  return max(lst, key=data.get)

def get_answers():
  return answers

def get_next_question(g):
  return g.sample(n=1, replace=True,
           random_state=randint(0, 3000))

def calc_threshold(threshold, n):
  return np.mean(
      [answers[n].get("false"), answers[n].get("true")]) < threshold

# use answers from file + answers from classified data,since a few questions missing
def give_answer(answer,generated_answer,user_answer,n):
  false_answer2 = generated_answer.strip().lower() != user_answer.strip().lower()
  false_answer = answer.strip().lower() != user_answer.strip().lower()
  if (false_answer & false_answer2):
    answers[n]["false"] = answers[n].get("false") - 1
  else:
    answers[n]["true"] = answers[n].get("true") + 1

def get_conv_questions():
  questions = pd.read_csv("data/classified.csv",
                          encoding="utf-8", sep=",")
  questions = questions.groupby('question').filter(
      lambda x: x['factuality'].sum() < 1)
  questions = questions.drop_duplicates(subset='question', keep="last")
  return questions.groupby(['topic'])


def get_answers_to_questions():
  answers_to_questions = pd.read_csv("data/question_answer.csv",
                                     encoding="utf-8", sep=";")
  answers_to_questions.columns = ['question', 'answer']
  return answers_to_questions

def main():
    answers_to_questions = get_answers_to_questions()

    questions = get_conv_questions()

    # Threshold for skipping a topic when too many questions have been answered wrongly

    print("Convergence Module:")
    for i in range(100):
      for n, g in questions:
        if calc_threshold(-1, n):
          continue
        print(get_answers())
        random_topic_question = get_next_question(g)
        generated_answer = random_topic_question["answer"].to_string(index=False)
        question = random_topic_question['question'].to_string(index=False)
        answer = get_question_answer(answers_to_questions, question)
        print(question)
        print("Topic:", n)
        print("Secret:", answer, '/', generated_answer)
        user_answer = input("Please give an answer:")
        give_answer(answer, generated_answer, user_answer, n)


def get_question_answer(answers_to_questions, question):
  return answers_to_questions[
    answers_to_questions["question"] == question][
    "answer"].to_string(index=False)


if __name__ == "__main__": main()
