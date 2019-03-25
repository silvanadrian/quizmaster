import random

from convergence import calc_threshold
from convergence import get_answers_to_questions
from convergence import get_next_question
from convergence import get_questions
from convergence import give_answer
from convergence import get_question_answer


def decision(probability=0.9):
  return random.random() < probability


def polymath_user(probability):
  skipped = []
  answers_to_questions = get_answers_to_questions()
  questions = get_questions()


  while len(skipped) <= 4:
    for n,g in questions:
      if n not in skipped:
        if calc_threshold(0, n):
          skipped.append(n)
          continue
        question = get_next_question(g)
        answer_generated = question["answer"].to_string(index=False)
        question_string = question.to_string(index=False)

        answer = get_question_answer(answers_to_questions,question_string)
        # hope for the best that the answers are right or available
        if len(skipped) <= 4:
          if decision(probability):
            if not answer_generated:
              user_answer = answer
              give_answer(answer, answer_generated, user_answer, n)
            else:
              user_answer = answer_generated
              give_answer(answer, answer_generated, user_answer, n)
          else:
            give_answer(answer, answer_generated, "False Answer", n)
        if len(skipped) == 4:
          print("Topic:", n)


def topic_expert_user(probability, topic):
  skipped = []
  answers_to_questions = get_answers_to_questions()
  questions = get_questions()

  while len(skipped) <= 4:
    for n,g in questions:
      if n not in skipped:
        if calc_threshold(-1, n):
          skipped.append(n)
          continue
        question = get_next_question(g)
        answer_generated = question["answer"].to_string(index=False)
        question_string = question.to_string(index=False)

        answer = get_question_answer(answers_to_questions,question_string)
        # hope for the best that the answers are right or available
        if n == topic:
          if len(skipped) <= 4:
            if decision(probability):
              if not answer_generated:
                user_answer = answer
                give_answer(answer, answer_generated, user_answer, n)
              else:
                user_answer = answer_generated
                give_answer(answer, answer_generated, user_answer, n)
            else:
              give_answer(answer, answer_generated, "False Answer", n)
        else:
          give_answer(answer, answer_generated, "False Answer", n)
        if len(skipped) == 4:
          print("Topic:", n)
          break

def main():
  #polymath_user(0.7)
  topic_expert_user(0.8, "music")

if __name__ == "__main__": main()