import json
import pandas as pd
import re
from datetime import datetime

def load_json(filepath):
    """
    Loads JSON data from the given file path.

    Args:
        filepath (str): Path to the JSON file.

    Returns:
        dict or list: Parsed JSON data from the file.
    """
    with open(filepath, "r") as f:
        return json.load(f)


def normalize_employees(employees):
    """
    Processes and normalizes a list of employee records into a structured pandas DataFrame.

    Args:
        employees (list): List of employee dictionaries.

    Returns:
        pd.DataFrame: Normalized DataFrame with cleaned and enriched fields.
    """
    normalized = []

    for emp in employees:
        # Create full name by combining first and last name
        full_name = f"{emp['first_name']} {emp['last_name']}".strip()
        
        # Extract years of experience, defaulting to 0
        years = emp.get("years_of_experience", 0)

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
        try:
            phone = int(phone)
        except:
            phone = "Invalid Number"

        # Normalize and structure each employee record
        normalized.append({
            "Full Name": full_name,
            "email": str(emp.get("email", "")).strip(),
            "phone": phone,
            "gender": emp.get("gender", ""),
            "age": int(emp.get("age", 0)),
            "job_title": emp.get("job_title", ""),
            "years_of_experience": int(years),
            "salary": int(emp.get("salary", 0)),
            "department": emp.get("department", ""),
            "designation": designation,
            "hire_date": datetime.now().strftime("%Y-%m-%d")  # Using current date as placeholder
        })

    return pd.DataFrame(normalized)


def save_to_csv(df, filepath):
    """
    Saves a pandas DataFrame to a CSV file.

    Args:
        df (pd.DataFrame): DataFrame to save.
        filepath (str): Output CSV file path.
    """
    df.to_csv(filepath, index=False)
    print(f"Data saved to {filepath}")


if __name__ == "__main__":
    # Load raw employee data
    raw = load_json("employees.json")

    # Extract employees list whether top-level or nested
    employees = raw if isinstance(raw, list) else raw.get("employees", [])

    # Normalize the employee data into structured DataFrame
    df = normalize_employees(employees)

    # Save the normalized data to CSV
    save_to_csv(df, "normalized_employees.csv")
