# Employee scraper
<br>

User Story: <br>

Title: Scraping Employee Data from API
<br>
<br>

As a developer,
I want to scrape employee data from the provided API endpoint (https://api.slingacademy.com/v1/sample-data/files/employees.json),
so that I can ingest the data into our data warehouse for further analysis.
<br>

```Acceptance Criteria:``` <br>
 
### Data Retrieval:

The scraper must make a successful HTTP request to the provided URL: https://api.slingacademy.com/v1/sample-data/files/employees.json.
The request must return a valid JSON response with employee data.
<br>
### Data Structure Validation:

The scraper must parse the JSON data into the appropriate fields, including (but not limited to):
Employee ID <br>
First Name <br>
Last Name <br>
Email <br>
Job Title  <br>
Phone Number  <br>
Hire Date <br>
<br> 
Each field should be properly extracted and mapped to the respective schema for ingestion.
<br>
### Error Handling:

If the API returns a non-200 status code, the scraper should log the error with the appropriate error message.
The scraper should handle any timeout errors or failed connections gracefully and retry the request a limited number of times before logging a failure.
<br>

### Data Normalization:

1.Create a new column called "designation" and if years_of_experience is less than 3 then make the value as system engineer and more than 3-5 will be considered as 
   data engineer and it's between 5-10 it will be senior data engineer and if it's more than 10+ years then it will be lead. <br>
2. combine both the columns first name and last name as a new column called "Full name".  <br> 
3. Inside the column "phone" if it value contains 'x' then it needs to consider as "Invalid Number".  <br>
4. Make sure all the columns data types are as follows  <br>
Full Name-           string  <br>
email-               string  <br> 
phone-               int   <br> 
gender-              string  <br> 
age-                 int <br>
job_title-           string <br>
years_of_experience  int  <br>
salary               int  <br>
department           string  <br> 
5.Currency Conversion (Optional): If salary data is in a different currency, include a mechanism to convert it to the desired currency (using an external currency exchange API). <br>
6.Date Formatting: Ensure that all date fields, such as "Hire Date," are in a consistent format (e.g., YYYY-MM-DD). <br> 

<br>

### Test Cases:
Test Case 1: Verify JSON File Download  <br>
Test Case 2: Verify JSON File Extraction  <br>
Test Case 3: Validate File Type and Format <br> 
Test Case 4: Validate Data Structure <br>
Test Case 5: Handle Missing or Invalid Data <br>
