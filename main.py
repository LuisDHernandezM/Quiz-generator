# Main file for project (Flashcard Quiz App)

# Luis Daniel Hernandez from CS210 class, group Copernicus
# Lab 5: File Handling and Exceptions


import random
import openai # type: ignore
import os

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Flashcard:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

def generate_flashcards(topic, num_cards=5):
    """
    Use OpenAI API to generate a list of flashcards for a given topic.
    """
    flashcards = []
    prompt = f"Generate {num_cards} simple Q&A flashcards on the topic '{topic}'. Format each flashcard as 'Question?|Answer'."

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        text = response.choices[0].message.content.strip()
        for line in text.split("\n"):
            if "|" in line:
                q, a = line.split("|", 1)
                flashcards.append(Flashcard(q.strip(), a.strip()))
    except Exception as e:
        print("Error generating flashcards:", e)
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
    print("=== AI Flashcard Quiz App ===")
    topic = input("Enter a topic for the flashcards (e.g., 'Python programming'): ").strip()
    num = input("How many flashcards do you want? (default 5): ").strip()
    num = int(num) if num.isdigit() else 5

    flashcards = generate_flashcards(topic, num)
    quiz_user(flashcards)

if __name__ == "__main__":
    main()
