
from database import create_database, save_message, get_messages

create_database()

save_message("test_chat", "user", "Hello, I am Saket")
save_message("test_chat", "assistant", "Hello Saket!")

messages = get_messages("test_chat")

for message in messages:
    print(message)
