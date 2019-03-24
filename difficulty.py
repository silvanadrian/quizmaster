import pandas as pd
from collections import Counter
from random import randint


# get most common item, in case of tie the first
def majority(lst):
  data = Counter(lst)
  return max(lst, key=data.get)


def main():
  questions = pd.read_csv("data/classified.csv",
                          encoding="utf-8", sep=",")

  answers_to_questions = pd.read_csv("data/question_answer.csv",
                                     encoding="utf-8", sep=";")
  answers_to_questions.columns = ['question', 'answer']

  questions = questions.groupby('question').filter(
      lambda x: x['factuality'].sum() < 1)
  questions = questions.groupby(['question', 'topic'], as_index=False)[
    'difficulty'].agg(majority)

  answered = {"Easy": False, "Medium": False, "Hard": False}

  for i in range(100):

    questions_to_answer = questions[questions['difficulty'] == "Easy"]
    if answered["Easy"] == True:
      questions_to_answer = questions[questions['difficulty'] == "Medium"]
    if answered["Medium"] == True:
      questions_to_answer = questions[questions['difficulty'] == "Hard"]


    random_topic_question = questions_to_answer.sample(n=1, replace=True,
                                             random_state=randint(0, 10000))

    print(random_topic_question["difficulty"])
    question = random_topic_question["question"].to_string(index=False)

    answer = answers_to_questions[
      answers_to_questions["question"].str.contains(question)][
      "answer"].to_string(index=False)

    print(question)
    print("Answer", answer)
    user_answer = input("Please give an answer:")


    true_answer = answer.strip().lower() == user_answer.strip().lower()
    if true_answer:
      if answered["Medium"] == True:
        answered["Hard"] = True
      if answered["Easy"] == True:
        answered["Medium"] = True
      if answered["Easy"] == False:
        answered["Easy"] = True



if __name__ == "__main__": main()
