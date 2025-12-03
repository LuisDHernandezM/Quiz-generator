# server.py
import socket
import threading
import os
from ai_flashcard import generate_flashcards, Flashcard, save_flashcards_to_file

HOST = "127.0.0.1"  # localhost
PORT = 5001      # port to listen on

# Load saved flashcards by topic if file exists
FLASHCARD_FILE = "ai_questions.txt"


def handle_client(conn, addr):
    print(f"Connected by {addr}")
    try:
        # Receive topic and number of cards
        data = conn.recv(1024).decode().strip()
        if not data:
            conn.close()
            return

        # Expected format: "topic|num_cards"
        if "|" in data:
            topic, num_str = data.split("|", 1)
            num_cards = int(num_str) if num_str.isdigit() else 5
        else:
            topic = data
            num_cards = 5

        # Check if saved flashcards exist
        flashcards = []
        if os.path.exists(FLASHCARD_FILE):
            with open(FLASHCARD_FILE, "r") as f:
                for line in f:
                    if "|" in line:
                        q, a = line.strip().split("|", 1)
                        flashcards.append(Flashcard(q, a))

        # Filter flashcards by topic keyword
        topic_cards = [f for f in flashcards if topic.lower() in f.question.lower()]
        if len(topic_cards) < num_cards:
            # Generate new flashcards if not enough
            new_cards = generate_flashcards(topic, num_cards - len(topic_cards))
            topic_cards.extend(new_cards)
            save_flashcards_to_file(topic_cards)  # update saved file

        # Send flashcards to client
        response = "\n".join(f"{f.question}|{f.answer}" for f in topic_cards[:num_cards])
        conn.sendall(response.encode())

    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    finally:
        conn.close()

    response = "\n".join(f"{f.question}|{f.answer}" for f in topic_cards[:num_cards])
    print(f"Sending flashcards for topic '{topic}':\n{response}")  # debug
    conn.sendall(response.encode())
    conn.close()


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Flashcard server running on {HOST}:{PORT}...")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()


if __name__ == "__main__":
    start_server()