import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', -1)

def main():

  questions = get_users_questions()

  userid = input("Plase input userid:\n")
  user_questions = get_preferance_id(questions, userid)

  user_preferance = get_user_preferance(user_questions)
  print(user_preferance)
  questions = get_prefereance_filtered_qustions(questions, user_preferance)

  for index, row in questions.iterrows():
    print(row['question'])


def get_preferance_id(questions, userid):
  user_questions = questions[questions['id'] == int(userid)]
  return user_questions


def get_users_questions():
  questions = pd.read_csv("data/classified.csv",
                          encoding="utf-8", sep=",")
  return questions


def get_prefereance_filtered_qustions(questions, user_preferance):
  questions = questions[questions['topic'] == user_preferance]
  return questions


def get_user_preferance(user_questions):
  user_questions = user_questions.groupby('topic')['opinion'].mean()
  user_preferance = user_questions.idxmax()
  return user_preferance


if __name__ == "__main__": main()