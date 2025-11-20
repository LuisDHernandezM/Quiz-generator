# Main file for project

# Luis Daniel Hernandez from CS210 class, group Copernicus
# Lab 5: File Handling and Exceptions

class Flashcard:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

flashcards = []

with open("questions.txt", "r") as file:
    for line in file:
        q, a = line.strip().split("|")
        flashcards.append(Flashcard(q, a))

score = 0

for card in flashcards:
    print(card.question)
    user_answer = input("Your answer: ")
    if user_answer.strip().lower() == card.answer.lower():
        print("Correct!\n")
        score += 1
    else:
        print(f"Wrong! The correct answer is: {card.answer}\n")

print(f"Your final score: {score}/{len(flashcards)}")