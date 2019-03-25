import random

from convergence import calc_threshold
from convergence import get_answers_to_questions
from convergence import get_next_question
from convergence import get_conv_questions
from convergence import give_answer
from convergence import get_question_answer
from classification import get_class_questions
from classification import get_class_question
from difficulty import prepare_diff, get_answered_diff, get_questions_to_answer, \
  sample_question, get_answers_to_questions_diff, check_answer


def decision(probability=0.9):
  return random.random() < probability


def polymath_user(probability):
  skipped = []
  answers_to_questions = get_answers_to_questions()
  questions = get_conv_questions()
  not_finished = True
  amount_of_questions = 0

  while not_finished:
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
          amount_of_questions += 1
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
          print("Amount of questions answered:", amount_of_questions)
          print("Finished topic was:", n)
          not_finished = False


def topic_expert_user(probability, topic):
  skipped = []
  answers_to_questions = get_answers_to_questions()
  questions = get_conv_questions()
  not_finished = True
  amount_of_questions = 0

  while not_finished:
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
              amount_of_questions +=1
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
          print("Amount of questions answered:", amount_of_questions)
          print("Finished Topic was:", n)
          not_finished = False

def classification():
  questions = get_class_questions()
  filtered_questions = get_class_question("Easy", questions, "music")

  for index, row in filtered_questions.iterrows():
    print(row['question'])


def diffuculty_user(probability):
  answers_to_questions, grouped_questions, questions = prepare_diff()

  answered = get_answered_diff()

  not_finished = True

  while not_finished:
    questions_to_answer = get_questions_to_answer(answered, grouped_questions)

    random_topic_question = sample_question(questions_to_answer)

    print("Difficulty:", random_topic_question["difficulty"].to_string(index=False))
    question = random_topic_question["question"].to_string(index=False)


    generated_answer = questions[questions['question'] == question]['answer'].to_string(index=False)

    answer = get_answers_to_questions_diff(answers_to_questions, question)

    print(question)
    if decision(probability):
      if not generated_answer:
        user_answer = answer
        check_answer(answer, answered, generated_answer, user_answer)
      else:
        user_answer = generated_answer
        check_answer(answer, answered, generated_answer, user_answer)
    else:
      check_answer(answer, answered, generated_answer, "Wrong!!!")
    answered = get_answered_diff()
    if answered["Hard"] == True:
      print("Finished arrived at hard questions")
      not_finished = False




def main():
  # Classification
  classification()
  print("\n\n")
  # Convergence
  polymath_user(0.5)
  topic_expert_user(0.8, "music")
  print("\n\n")
  # Difficulty
  diffuculty_user(0.5)

if __name__ == "__main__": main()