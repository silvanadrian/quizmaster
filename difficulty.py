import pandas as pd
from collections import Counter
from random import randint

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', -1)


answered = {"Easy": False, "Medium": False, "Hard": False}

# get most common item, in case of tie the first
def majority(lst):
  data = Counter(lst)
  return max(lst, key=data.get)


def main():
  answers_to_questions, grouped_questions, questions = prepare_diff()

  for i in range(100):


    questions_to_answer = get_questions_to_answer(answered, grouped_questions)

    random_topic_question = sample_question(questions_to_answer)

    print("Difficulty:", random_topic_question["difficulty"].to_string(index=False))
    question = random_topic_question["question"].to_string(index=False)


    generated_answer = questions[questions['question'] == question]['answer'].to_string(index=False)

    answer = get_answers_to_questions_diff(answers_to_questions, question)

    print(question)
    print("Answer", answer, "/", generated_answer)
    user_answer = input("Please give an answer:")

    check_answer(answer, answered, generated_answer, user_answer)


def prepare_diff():
  questions = pd.read_csv("data/classified.csv",
                          encoding="utf-8", sep=",")
  answers_to_questions = pd.read_csv("data/question_answer.csv",
                                     encoding="utf-8", sep=";")
  answers_to_questions.columns = ['question', 'answer']
  questions = questions.groupby('question').filter(
      lambda x: x['factuality'].sum() < 1)
  grouped_questions = questions.groupby(['question', 'topic'], as_index=False)[
    'difficulty'].agg(majority)
  questions = questions.drop_duplicates(subset='question', keep="last")
  return answers_to_questions, grouped_questions, questions


def sample_question(questions_to_answer):
  return questions_to_answer.sample(n=1, replace=True,
                                    random_state=randint(0, 10000))


def check_answer(answer, answered, generated_answer, user_answer):
  true_answer2 = generated_answer.strip().lower() == user_answer.strip().lower()
  true_answer = answer.strip().lower() == user_answer.strip().lower()
  if (true_answer) or (true_answer2):
    if answered["Medium"] == True:
      answered["Hard"] = True
    if answered["Easy"] == True:
      answered["Medium"] = True
    if answered["Easy"] == False:
      answered["Easy"] = True


def get_answers_to_questions_diff(answers_to_questions, question):
  return answers_to_questions[
    answers_to_questions["question"] == question][
    "answer"].to_string(index=False)


def get_answered_diff():
  return answered


def get_questions_to_answer(answered, questions):
  questions_to_answer = questions[questions['difficulty'] == "Easy"]
  if answered["Easy"] == True:
    questions_to_answer = questions[questions['difficulty'] == "Medium"]
  if answered["Medium"] == True:
    questions_to_answer = questions[questions['difficulty'] == "Hard"]
  return questions_to_answer


if __name__ == "__main__": main()
