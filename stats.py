import json

def load_data(file_path):
    """Load data from a JSON file."""
    with open(file_path, 'r') as file:
        return json.load(file)

def calculate_statistics(conversations):
    """Calculate various statistics from conversation data."""
    total_words = 0
    total_messages = 0
    messages_by_jamie = 0
    conversation_responses = 0

    # Count words, messages, and messages by Jamie
    for thread in conversations:
        jamie_in_thread = False
        for message in thread:
            total_messages += 1
            content = message.get('content', '')
            total_words += len(content.split())
            if message['sender_name'] == "Jamie Hughes":
                messages_by_jamie += 1
                jamie_in_thread = True
        # Count the thread as a conversation response if Jamie participated
        if jamie_in_thread:
            conversation_responses += 1

    print(f"Total words: {total_words}")
    print(f"Total messages: {total_messages}")
    print(f"Conversation responses involving Jamie Hughes: {conversation_responses}")
    print(f"Messages sent by Jamie Hughes: {messages_by_jamie}")

def main():
    # Load conversation threads
    conversations = load_data('/Users/macbook/Desktop/jamieAI/v2/all_conversations.json')
    
    # Calculate and print statistics
    calculate_statistics(conversations)

if __name__ == "__main__":
    main()
