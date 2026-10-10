from file_tools import load_rows
from file_tools import save_cleaned_records
from file_tools import save_report
from checker import check_records

def main(input_filename="requests.csv"):
    try:
        returned_list = load_rows(input_filename)
        report_summary = check_records(returned_list)
        report = report_summary["report"]
        output_path_records = save_cleaned_records(report_summary["cleaned_records"])
        output_path_report = save_report(report)
    except (FileNotFoundError, ValueError) as error:
        print(f"The program didn't success. Error: {error}")
        return


    print(f"Total records: {report.get("total_records")}")
    print(f"Valid records: {report.get("valid_records")}")
    print(f"Rejected records: {report.get("rejected_records")}")
    print(f"Total tokens: {report.get("total_tokens")}")
    print(f"Clean records path: {output_path_records}")
    print(f"Report path: {output_path_report}")

if __name__ == "__main__":
    main("requests.csv")
