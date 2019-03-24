import pandas as pd
from scipy.stats import pearsonr


def takeCorrelation(elem):
  return elem[1]


def main():

  questions = pd.read_csv("data/classified.csv",
                          encoding="utf-8", sep=",")

  friends = []
  type = input("Which friend recommending method? topic? features?")
  if type == "topic":
    print("Topic based recommendation:")
    user_id = input("Please input your user id:")
    cutoff_k = input("Cutoff k:")

    user_features = questions[questions['id'] == int(user_id)].groupby(['topic'])['opinion'].mean()
    questions = questions.groupby(['id'])

    for n, g in questions:
      if n == int(user_id):
        continue
      # when classification not works properly then some users have only 4 topics
      if len(g.groupby(['topic'])['opinion'].mean()) < 5:
        continue
      corr, p_value = pearsonr(user_features, g.groupby(['topic'])['opinion'].mean())
      friends.append((n, corr))

    friends.sort(key=takeCorrelation,reverse=True)
    for friend in friends[:int(cutoff_k)]:
      print(friend)

  else:
    print("Feature based recommendation")
    




if __name__ == "__main__": main()