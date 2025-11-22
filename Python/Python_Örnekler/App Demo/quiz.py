class question:
    def __init__(self, prompt,choices, answer):
        self.prompt = prompt
        self.choices = choices
        self.answer = answer

q1 = "What is the capital of France?"
q2 = "What is 2 + 2?"
q3 = "What is the largest planet in our solar system?"
q4 = "Who wrote 'To Kill a Mockingbird'?"
q5 = "What is the chemical symbol for water?"

list_of_questions = [
    question(q1,["a) London","b) Berlin","c) Paris"], "c"),
    question(q2,["a) 3","b) 4","c) 5"], "b"),
    question(q3,["a) Earth","b) Jupiter","c) Saturn"], "b"),
    question(q4,["a) Harper Lee","b) Mark Twain","c) J.K. Rowling"], "a"),
    question(q5,["a) CO2","b) H2O","c) O2"], "b"),
]

class quiz:
    def __init__(self, questions):
        self.questions = questions
        self.score = 0
        self.question_index = 0

    def get_question(self):
        return self.questions[self.question_index]

    def display_question(self):
        question = self.get_question()
        print(question.prompt)
        for choice in question.choices:
            print(choice)
        answer = input("Your answer: ")
        self.check_answer(answer)
        self.question_index += 1
        self.load_next_question()

    def check_answer(self, answer):
        question = self.get_question()
        if answer == question.answer:
            self.score += 1
            print("Correct!")
        else:
            print(f"Wrong! The correct answer was: {question.answer}")

    def load_next_question(self):
        if self.question_index < len(self.questions):
            self.display_question()
        else:
            self.show_score()

    def show_score(self):
        print(f"Quiz finished! Your score: {self.score}/{len(self.questions)}")
quiz = quiz(list_of_questions)
quiz.load_next_question()
#--------------------------------