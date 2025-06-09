import json
import pandas as pd
import re
from datetime import datetime


def load_json(filepath):
    with open(filepath, "r") as f:
        return json.load(f)


def normalize_employees(employees):
    normalized = []
    for emp in employees:
        full_name = f"{emp['first_name']} {emp['last_name']}".strip()
        years = emp.get("years_of_experience", 0)

        # Designation logic
        if years < 3:
            designation = "System Engineer"
        elif 3 <= years <= 5:
            designation = "Data Engineer"
        elif 5 < years <= 10:
            designation = "Senior Data Engineer"
        else:
            designation = "Lead"

        # Phone number cleaning
        phone_raw = emp.get("phone", "")
        phone = "Invalid Number" if 'x' in phone_raw.lower() else re.sub(r'\D', '', phone_raw)
        try:
            phone = int(phone)
        except:
            phone = "Invalid Number"

        # Normalize record
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
            "hire_date": datetime.now().strftime("%Y-%m-%d")  # Placeholder
        })
    return pd.DataFrame(normalized)


def save_to_csv(df, filepath):
    df.to_csv(filepath, index=False)
    print(f"Data saved to {filepath}")


if __name__ == "__main__":
    raw = load_json("employees.json")
    employees = raw if isinstance(raw, list) else raw.get("employees", [])
    df = normalize_employees(employees)
    save_to_csv(df, "normalized_employees.csv")


