from collections import defaultdict
import json

class TrainingDataValidator:
    
    def __init__(self, file_path):
        self.file_path = file_path
        self.format_errors = defaultdict(int)
        self.message_counter = 0

    def validate(self):
        """
        Taken from openapi site to check for errors
        """
        with open(self.file_path, 'r', encoding='utf-8') as f:
            dataset = [json.loads(line) for line in f]

        for ex in dataset:
            self.message_counter += 1
            if not isinstance(ex, dict):
                self.format_errors["data_type"] += 1
                continue

            messages = ex.get("messages", None)
            if not messages:
                self.format_errors["missing_messages_list"] += 1
                continue

            for message in messages:
                if "role" not in message or "content" not in message:
                    self.format_errors["message_missing_key"] += 1
                    

                if any(k not in ("role", "content", "name", "function_call") for k in message):
                    self.format_errors["message_unrecognized_key"] += 1

                if message.get("role", None) not in ("system", "user", "assistant", "function"):
                    self.format_errors["unrecognized_role"] += 1

                content = message.get("content", None)
                function_call = message.get("function_call", None)

                if (not content and not function_call) or not isinstance(content, str):
                    self.format_errors["missing_content"] += 1

            if not any(message.get("role", None) == "assistant" for message in messages):
                self.format_errors["example_missing_assistant_message"] += 1

        self.report_errors()

    def report_errors(self):
        if self.format_errors:
            print("Found errors:")
            for k, v in self.format_errors.items():
                print(f"{k}: {v}")
        else:
            print("No errors found")

        print(f"{self.message_counter} messages processed")
