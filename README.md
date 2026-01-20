TOPSIS Implementation in Python
Author: Saksham
Roll No: 102303157
This project is a Python implementation of the TOPSIS (Technique for Order Preference by Similarity to Ideal Solution) method used in multi-criteria decision making. It provides both a command-line tool and a simple web service to rank alternatives based on multiple criteria, weights, and impacts.
What is TOPSIS?
TOPSIS is a decision-making technique that ranks alternatives by comparing their distance from an ideal best solution and an ideal worst solution.
The alternative closest to the ideal best and farthest from the ideal worst is ranked highest.
It is commonly used in areas like product selection, performance evaluation, and decision analysis where multiple criteria are involved.
How the Method Works (Brief)
Read the decision matrix from a CSV file
Normalize the data so different criteria become comparable
Apply weights to each criterion
Determine the positive and negative ideal solutions based on impacts
Calculate Euclidean distance from both ideal solutions
Compute the TOPSIS score
Rank alternatives based on the score
Project Structure
Topsis_Saksham_102303157/
├── topsis_saksham_102303157/   # Core TOPSIS logic (Python package)
├── topsis-web-service/         # Flask-based web service
│   └── app.py
├── data.csv                    # Sample input file
├── output-result.csv           # Sample output
├── setup.py
├── requirements.txt
└── README.md
Input Format
The input CSV file should have:
First column: alternative names
Remaining columns: numeric criteria values
Example:
Model	Price	Performance	Weight
Weights and impacts are provided separately:
Weights: 1,2,3
Impacts: +,-,+
Command Line Usage
Install dependencies:
pip install -r requirements.txt
Run TOPSIS:
topsis data.csv "1,2,3" "+,-,+"
Optional output file:
topsis data.csv "1,2,3" "+,-,+" result.csv
The output file contains TOPSIS scores and ranks for each alternative.
Web Service
The topsis-web-service folder contains a Flask application that exposes TOPSIS through an API.
Users can upload a CSV file along with weights and impacts and receive ranked results.
This is useful for integrating TOPSIS into web or backend systems.
Output
The final output includes:
Original data
Calculated TOPSIS score
Rank of each alternative
Higher score indicates a better alternative.
Validation
The implementation checks for:
Correct number of weights and impacts
Numeric criteria values
Valid impact symbols (+ or -)
Proper CSV format
Dependencies
Python 3.x
pandas
numpy
flask (for web service)
Conclusion
This project provides a simple and practical implementation of the TOPSIS method with both CLI and web-based access. It is designed to be easy to use, readable, and suitable for real decision-making scenarios.
