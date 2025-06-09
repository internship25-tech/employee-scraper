import unittest
import os
import pandas as pd
import employeescraper as es  # Custom module containing employee data handling functions


class TestEmployeeDataProcessing(unittest.TestCase):
    """
    Test Suite for Employee Data Processing.
    
    This test suite validates the complete pipeline of:
    1. JSON file download and loading
    2. Data extraction and normalization
    3. File creation and format
    4. Dataframe structure and schema
    5. Data validation and error handling
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up resources for all tests (run once before all test cases).
        Loads and processes the employee data.
        """
        # Load JSON data
        cls.raw_json = es.load_json("employees.json")
        
        # Ensure we extract employee list even if nested under "employees" key
        cls.employees = cls.raw_json if isinstance(cls.raw_json, list) else cls.raw_json.get("employees", [])

        # Normalize the employee list into a pandas DataFrame
        cls.df = es.normalize_employees(cls.employees)

        # Save the DataFrame to a CSV file for further validation
        cls.output_file = "normalized_employees.csv"
        es.save_to_csv(cls.df, cls.output_file)

    def test_1_verify_json_download(self):
        """
        Test Case 1: Verify that the JSON file was successfully loaded.
        """
        self.assertIsNotNone(self.raw_json, "JSON data should not be None")
        self.assertGreater(len(self.employees), 0, "Employee data should not be empty")

    def test_2_verify_json_extraction(self):
        """
        Test Case 2: Ensure each employee record has required fields.
        """
        required_keys = {"first_name", "last_name", "email", "job_title", "phone", "age", "years_of_experience"}
        sample = self.employees[0]
        self.assertTrue(required_keys.issubset(sample.keys()), "Missing expected keys in JSON")

    def test_3_validate_file_type_and_format(self):
        """
        Test Case 3: Validate the output CSV file exists and has correct format.
        """
        self.assertTrue(os.path.exists(self.output_file), "CSV file was not created")
        self.assertTrue(self.output_file.endswith(".csv"), "Output file is not a CSV")

        df = pd.read_csv(self.output_file)
        self.assertFalse(df.empty, "CSV file should not be empty")

    def test_4_validate_data_structure(self):
        """
        Test Case 4: Check if the DataFrame has the expected column structure.
        """
        expected_columns = [
            "Full Name", "email", "phone", "gender", "age", "job_title",
            "years_of_experience", "salary", "department", "designation", "hire_date"
        ]
        for col in expected_columns:
            self.assertIn(col, self.df.columns, f"Missing column: {col}")

    def test_5_handle_missing_or_invalid_data(self):
        """
        Test Case 5: Validate that the data does not contain invalid types or values.
        """
        # Check that phone numbers are either valid integers or marked as 'Invalid Number'
        valid_phones = self.df["phone"].apply(lambda x: isinstance(x, int) or x == "Invalid Number")
        self.assertTrue(valid_phones.all(), "Phone field contains invalid values")

        # Validate data types for numeric fields
        self.assertTrue(self.df["age"].apply(lambda x: isinstance(x, int)).all(), "Invalid age type")
        self.assertTrue(self.df["salary"].apply(lambda x: isinstance(x, int)).all(), "Invalid salary type")
        self.assertTrue(self.df["years_of_experience"].apply(lambda x: isinstance(x, int)).all(), "Invalid experience type")


# Run the test suite
unittest.main(argv=[''], exit=False, verbosity=2)
