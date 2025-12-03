# client.py
import socket
import random
from ai_flashcard import Flashcard, quiz_user

HOST = "127.0.0.1"
PORT = 5001

def get_flashcards_from_server(topic, num_cards=5):
    flashcards = []
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(f"{topic}|{num_cards}".encode())
        s.shutdown(socket.SHUT_WR)  # signal done sending

        data = b""
        while True:
            part = s.recv(1024)
            if not part:
                break
            data += part

    text = data.decode()
    for line in text.split("\n"):
        if "|" in line:
            q, a = line.strip().split("|", 1)
            flashcards.append(Flashcard(q.strip(), a.strip()))
    random.shuffle(flashcards)
    return flashcards


def main():
    print("=== Flashcard Quiz Client ===")
    topic = input("Enter a topic for the flashcards: ").strip()
    num = input("How many flashcards do you want? (default 5): ").strip()
    num = int(num) if num.isdigit() else 5

    flashcards = get_flashcards_from_server(topic, num)
    if not flashcards:
        print("No flashcards received from server. Exiting.")
        return

    quiz_user(flashcards)


if __name__ == "__main__":
    main()