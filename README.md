
---

# TOPSIS Implementation in Python

**Author:** Saksham
**Roll No:** 102303157

This project is a Python implementation of the **TOPSIS (Technique for Order Preference by Similarity to Ideal Solution)** method used in multi-criteria decision making. It provides both a **command-line tool** and a **simple web service** to rank alternatives based on multiple criteria, weights, and impacts.

---

## What is TOPSIS?

TOPSIS is a decision-making technique that ranks alternatives by comparing their distance from an **ideal best solution** and an **ideal worst solution**.

The alternative closest to the ideal best and farthest from the ideal worst is ranked highest.

It is commonly used in:

* product selection
* performance evaluation
* decision analysis involving multiple criteria

---

## How the Method Works (Brief)

1. Read the decision matrix from a CSV file
2. Normalize the data so different criteria become comparable
3. Apply weights to each criterion
4. Determine the positive and negative ideal solutions based on impacts
5. Calculate Euclidean distance from both ideal solutions
6. Compute the TOPSIS score
7. Rank alternatives based on the score

---

## Project Structure

```
Topsis_Saksham_102303157/
├── topsis_saksham_102303157/   # Core TOPSIS logic (Python package)
├── topsis-web-service/         # Flask-based web service
│   └── app.py
├── data.csv                    # Sample input file
├── output-result.csv           # Sample output
├── setup.py
├── requirements.txt
└── README.md
```

---

## Input Format

The input CSV file should have:

* **First column:** alternative names
* **Remaining columns:** numeric criteria values

Example:

| Model | Price | Performance | Weight |
| ----- | ----- | ----------- | ------ |

Weights and impacts are provided separately:

* **Weights:** `1,2,3`
* **Impacts:** `+,-,+`

---
## Example
Input 
<img width="283" height="168" alt="image" src="https://github.com/user-attachments/assets/863ef29a-dc1b-4312-86d1-7740aca56377" />

output
<img width="963" height="395" alt="image" src="https://github.com/user-attachments/assets/8ed5a4b7-3763-4e1e-9fe2-085b6d9c281e" />



## Command Line Usage

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run TOPSIS

```bash
topsis data.csv "1,2,3" "+,-,+"
```

### Optional output file

```bash
topsis data.csv "1,2,3" "+,-,+" result.csv
```

The output file contains **TOPSIS scores** and **ranks** for each alternative.

---

## Web Service

The `topsis-web-service` folder contains a Flask application that exposes TOPSIS through an API.

Users can:

* upload a CSV file
* provide weights and impacts
* receive ranked results

This allows TOPSIS to be integrated into web or backend systems.

---

## Output

The final output includes:

* original input data
* calculated TOPSIS score
* rank of each alternative

A **higher score** indicates a **better alternative**.

---

## Validation

The implementation checks for:

* correct number of weights and impacts
* numeric criteria values
* valid impact symbols (`+` or `-`)
* proper CSV format

---

## Dependencies

* Python 3.x
* pandas
* numpy
* flask (for web service)

---

## Conclusion

This project provides a clean and practical implementation of the TOPSIS method with both CLI and web-based access. It is designed to be easy to use, readable, and suitable for real decision-making scenarios.

---

