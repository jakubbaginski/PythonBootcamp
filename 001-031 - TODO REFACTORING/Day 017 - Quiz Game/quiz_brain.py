import random


class QuizBrain:

    def __init__(self, questions):
        self.question_number = 0
        self.question_list = questions
        self.correct_answers = 0

    def still_have_questions(self):
        return len(self.question_list) > 0

    def get_next_question(self):
        try:
            result = self.question_list[random.SystemRandom().randint(0, len(self.question_list))-1]
            self.question_list.remove(result)
            self.question_number += 1
        except IndexError:
            result = None
        return result

    def check_answer(self, answer_key, correct_answer):
        if (answer_key in ['f', 'false'] and not correct_answer) or (answer_key in ['t', 'true'] and correct_answer):
            self.correct_answers += 1
            print("You got it right.")
        else:
            print("Wrong answer.")
        print(f"Correct answer was: {correct_answer}")
        return None

    def print_result(self):
        print(f"Your current score is: {self.correct_answers:.0f}/{self.question_number:.0f}")
        return None

    def next_question(self):
        result = self.get_next_question()
        if result is not None:
            answer_key = ""
            while answer_key.lower() not in ["f", "t", "false", "true"]:
                answer_key = input(f"\nQ.{self.question_number:.0f}: {result.text} [T]rue/[F]alse: ")
            self.check_answer(answer_key, result.answer)
            self.print_result()
        else:
            print("No questions found.")
        return None
