# Main file for project (Flashcard Quiz App)

# Luis Daniel Hernandez from CS210 class, group Copernicus
# Lab 5: File Handling and Exceptions

# Initialize OpenAI client
import random
from gpt4all import GPT4All # type: ignore

class Flashcard:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

def generate_flashcards(topic, num_cards=5):
    """
    Use GPT4All local model to generate flashcards.
    """
    flashcards = []

    # Load GPT4All model (make sure you have downloaded the .bin file)
    model = GPT4All("gpt4all-lora-quantized.bin")  # path to your local model

    prompt = f"Generate {num_cards} simple Q&A flashcards about '{topic}'. Format each flashcard as 'Question?|Answer'."

    response = model.generate(prompt)

    for line in response.split("\n"):
        if "|" in line:
            q, a = line.split("|", 1)
            flashcards.append(Flashcard(q.strip(), a.strip()))

    return flashcards

def quiz_user(flashcards):
    if not flashcards:
        print("No flashcards available. Exiting quiz.")
        return

    score = 0
    random.shuffle(flashcards)

    for card in flashcards:
        print(f"\nQuestion: {card.question}")
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

    print(f"\nYour final score: {score}/{len(flashcards)}")

def main():
    print("=== GPT4All Flashcard Quiz App ===")
    topic = input("Enter a topic for the flashcards (e.g., 'Python programming'): ").strip()
    num = input("How many flashcards do you want? (default 5): ").strip()
    num = int(num) if num.isdigit() else 5

    flashcards = generate_flashcards(topic, num)
    quiz_user(flashcards)

if __name__ == "__main__":
    main()

