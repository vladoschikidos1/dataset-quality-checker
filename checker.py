def validate_record(record):
    if not isinstance(record.get("request_id"), str) or not record.get("request_id").strip():
        raise ValueError("Request ID is required")
    if not isinstance(record.get("user"), str) or not record.get("user").strip():
        raise ValueError("User is required")
    if not isinstance(record.get("model"), str) or not record.get("model").strip():
        raise ValueError("Model is required")
    if not isinstance(record.get("prompt"), str) or not record.get("prompt").strip():
        raise ValueError("Prompt is required")


    clean_request_id = record.get("request_id").strip()
    clean_user = record.get("user").strip()
    clean_model = record.get("model").strip()
    prompt = record.get("prompt").strip().split()
    clean_prompt = " ".join(prompt)
    try:
        max_tokens = int(record.get("max_tokens"))
    except (ValueError, TypeError):
        raise ValueError("Max_tokens must be a positive integer")
    if max_tokens <= 0:
        raise ValueError("Max_tokens must be a positive integer")

    word_count = len(prompt)

    return_dict = {
        "request_id": clean_request_id,
        "user": clean_user,
        "model": clean_model,
        "prompt": clean_prompt,
        "max_tokens": max_tokens,
        "word_count": word_count
    }
    return return_dict
def check_records(records):
    accepted_records = []
    errors_records = []
    accepted_requests = set()

    for record_number, record in enumerate(records, start= 1):
        try:
           clean_return = validate_record(record)
           if clean_return.get("request_id") in accepted_requests:
               raise ValueError("Duplicate request ID")
           else:
               accepted_records.append(clean_return)
               accepted_requests.add(clean_return.get("request_id"))
        except ValueError as error:
            request_id = record.get("request_id")
            if isinstance(request_id, str):
                request_id = request_id.strip()
            else:
                request_id = ""
            error_record = {
                "record_number": record_number,
                "request_id": request_id,
                "error": str(error)
            }
            errors_records.append(error_record)
    total_max_tokens = 0
    models = set()
    for record in accepted_records:
        max_tokens = record.get("max_tokens")
        total_max_tokens += max_tokens
        model = record.get("model")
        models.add(model)
    report_dict = {
        "total_records": len(records),
        "valid_records": len(accepted_records),
        "rejected_records": len(errors_records),
        "total_tokens": total_max_tokens,
        "model": sorted(models),
        "errors": errors_records
    }
    summary_dict = {
        "cleaned_records": accepted_records,
        "report": report_dict
    }
    return summary_dict


if __name__ == "__main__":
    from file_tools import load_rows

    records = load_rows("requests.csv")
    result = check_records(records)
    print(result["report"])
