import os
import json
import re
from datetime import datetime

# Path to the inbox directory
inbox_path = "/Users/macbook/Desktop/jamieAI/data/inbox"
jamie_threshold = 3  # Minimum number of Jamie's messages required per thread
total_message_threshold = 5  # Minimum total messages in a thread
jamie_percentage_threshold = 0.25  # Minimum percentage of Jamie's messages in a thread
max_messages_per_thread = 7  # Maximum number of messages allowed in a thread

def parse_timestamp(ts):
    """Convert timestamp in milliseconds to datetime."""
    return datetime.fromtimestamp(ts / 1000.0)

def determine_threshold(prev_message, current_message):
    """Determine the time threshold for conversation separation."""
    time_diff = (current_message['timestamp_ms'] - prev_message['timestamp_ms']) / 60000
    if time_diff < 30:
        return 30
    elif time_diff < 1440:
        return 1440
    else:
        return 2880  # 48 hours

def clean_text(text):
    """Clean up text by encoding to ASCII, removing non-ASCII characters, and replacing newline and tab characters."""
    text = text.replace('\n', ' ').replace('\t', ' ').replace('\\', ' ')
    ascii_encoded = text.encode('ascii', errors='ignore')
    cleaned_text = ascii_encoded.strip().decode('ascii')
    return cleaned_text

def remove_invalid_messages(messages):
    """Remove messages based on specific criteria."""
    valid_messages = []
    url_pattern = re.compile(r'https?://\S+')
    excluded_phrases = ["reacted", "shared a link", "mentioned you", "poll", "you missed a", "the video call ended.",
                        "you started a video call.", "you changed the", "to the group", "from the group", "as a group admin",
                        "member approval", "named the group", "nickname for", "you joined the video call.",
                        "you joined the", "you called", "called you", "missed your call.", "missed your",
                        "you can now message and call each other and see info like active status and when you've read messages."]
    emoji_pattern = re.compile(r'\\u\w{4}')
    
    for message in messages:
        content = message.get('content', '').lower()
        if 'share' not in message and not any(phrase in content for phrase in excluded_phrases) and not url_pattern.search(content):
            cleaned_content = emoji_pattern.sub('', content)
            if cleaned_content.strip():
                message.pop('reactions', None)
                message['content'] = clean_text(cleaned_content)
                valid_messages.append(message)
    return valid_messages

def contains_excluded_words(thread, excluded_words):
    """Check if any message in the thread contains excluded words."""
    for message in thread:
        content = message['content'].lower()
        if any(word.lower() in content for word in excluded_words):
            return True
    return False

def create_conversation_threads(messages, excluded_words):
    """Create threads based on the timestamps, Jamie's involvement, and content length."""
    threads = []
    current_thread = []
    jamie_messages_count = 0
    prev_message = None

    for message in sorted(messages, key=lambda x: x['timestamp_ms']):
        if not current_thread:
            current_thread.append(message)
            if message['sender_name'] == "Jamie Hughes":
                jamie_messages_count += 1
        else:
            threshold = determine_threshold(prev_message, message)
            if (message['timestamp_ms'] - prev_message['timestamp_ms']) / 60000 < threshold:
                if len(current_thread) < max_messages_per_thread:
                    current_thread.append(message)
                    if message['sender_name'] == "Jamie Hughes":
                        jamie_messages_count += 1
                else:
                    if jamie_messages_count >= jamie_threshold and jamie_messages_count / len(current_thread) >= jamie_percentage_threshold and not contains_excluded_words(current_thread, excluded_words):
                        threads.append(current_thread)
                    current_thread = [message]
                    jamie_messages_count = 1 if message['sender_name'] == "Jamie Hughes" else 0
            else:
                if len(current_thread) >= total_message_threshold and jamie_messages_count >= jamie_threshold and jamie_messages_count / len(current_thread) >= jamie_percentage_threshold and not contains_excluded_words(current_thread, excluded_words):
                    threads.append(current_thread)
                current_thread = [message]
                jamie_messages_count = 1 if message['sender_name'] == "Jamie Hughes" else 0
        prev_message = message

    if current_thread and len(current_thread) >= total_message_threshold and jamie_messages_count >= jamie_threshold and jamie_messages_count / len(current_thread) >= jamie_percentage_threshold and not contains_excluded_words(current_thread, excluded_words):
        threads.append(current_thread)
    return threads

def process_conversations(excluded_words):
    dataset = []
    for folder in os.listdir(inbox_path):
        folder_path = os.path.join(inbox_path, folder)
        if os.path.isdir(folder_path):
            for file_name in os.listdir(folder_path):
                if file_name.endswith('.json'):
                    file_path = os.path.join(folder_path, file_name)
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        if any(participant['name'] == 'Jamie Hughes' for participant in data['participants']):
                            messages = remove_invalid_messages(data['messages'])
                            threads = create_conversation_threads(messages, excluded_words)
                            for thread in threads:
                                first_message = thread[0]['content']
                                output = ""
                                for message in thread[1:]:  # Start from the second message
                                    output += f"{message['sender_name']}: {message['content']}\n"
                                dataset.append({
                                    "instruction": "Based on the context of the following conversation thread, provide a response from Jamie Hughes.",
                                    "input": first_message,
                                    "output": output.strip()
                                })
                            print(f"Processed {file_path}: {len(threads)} conversation threads found.")

    # Save the dataset to a JSON file
    with open('/Users/macbook/Desktop/jamieAI/dataset.json', 'w') as dataset_file:
        json.dump(dataset, dataset_file, indent=4)

# Example usage
excluded_words = [""]
process_conversations(excluded_words)
