import pandas as pd
from multiprocessing import Pool

# Load the fee structure CSV file
data_frame = pd.read_csv('fee_structure.csv')

# Function to find the most frequently occurring date
def find_most_frequent_date(dates_list):
    date_frequency = {}
    for date in dates_list:
        date_frequency[date] = date_frequency.get(date, 0) + 1
    return max(date_frequency, key=date_frequency.get)

# Function to process fee data for a specific student (linear approach)
def get_fee_data(student_id):
    # Normalize the student name and the 'Name' column for case and extra spaces
    student_id = student_id.strip().lower()
    data_frame['Name'] = data_frame['Name'].str.strip().str.lower()

    # Filter the data for the student
    student_info = data_frame[data_frame['Name'] == student_id]
    
    if student_info.empty:
        return f"Student {student_id} not found in the data."

    # Gather all fee submission dates
    fee_submission_dates = []
    for col in student_info.columns:
        if "Fee Submission Date" in col:
            fee_submission_dates.extend(student_info[col].dropna().tolist())

    if not fee_submission_dates:
        return f"No fee submission dates found for student {student_id}."

    # Get the most frequent fee submission date
    common_submission_date = find_most_frequent_date(fee_submission_dates)
    return f"Student: {student_id}\nFee Dates: {fee_submission_dates}\nMost Frequent Date: {common_submission_date}"

# Helper function to use parallel processing for a single student
def parallel_process_student(student_id):
    return get_fee_data(student_id)

# Function to retrieve fee data using parallel processing
def get_fee_data_parallel(student_id):
    with Pool(1) as pool:  # Using one process for simplicity
        result = pool.apply(parallel_process_student, args=(student_id,))
    return result

# Main execution
if __name__ == "__main__":
    student_id = input("Please enter the student's name: ")

    print("\n--- Linear Processing ---")
    linear_output = get_fee_data(student_id)
    print(linear_output)

    print("\n--- Parallel Processing ---")
    parallel_output = get_fee_data_parallel(student_id)
    print(parallel_output)
