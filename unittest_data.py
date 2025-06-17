import unittest
from unittest.mock import patch, MagicMock
import os
import pandas as pd
import employeescraper as es


# Dummy data for testing
DUMMY_JSON = {
    "employees": [
        {
            "first_name": "Alice",
            "last_name": "Wonderland",
            "email": "alice@example.com",
            "job_title": "Developer",
            "phone": "555-123-8888",
            "age": 30,
            "years_of_experience": 5,
            "salary": 50000,
            "department": "Engineering"
        },
        {
            "first_name": "Bob",
            "last_name": "Builder",
            "email": "bob@example.com",
            "job_title": "Developer",
            "phone": "555-666-9999",
            "age": 35,
            "years_of_experience": 10,
            "salary": 70000,
            "department": "Engineering"
        }
    ]
}

DUMMY_DF = pd.DataFrame([
    {
        "Full Name": "Alice Wonderland",
        "email": "alice@example.com",
        "phone": 5551238888,
        "gender": "",
        "age": 30,
        "job_title": "Developer",
        "years_of_experience": 5,
        "salary": 50000,
        "department": "Engineering",
        "designation": "Data Engineer",
        "hire_date": "2025-06-16"
    },
    {
        "Full Name": "Bob Builder",
        "email": "bob@example.com",
        "phone": 5556669999,
        "gender": "",
        "age": 35,
        "job_title": "Developer",
        "years_of_experience": 10,
        "salary": 70000,
        "department": "Engineering",
        "designation": "Senior Data Engineer",
        "hire_date": "2025-06-16"
    }
])

class TestEmployeeDataProcessing(unittest.TestCase):
    """
    Test Suite for Employee Data Processing with Mocked Functions.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up resources for all tests with mocked functions.
        """
        patcher_json = patch('employeescraper.load_json', return_value=DUMMY_JSON)
        patcher_normalize = patch('employeescraper.normalize_employees', return_value=DUMMY_DF)
        patcher_save = patch('employeescraper.save_to_csv')
        patcher_exists = patch('os.path.exists', return_value=True)
        patcher_pd = patch('pandas.read_csv', return_value=DUMMY_DF.copy())    

        # Start patches
        cls.mock_load_json = patcher_json.start()
        cls.mock_normalize = patcher_normalize.start()
        cls.mock_save = patcher_save.start()
        cls.mock_exists = patcher_exists.start()
        cls.mock_pd = patcher_pd.start()

        # Now we can reuse this for subsequent tests
        cls.raw_json = es.load_json("employees.json")
        cls.employees = cls.raw_json['employees']

        cls.df = es.normalize_employees(cls.employees)
        es.save_to_csv(cls.df, "normalized_employees.csv")

        cls.output_file = "normalized_employees.csv"

    @classmethod
    def tearDownClass(cls):
        """
        Stop all patches after all tests.
        """
        cls.mock_load_json.stop()
        cls.mock_normalize.stop()
        cls.mock_save.stop()
        cls.mock_exists.stop()
        cls.mock_pd.stop()


    def test_1_verify_json_download(self):
        """
        Test if load_json was called and returned dummy data.
        """
        self.mock_load_json.assert_called_once()
        self.assertEqual(len(self.employees), 2)

    def test_2_verify_json_extraction(self):
        """
        Validate the structure of dummy data.
        """
        for emp in self.employees:
            self.assertIn("first_name", emp)
            self.assertIn("last_name", emp)
            self.assertIn("email", emp)

    def test_3_validate_file_creation(self):
        """
        Confirm save_to_csv was called with the dummy DataFrame.
        """
        self.mock_save.assert_called_once()
        call_args = self.mock_save.call_args[0]
        df_passed = call_args[0]
        self.assertEqual(len(df_passed), 2)
        self.assertEqual("Full Name", df_passed.columns[0])

    def test_4_validate_data_structure(self):
        """
        Check if the DataFrame structure is correct.
        """
        expected_columns = [
            "Full Name", "email", "phone", "gender", "age",
            "job_title", "years_of_experience", "salary",
            "department", "designation", "hire_date"
        ]
        for col in expected_columns:
            self.assertIn(col, self.df.columns)


    def test_5_handle_invalid_data(self):
        """
        Validate phone, age, salary, and experience data.
        """
        self.assertTrue(self.df["phone"].apply(lambda x: isinstance(x, int)).all())  
        self.assertTrue(self.df["age"].apply(lambda x: isinstance(x, int)).all())   
        self.assertTrue(self.df["salary"].apply(lambda x: isinstance(x, int)).all())   
        self.assertTrue(self.df["years_of_experience"].apply(lambda x: isinstance(x, int)).all()) 


# Run the test suite
if __name__ == '__main__':
    unittest.main(verbosity=2)
