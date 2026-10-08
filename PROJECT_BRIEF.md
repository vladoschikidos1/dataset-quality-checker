# Stage 1 project: Dataset Quality Checker

## Purpose

Build a local Python program that checks a CSV dataset of AI request records. It should keep usable records, explain why other records were rejected, and save results that someone else can inspect.

This is a fixed project with four checkpoints. The supplied files are synthetic practice data. The finished program runs with `python main.py` from the project folder. Its data paths must also work when it is launched from another working directory.

## Supplied files

| File | Purpose |
| --- | --- |
| `data/requests.csv` | Main dataset: 12 records with intentional quality problems |
| `data/missing_columns.csv` | CSV missing required column names |
| `data/headers_only.csv` | Correct header with zero data records |
| `output/` | Destination for generated results |
| `.gitignore` | Excludes environments, caches, editor files and local credentials |

The required input columns are `request_id`, `user`, `model`, `prompt` and `max_tokens`. Column order may vary; additional columns may be ignored. The supplied files use valid CSV syntax. Validation focuses on column names, field values and duplicate request IDs.

## Program files

Create these as their checkpoints are introduced:

| File | Responsibility |
| --- | --- |
| `file_tools.py` | Read CSV data and write CSV/JSON output |
| `checker.py` | Clean records, apply validation rules and build the report |
| `main.py` | Connect the functions, print the result and handle file-level failures |
| `test_checker.py` | Five focused test functions for the checking logic |

Use Python's standard library for the application and pytest for its tests. Write a short `README.md` at the final checkpoint explaining how to run the application and tests.

## Data rules

Check the rules in the order below. Record only the first error found in a rejected record.

| Order | Rule | Error message |
| --- | --- | --- |
| 1 | `request_id` must be a nonblank string | `Request ID is required` |
| 2 | `user` must be a nonblank string | `User is required` |
| 3 | `model` must be a nonblank string | `Model is required` |
| 4 | `prompt` must be a nonblank string | `Prompt is required` |
| 5 | `max_tokens` must convert to an integer greater than zero | `max_tokens must be a positive integer` |
| 6 | The cleaned request ID must not already belong to an accepted record | `Duplicate request ID` |

Invalid records do not reserve their request IDs. Keep the first valid occurrence of an ID and reject later valid occurrences of that ID. IDs are compared after trimming outside spaces; comparison is case-sensitive.

For an accepted record:

- Strip outside spaces from the request ID, user and model.
- Remove outside spaces and collapse repeated whitespace in the prompt.
- Preserve capitalisation in all text fields.
- Store `max_tokens` as an integer.
- Add `word_count`, calculated from the words in the cleaned prompt.
- Preserve the original input order among accepted records.

An invalid record is added to the errors list; processing then continues with the next record.

## Required outputs

### `output/cleaned_requests.csv`

Write the accepted records with these columns, in this order:

`request_id,user,model,prompt,max_tokens,word_count`

Include a header even when there are no accepted records. Each run replaces this output file; the input file remains the source dataset.

### `output/quality_report.json`

Write a JSON object with:

| Key | Value |
| --- | --- |
| `total_records` | Number of input data records, excluding the header |
| `valid_records` | Number of accepted records |
| `rejected_records` | Number of rejected records |
| `total_tokens` | Sum of token counts from accepted records, including repeated values |
| `models` | Alphabetically sorted list of unique model names from accepted records |
| `errors` | List of rejected-record details, in input order |

Each item in `errors` must contain `record_number`, `request_id` and `error`. Record numbering starts at 1 for the first data record and excludes the header. Include the trimmed ID where available, or an empty string when it is blank.

For the supplied main dataset, the summary must contain:

```json
{
  "total_records": 12,
  "valid_records": 5,
  "rejected_records": 7,
  "total_tokens": 330,
  "models": ["Model A", "Model B", "Model C"]
}
```

The actual report must also include its seven error entries. Accepted request IDs should be R001, R002, R007, R008 and R010, in that order.

For an empty dataset, all four counts/totals are zero and `models` and `errors` are empty lists. The cleaned CSV contains only its header.

## Four checkpoints

### 1. Load the data

Create `file_tools.py` with `load_rows(filename)`.

The function locates `filename` inside the `data` folder next to `file_tools.py`, opens it as UTF-8 CSV using `newline=""`, checks the required column names, and returns a list of raw row dictionaries. Values remain strings at this checkpoint.

`csv.DictReader` exposes the column names through `reader.fieldnames`. If required columns are missing, raise `ValueError("Missing required columns")`. A missing file should raise `FileNotFoundError`. The caller will handle these failures later.

Checks: `requests.csv` returns 12 rows; `headers_only.csv` returns an empty list; `missing_columns.csv` raises the specified ValueError.

### 2. Check the records

Create `checker.py`. Implement `validate_record(record)` to validate and clean one record, raising `ValueError` for an invalid record. Then implement `check_records(records)` to process the list, check duplicate IDs, collect accepted records and produce the report.

Its result should be a dictionary with two keys: `cleaned_records` holds the accepted list, and `report` holds the report object described above. The checking functions operate on Python data; file reading and writing belong in `file_tools.py`.

### 3. Save and run

Add CSV and JSON writing functions to `file_tools.py`. Create `main.py` with `main(input_filename="requests.csv")` to load the chosen input, call the checker, save both output files and print a concise summary including the two output paths. This parameter lets you check the other supplied files without changing the processing logic.

Build paths from the script location. Catch file-level failures and missing-column errors at the entry point and show a clear message. Validate the input and complete checking before opening output files for writing. Use a main guard so importing a module does not run the complete application.

### 4. Verify and finish

Write five focused pytest test functions covering:

1. Cleaning a valid record, including the smallest valid token count of 1.
2. Rejecting a blank prompt.
3. Rejecting invalid token counts: `0`, `-5` and `"many"` (one parametrised function).
4. Duplicate handling: an invalid record does not reserve an ID, the first valid record with that ID is accepted, and a later valid duplicate is rejected.
5. An empty dataset produces an empty accepted list and a zero summary.

Run the application with the supplied input files and inspect the CSV and JSON results. Add the short README and commit the project to Git, with a meaningful commit after each completed checkpoint.

## Completion standard

The project is complete when the required outputs are correct, the checks pass, the input file is preserved, and you can explain how one accepted record and one rejected record travel through your program.

Write the implementation yourself. Lesson notes and documentation are allowed. When stuck, ask for a targeted hint and show the code you have tried. Feedback will distinguish independent work from work completed with guidance.

Improvements outside this brief can be recorded as future work; the four checkpoints define this project's finishing point.
