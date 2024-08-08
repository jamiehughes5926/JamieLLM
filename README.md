# JamieLLM
# README

## Overview

This project aims to scrape Facebook Messenger messages to create a dataset that can be used to fine-tune a model to imitate Jamie Hughes' communication style. The code provided achieves this by finding, processing, and extracting relevant responses from the conversation threads.

## Prerequisites

- Python 3.x
- Required Python libraries: `os`, `json`, `datetime`, `re`

## Directory Structure

```
/Users/macbook/Desktop/jamieAI/
|-- data/
|   |-- inbox/
|       |-- [individual chat folders containing JSON files]
|-- scrap-data/
|   |-- clean_conversations.json
|   |-- jamie_responses.json
|-- dataset.json
|-- README.md
|-- script.py (the script file containing the code)
```

## How to Use

### Step 1: Organize Data

Ensure that your Facebook Messenger JSON files are located in the `/Users/macbook/Desktop/jamieAI/data/inbox/` directory. Each chat should be in its own folder within the `inbox` directory.

### Step 2: Run the Script

The script performs the following steps:

1. **Find JSON Files**: Recursively searches for JSON files named `clean_conversations.json` in the specified directory.
2. **Load JSON File**: Loads the content of each found JSON file.
3. **Extract Responses**: Processes each conversation to extract Jamie Hughes' responses along with the corresponding messages.
4. **Process Conversations**: Processes the extracted conversations to create a dataset of Jamie Hughes' communication style.
5. **Save Extracted Responses**: Saves the extracted responses to a JSON file named `jamie_responses.json`.
6. **Create Conversation Threads**: Creates conversation threads based on specific criteria such as timestamp, content length, and Jamie's involvement.
7. **Save Final Dataset**: Saves the final dataset to a JSON file named `dataset.json`.

### Running the Script

1. Ensure all the required Python libraries are installed.
2. Save the provided script to a file named `script.py`.
3. Open a terminal and navigate to the directory containing `script.py`.
4. Run the script using the command:
   ```sh
   python script.py
   ```

### Customization

You can customize the following parameters in the script to fit your specific needs:

- **Message Thresholds**:
  - `jamie_threshold`: Minimum number of Jamie's messages required per thread.
  - `total_message_threshold`: Minimum total messages in a thread.
  - `jamie_percentage_threshold`: Minimum percentage of Jamie's messages in a thread.
  - `max_messages_per_thread`: Maximum number of messages allowed in a thread.
  
- **Excluded Words and Phrases**:
  Modify the `excluded_words` list to exclude threads containing certain words or phrases.

### Output

The script generates two main output files:

1. `jamie_responses.json`: Contains the extracted responses where Jamie Hughes replies to a message or sends consecutive messages.
2. `dataset.json`: Contains the final dataset formatted for training a model to imitate Jamie Hughes' communication style.

### Example Output

An example of the format of entries in the `dataset.json`:

```json
[
    {
        "instruction": "Based on the context of the following conversation thread, provide a response from Jamie Hughes.",
        "input": "First message content...",
        "output": "Jamie Hughes: Response content..."
    },
    ...
]
```

## License

This project is licensed under the MIT License.

## Contact

For any questions or issues, please contact Jamie Hughes.

---

This README provides a comprehensive overview and instructions on how to use the provided script to process Facebook Messenger messages and create a dataset for fine-tuning a model to imitate Jamie Hughes' communication style.
