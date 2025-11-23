# Luis Daniel Hernandez from CS210 class, group Copernicus, 11/20/2025
# Lab 5: Flashcard Quiz Application with File Handling and Exceptions


class Flashcard:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

def load_flashcards(filename):
    flashcards = []
    try:
        with open(filename, "r") as file:
            for line in file:
                if "|" in line:
                    question, answer = line.strip().split("|")
                    flashcards.append(Flashcard(question, answer))
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    return flashcards

def run_quiz(flashcards):
    score = 0

    for card in flashcards:
        print("\nQuestion:")
        print(card.question)

        attempts = 3
        while attempts > 0:
            user_answer = input("Your answer: ").strip()

            if user_answer.lower() == card.answer.lower():
                print("Correct!")
                score += 1
                break
            else:
                attempts -= 1
                if attempts > 0:
                    print(f"Wrong. Try again ({attempts} attempts left).")
                else:
                    print(f"Out of tries! The correct answer was: {card.answer}")

    print(f"\nYour final score: {score}/{len(flashcards)}")


def main():
    filename = "questions.txt"
    flashcards = load_flashcards(filename)

    if not flashcards:
        print("No questions loaded. Exiting.")
        return

    print("Flashcard Quiz — You get 3 tries per question!\n")
    run_quiz(flashcards)



if __name__ == "__main__":
    main()