# Main file for project (Flashcard Quiz App)

# Luis Daniel Hernandez from CS210 class, group Copernicus
# Lab 5: File Handling and Exceptions


import random



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
                    q, a = line.strip().split("|", 1)
                    flashcards.append(Flashcard(q, a))
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    return flashcards


def quiz_user(flashcards):
    if not flashcards:
        print("No flashcards loaded. Exiting quiz.")
        return

    score = 0
    random.shuffle(flashcards)  # Shuffle questions randomly

    for card in flashcards:
        print(f"Question: {card.question}")
        guesses = 0
        correct = False

        while guesses < 3 and not correct:
            user_answer = input(f"Your answer (guess {guesses+1}/3): ").strip()
            guesses += 1
            if user_answer.lower() == card.answer.lower():
                print("✅ Correct!\n")
                score += 1
                correct = True
            elif guesses < 3:
                print("❌ Incorrect. Try again.\n")
            else:
                print(f"❌ Wrong! The correct answer is: {card.answer}\n")

    print(f"Your final score: {score}/{len(flashcards)}")


def main():
    print("=== Flashcard Quiz App ===")
    filename = input("Enter the flashcard file name (e.g., questions.txt): ").strip()
    flashcards = load_flashcards(filename)
    quiz_user(flashcards)


if __name__ == "__main__":
    main()
