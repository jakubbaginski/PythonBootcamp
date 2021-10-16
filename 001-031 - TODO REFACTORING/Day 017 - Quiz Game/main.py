from question_model import Question
from quiz_brain import QuizBrain
from data import new_data

questions = []
for item in new_data:
    questions.append(Question(item["question"], item["correct_answer"] == "True"))

brain = QuizBrain(questions.copy())

while brain.still_have_questions():
    brain.next_question()

print("\n\nYou have completed the quiz.")
print(f"Your final score is {brain.correct_answers:.0f}/{brain.question_number:.0f} 👍👍👍")
