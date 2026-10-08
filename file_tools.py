import csv
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


if __name__ == "__main__":
    print(load_rows("requests.csv"))
    print(load_rows("headers_only.csv"))

