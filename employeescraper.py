import json
import pandas as pd
import re
from datetime import datetime

def load_json(filepath):
    """
    Loads JSON data from the given file path with error handling.

    Args:
        filepath (str): Path to the JSON file.

    Returns:
        dict or list: Parsed JSON data from the file.
    """
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:   # Handle file not found error
        # If the file does not exist, print an error message and return an empty dict
        print(f"Error: File {filepath} not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Failed to parse {filepath}. Invalid JSON format.")
        return {}


def normalize_employees(employees):
    normalized = []

    for emp in employees:
        try:
            # Create full name by combining first and last name
            full_name = f"{emp['first_name']} {emp['last_name']}".strip()

            # Extract years of experience
            years = int(emp.get("years_of_experience", 0))

            # Assign designation based on years of experience
            if years < 3:
                designation = "System Engineer"
            elif 3 <= years <= 5:
                designation = "Data Engineer"
            elif 5 < years <= 10:
                designation = "Senior Data Engineer"
            else:
                designation = "Lead"

            # Clean and validate phone number
            phone_raw = emp.get("phone", "")
            phone = "Invalid Number" if 'x' in phone_raw.lower() else re.sub(r'\D', '', phone_raw)

            phone = int(phone) if phone.isdigit() else "Invalid Number"

            normalized.append({
                "Full Name": full_name,
                "email": str(emp.get("email", '')).strip(),
                "phone": phone,
                "gender": emp.get("gender", ''),
                "age": int(emp.get("age", 0)),
                "job_title": emp.get("job_title", ''),
                "years_of_experience": int(years),
                "salary": int(emp.get("salary", 0)),
                "department": emp.get("department", ''),
                "designation": designation,
                "hire_date": datetime.now().strftime("%Y-%m-%d")  # Using current date as placeholder
           })

        except Exception as e:
            print(f"Error processing employee record {emp}. Exception: {e}")

    return pd.DataFrame(normalized)

def save_to_csv(df, filepath):
    try:
        df.to_csv(filepath, index=False)
        print(f"Data successfully saved to {filepath}")
    except Exception as e:
        print(f"Error while saving CSV: {e}")


if __name__ == "__main__":
    # Load raw employee data
    raw = load_json("employees.json")

    # Extract employees list whether top-level or nested
    employees = raw if isinstance(raw, list) else raw.get("employees", [])

    # Normalize the employee data into structured DataFrame
    df = normalize_employees(employees)
    import os

    def save_to_csv(df, filepath):
        """Save DataFrame to CSV with error handling if the file already exists."""
        try:
            if os.path.exists(filepath):
                print(f"Error: File {filepath} already exists.")
                return  # or raise FileExistsError(f"File {filepath} already exists.")
            
            df.to_csv(filepath, index=False)
            print(f"Data successfully saved to {filepath}")

        except Exception as e:
            print(f"Error while saving CSV: {e}")

    
    save_to_csv(df, "normalized_employees.csv") # Save the normalized data to CSV