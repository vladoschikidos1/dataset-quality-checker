import csv
import json
from pathlib import Path

def load_rows(filename):
    script_path = Path(__file__).resolve()
    folder_path = script_path.parent
    input_path = folder_path / "data" / filename

    try:
        with open(input_path, "r", newline= "", encoding= "utf-8") as file:
            reader = csv.DictReader(file)
            required_columns = ["request_id", "user", "model", "prompt", "max_tokens"]
            current_columns = reader.fieldnames
            for column in required_columns:
                if column not in current_columns:
                    raise ValueError("Missing required columns")

            data_list = []
            for row in reader:
                request_id = row.get("request_id")
                user = row.get("user")
                model = row.get("model")
                prompt = row.get("prompt")
                max_tokens = row.get("max_tokens")

                data_dict = {
                    "request_id": request_id,
                    "user": user,
                    "model": model,
                    "prompt": prompt,
                    "max_tokens": max_tokens
                }
                data_list.append(data_dict)

            return data_list

    except FileNotFoundError:
        raise

def save_cleaned_records(records):
    script_path = Path(__file__).resolve()
    folder_path = script_path.parent
    output = folder_path / "output" / "cleaned_requests.csv"

    with open(output, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames= ["request_id", "user", "model", "prompt", "max_tokens", "word_count"])
        writer.writeheader()
        for record in records:
            writer.writerow(record)

    return output

def save_report(report):
    script_path = Path(__file__).resolve()
    folder_path = script_path.parent
    output = folder_path / "output" / "quality_report.json"

    with open(output, "w", encoding="utf-8") as file:
        json.dump(report, file, indent= 4)

    return output



if __name__ == "__main__":
    print(load_rows("requests.csv"))
    print(load_rows("headers_only.csv"))

