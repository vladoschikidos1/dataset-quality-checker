import pytest
from checker import validate_record, check_records

record_test = {
    "request_id": " R001 ",
    "user": " Vlad ",
    "model": " Model A ",
    "prompt": "  Explain   Python functions  ",
    "max_tokens": "1"
}
expected_dict = {
    "request_id": "R001",
    "user": "Vlad",
    "model": "Model A",
    "prompt": "Explain Python functions",
    "max_tokens": 1,
    "word_count": 3
}

def test_valid_records():
    return_dict = validate_record(record_test)
    assert return_dict == expected_dict

blank_prompt_record  = {
    "request_id": " R001 ",
    "user": " Vlad ",
    "model": " Model A ",
    "prompt": " ",
    "max_tokens": "1"
}
def test_blank_prompt():
    with pytest.raises(ValueError, match = "Prompt is required"):
        validate_record(blank_prompt_record)

@pytest.mark.parametrize(
    "invalid_tokens",
    [0, -5, "many"]
)

def test_invalid_tokens(invalid_tokens):
    test_record = record_test.copy()
    test_record["max_tokens"] = invalid_tokens
    with pytest.raises(ValueError, match="Max_tokens must be a positive integer"):
        validate_record(test_record)

records = [
    {
        "request_id": "R001",
        "user": "Vlad",
        "model": "Model A",
        "prompt": "   ",
        "max_tokens": "10"
    },
    {
        "request_id": "R001",
        "user": "Vlad",
        "model": "Model A",
        "prompt": "Explain JSON",
        "max_tokens": "20"
    },
    {
        "request_id": " R001 ",
        "user": "Vlad",
        "model": "Model A",
        "prompt": "Explain APIs",
        "max_tokens": "30"
    }
]
expected_duplicate_result = {
    "cleaned_records": [
        {
            "request_id": "R001",
            "user": "Vlad",
            "model": "Model A",
            "prompt": "Explain JSON",
            "max_tokens": 20,
            "word_count": 2
        }
    ],
    "report": {
        "total_records": 3,
        "valid_records": 1,
        "rejected_records": 2,
        "total_tokens": 20,
        "models": ["Model A"],
        "errors": [
            {
                "record_number": 1,
                "request_id": "R001",
                "error": "Prompt is required"
            },
            {
                "record_number": 3,
                "request_id": "R001",
                "error": "Duplicate request ID"
            }
        ]
    }
}
def test_duplicate_ids():
    summary_return = check_records(records)
    assert  summary_return == expected_duplicate_result

expected_empty_result = {
    "cleaned_records": [],
    "report": {
        "total_records": 0,
        "valid_records": 0,
        "rejected_records": 0,
        "total_tokens": 0,
        "models": [],
        "errors": []
    }
}
def test_empty_input():
    return_dict = check_records([])
    assert return_dict == expected_empty_result
