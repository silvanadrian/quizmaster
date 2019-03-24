import pandas as pd
from collections import Counter

#get most common item, in case of tie the first
def majority(lst):
  data = Counter(lst)
  return max(lst, key=data.get)

def main():
  questions = pd.read_csv("data/classified.csv",
                          encoding="utf-8", sep=",")

  answers_to_questions = pd.read_csv("data/question_answer.csv",
                                     encoding="utf-8", sep=";")
  answers_to_questions.columns = ['question', 'answer']

  print(questions['difficulty'])
  questions = questions.groupby('question').filter(
      lambda x: x['factuality'].sum() < 1)
  questions = questions.groupby(['question', 'topic'], as_index=False)['difficulty'].agg(majority)




  print(questions)





if __name__ == "__main__": main()