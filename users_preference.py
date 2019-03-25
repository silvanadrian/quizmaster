import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', -1)

def main():

  questions = pd.read_csv("data/classified.csv",
                          encoding="utf-8", sep=",")

  userid = input("Plase input userid:\n")
  user_questions = questions[questions['id'] == int(userid)]

  user_questions = user_questions.groupby('topic')['opinion'].mean()
  user_preferance =user_questions.idxmax()
  print(user_preferance)
  questions = questions[questions['topic'] == user_preferance]

  for index, row in questions.iterrows():
    print(row['question'])
    input("press for next question")


if __name__ == "__main__": main()