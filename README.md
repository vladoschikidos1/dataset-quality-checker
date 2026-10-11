# Dataset Quality Checker

A Python program that checks a CSV file of AI request records, saves the valid records and explains why other records were rejected.

I built this to practise working with files, validating data, organising code into modules and writing tests. The included datasets contain made-up practice data.

## What it does

- Checks that all five required column names are present.
- Rejects blank request IDs, users, models and prompts.
- Converts `max_tokens` to an integer and rejects values of zero or less.
- Removes outside spaces and collapses repeated whitespace in prompts, while keeping capitalisation.
- Adds a word count to each accepted record.
- Rejects duplicate request IDs after trimming outside spaces.
- Produces a cleaned CSV and a JSON report.

The first valid record with an ID is kept. An invalid record does not reserve its ID. IDs are case-sensitive.

Only the first error in each rejected record is reported, and processing continues with the next record.

## Setup and running

Developed with Python 3.14. The application uses Python's standard library; `pytest` is needed for the tests.

Open a terminal in the project folder. On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install pytest
```

Keep the `data/` folder alongside the Python files, and make sure an `output/` folder exists.

Run the checker:

```bash
python main.py
```

By default, it reads `data/requests.csv`. To select another file in `data/`, change the call under the main guard in `main.py`, for example:

```python
main("headers_only.csv")
```

## Input

The CSV must have these columns. Their order can vary.

```csv
request_id,user,model,prompt,max_tokens
```

The supplied files are:

| File | Contents |
| --- | --- |
| `data/requests.csv` | 12 records, including intentional errors and a duplicate ID |
| `data/headers_only.csv` | All required headers, with no data records |
| `data/missing_columns.csv` | An example with missing required columns |

A missing file or missing required columns produces an error message.

## Output

| File | Contents |
| --- | --- |
| `output/cleaned_requests.csv` | Accepted records with the original five columns and an added `word_count` |
| `output/quality_report.json` | Record counts, total tokens from accepted records, sorted unique model names and rejection details |

Rejected records include their record number, request ID and error message. Record numbering starts at 1 after the CSV header.

Each run overwrites the output files. The input file is not changed.

For the supplied `requests.csv`, the summary is:

```text
Total records: 12
Valid records: 5
Rejected records: 7
Total tokens: 330
```

The program also prints the paths to both output files.

## Tests

Run from the project folder with the virtual environment active:

```bash
python -m pytest test_checker.py -q
```

Seven test cases cover valid-record cleaning, blank prompts, invalid token counts, duplicate IDs and an empty dataset.

## Code structure

| File | Responsibility |
| --- | --- |
| `file_tools.py` | Reads CSV input and writes the CSV and JSON outputs |
| `checker.py` | Validates records, handles duplicates and builds the report |
| `main.py` | Runs the workflow and displays the summary or a file-level error |
| `test_checker.py` | Tests the record-checking logic |