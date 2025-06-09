import unittest
import os
import pandas as pd
import employeescraper as es  


class TestEmployeeDataProcessing(unittest.TestCase):

# Test Cases:
# Test Case 1: Verify JSON File Download
# Test Case 2: Verify JSON File Extraction
# Test Case 3: Validate File Type and Format
# Test Case 4: Validate Data Structure
# Test Case 5: Handle Missing or Invalid Data

    @classmethod
    def setUpClass(cls):
        cls.raw_json = es.load_json("employees.json")
        cls.employees = cls.raw_json if isinstance(cls.raw_json, list) else cls.raw_json.get("employees", [])
        cls.df = es.normalize_employees(cls.employees)
        cls.output_file = "normalized_employees.csv"
        es.save_to_csv(cls.df, cls.output_file)

    def test_1_verify_json_download(self):
        """Test Case 1: Verify JSON File Download"""
        self.assertIsNotNone(self.raw_json)
        self.assertGreater(len(self.employees), 0, "Employee data should not be empty")

    def test_2_verify_json_extraction(self):
        """Test Case 2: Verify JSON File Extraction"""
        required_keys = {"first_name", "last_name", "email", "job_title", "phone", "age", "years_of_experience"}
        sample = self.employees[0]
        self.assertTrue(required_keys.issubset(sample.keys()), "Missing expected keys in JSON")

    def test_3_validate_file_type_and_format(self):
        """Test Case 3: Validate File Type and Format"""
        self.assertTrue(os.path.exists(self.output_file), "CSV file was not created")
        self.assertTrue(self.output_file.endswith(".csv"))

        df = pd.read_csv(self.output_file)
        self.assertFalse(df.empty, "CSV file should not be empty")

    def test_4_validate_data_structure(self):
        """Test Case 4: Validate Data Structure"""
        expected_columns = [
            "Full Name", "email", "phone", "gender", "age", "job_title",
            "years_of_experience", "salary", "department", "designation", "hire_date"
        ]
        for col in expected_columns:
            self.assertIn(col, self.df.columns, f"Missing column: {col}")

    def test_5_handle_missing_or_invalid_data(self):
        """Test Case 5: Handle Missing or Invalid Data"""
      
        valid_phones = self.df["phone"].apply(lambda x: isinstance(x, int) or x == "Invalid Number")
        self.assertTrue(valid_phones.all(), "Phone field contains invalid values")

        # Data types check
        self.assertTrue(self.df["age"].apply(lambda x: isinstance(x, int)).all(), "Invalid age type")
        self.assertTrue(self.df["salary"].apply(lambda x: isinstance(x, int)).all(), "Invalid salary type")
        self.assertTrue(self.df["years_of_experience"].apply(lambda x: isinstance(x, int)).all(), "Invalid experience type")



unittest.main(argv=[''], exit=False, verbosity=2)
