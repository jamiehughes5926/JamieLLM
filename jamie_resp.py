import os
import json
from datetime import datetime

def find_json_files(root_dir, filename):
    """Recursively find all JSON files in the directory tree."""
    for root, dirs, files in os.walk(root_dir):
        if filename in files:
            yield os.path.join(root, filename)

def load_json_file(filepath):
    """Load a JSON file and return the content."""
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)

def format_timestamp(timestamp_str):
    """Pass through the timestamp string as it's already in formatted string form."""
    return timestamp_str

def extract_responses(conversations):
    """Extract responses where Jamie Hughes replies to a message or sends consecutive messages, including formatted timestamps."""
    responses = []
    for conversation in conversations:
        # Sort messages by timestamp to ensure correct ordering
        sorted_messages = sorted(conversation['messages'], key=lambda x: datetime.strptime(x['timestamp_ms'], '%Y-%m-%d %H:%M:%S'))
        previous_message = None
        for message in sorted_messages:
            if previous_message and previous_message['sender_name'] != "Jamie Hughes" and message['sender_name'] == "Jamie Hughes":
                response = {
                    'instruction': "The goal is to train a model to imitate Jamie Hughes' communication style. The input provided is a message that Jamie Hughes received, and the expected output is his corresponding response. Note that sometimes Jamie may send multiple responses to a single message, which should be captured accurately.",
                    'input': f"{previous_message['sender_name']}: {previous_message['content']}",
                    'output': f"Jamie Hughes: {message['content']} "
                }
                responses.append(response)
            elif previous_message and previous_message['sender_name'] == "Jamie Hughes" and message['sender_name'] == "Jamie Hughes":
                # Append to the last output if Jamie sends consecutive messages
                responses[-1]['output'] += f" | Jamie Hughes: {message['content']} "
            previous_message = message
            
    return responses



def process_conversations(json_files):
    """Process all JSON files to extract responses, including timestamp data."""
    all_responses = []
    for file in json_files:
        data = load_json_file(file)
        responses = extract_responses(data)
        all_responses.extend(responses)
    return all_responses

# Directory where the cleaned JSON files are stored
root_directory = '/Users/macbook/Desktop/jamieAI/scrap-data'

# JSON file containing cleaned conversations
json_files = list(find_json_files(root_directory, 'clean_conversations.json'))

# Process cleaned data to extract responses
responses = process_conversations(json_files)

# Output file path for storing responses
responses_path = '/Users/macbook/Desktop/jamieAI/scrap-data/jamie_responses.json'

# Save extracted responses to a new JSON file
with open(responses_path, 'w', encoding='utf-8') as file:
    json.dump(responses, file, indent=4)

print("Jamie Hughes' responses have been saved to:", responses_path)
