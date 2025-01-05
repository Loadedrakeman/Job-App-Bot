Dice Job Application Automation
This Python project automates the process of finding and applying to jobs on Dice. It uses Selenium to interact with the Dice website, navigate job listings, and submit applications for jobs with the "Easy Apply" option.

Features
Automatically logs in to your Dice account.
Searches for jobs based on a specified job title and location.
Filters results to only include jobs posted "Today."
Iterates through all job listings and submits applications for jobs with the "Easy Apply" option.
Handles pagination to process all pages of results.
Supports multiple locations for job searches (e.g., Seattle, Denver, Chicago, Washington, DC).
Skips external job listings and gracefully handles errors.
Requirements
Python 3.8 or higher
Chrome browser
ChromeDriver compatible with your Chrome version
Required Python libraries:
selenium
Setup
Clone the Repository

bash
Copy code
git clone https://github.com/yourusername/dice-job-automation.git
cd dice-job-automation
Install Dependencies Install the required Python packages using pip:

bash
Copy code
pip install selenium
Download ChromeDriver

Download the appropriate version of ChromeDriver from here.
Place the chromedriver executable in the project directory or a directory in your system's PATH.
Update Credentials

Open the script file and replace the placeholders for your email and password:
python
Copy code
email = "YOUR_EMAIL"
password = "YOUR_PASSWORD"
Update ChromeDriver Path

Set the correct path to the ChromeDriver executable in this line:
python
Copy code
chrome_service = Service("PATH_TO_YOUR_CHROMEDRIVER")
How to Use
Run the Script Execute the script to start the automation:

bash
Copy code
python dice_login.py
Monitor the Logs

The script will output logs for each job listing, including whether it applied or skipped the job.
It will also handle pagination and switch locations once all pages of results are processed.
Customizing Search

To change the job title, modify this line in the script:
python
Copy code
job_title = "data"
Add or remove locations in this list:
python
Copy code
locations = ["Seattle", "Denver", "Chicago", "Washington, DC"]
How It Works
Login:
Logs into your Dice account using your credentials.
Search:
Searches for jobs based on the provided title and location.
Filters results to include only jobs posted today.
Process Jobs:
Iterates through job listings on the current page.
If a job has an "Easy Apply" button, it submits the application.
Skips jobs with "Apply Now" or external websites.
Pagination:
Clicks the "Next" button to load the next page of results.
Continues until no more pages are left, then switches to the next location.
Repeat:
Processes all specified locations.
Error Handling
External Listings: Automatically skips job listings that redirect to external websites.
Button Not Found: Skips jobs where the "Easy Apply" button is not detected.
Interception Errors: Uses JavaScript-based interaction to bypass click interception issues.
Pagination Failures: Skips to the next location if no valid pagination button is found.
Future Enhancements
Support for other job platforms (e.g., LinkedIn, Monster).
Adding functionality to customize filters beyond "Today."
Improved UI or CLI for user interaction.
Saving logs to a file for better tracking.
Contributing
Contributions are welcome! If you encounter any issues or have ideas for improvements:

Fork this repository.
Create a new branch for your feature or bugfix.
Submit a pull request with a detailed description.
License
This project is licensed under the MIT License.

Disclaimer
This project is for educational and personal use only. Automating interactions with websites may violate their terms of service. Use at your own risk.
