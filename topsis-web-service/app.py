from flask import Flask, render_template, request, flash, redirect, url_for
import pandas as pd
import numpy as np
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import re
from werkzeug.utils import secure_filename

from dotenv import load_dotenv
load_dotenv()

EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
app.secret_key = os.getenv('SECRET_KEY')

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['RESULT_FOLDER'] = 'results'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create folders if they don't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULT_FOLDER'], exist_ok=True)

# Email configuration (Update with your email credentials)
    # Change this (use App Password for Gmail)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_inputs(df, weights, impacts):
    """Validate TOPSIS inputs"""
    errors = []
    
    # Check if file has at least 3 columns
    if len(df.columns) < 3:
        errors.append("Input file must contain at least three columns")
        return errors
    
    # Check if numeric columns contain only numeric values
    numeric_cols = df.iloc[:, 1:]
    for col in numeric_cols.columns:
        if not pd.api.types.is_numeric_dtype(numeric_cols[col]):
            try:
                pd.to_numeric(numeric_cols[col])
            except:
                errors.append(f"Column '{col}' contains non-numeric values")
                return errors
    
    # Parse weights
    try:
        weights_list = [float(w.strip()) for w in weights.split(',')]
    except ValueError:
        errors.append("Weights must be numeric values separated by commas")
        return errors
    
    # Parse impacts
    impacts_list = [i.strip() for i in impacts.split(',')]
    
    # Check if impacts are either +ve or -ve
    for impact in impacts_list:
        if impact not in ['+', '-']:
            errors.append("Impacts must be either '+' or '-'")
            return errors
    
    # Check if number of weights and impacts match
    if len(weights_list) != len(impacts_list):
        errors.append(f"Number of weights ({len(weights_list)}) must equal number of impacts ({len(impacts_list)})")
        return errors
    
    # Check if number matches columns
    num_numeric_cols = len(df.columns) - 1
    if len(weights_list) != num_numeric_cols:
        errors.append(f"Number of weights/impacts ({len(weights_list)}) must equal number of criteria columns ({num_numeric_cols})")
        return errors
    
    return errors

def normalize_matrix(df):
    """Normalize the decision matrix"""
    numeric_data = df.iloc[:, 1:].values
    root_sum_squares = np.sqrt(np.sum(numeric_data**2, axis=0))
    normalized = numeric_data / root_sum_squares
    return normalized

def calculate_weighted_matrix(normalized, weights):
    """Calculate weighted normalized decision matrix"""
    return normalized * weights

def find_ideal_solutions(weighted, impacts):
    """Find ideal best and ideal worst solutions"""
    ideal_best = []
    ideal_worst = []
    
    for i, impact in enumerate(impacts):
        if impact == '+':
            ideal_best.append(np.max(weighted[:, i]))
            ideal_worst.append(np.min(weighted[:, i]))
        else:
            ideal_best.append(np.min(weighted[:, i]))
            ideal_worst.append(np.max(weighted[:, i]))
    
    return np.array(ideal_best), np.array(ideal_worst)

def calculate_distances(weighted, ideal_best, ideal_worst):
    """Calculate Euclidean distances"""
    distance_best = np.sqrt(np.sum((weighted - ideal_best)**2, axis=1))
    distance_worst = np.sqrt(np.sum((weighted - ideal_worst)**2, axis=1))
    return distance_best, distance_worst

def calculate_topsis_score(distance_best, distance_worst):
    """Calculate TOPSIS score"""
    return distance_worst / (distance_best + distance_worst)

def calculate_rank(scores):
    """Calculate rank based on TOPSIS scores"""
    return pd.Series(scores).rank(ascending=False, method='min').astype(int)

def perform_topsis(input_file, weights, impacts, output_file):
    """Perform TOPSIS analysis"""
    # Read CSV
    df = pd.read_csv(input_file)
    
    # Validate
    errors = validate_inputs(df, weights, impacts)
    if errors:
        return False, errors
    
    # Parse weights and impacts
    weights_list = [float(w.strip()) for w in weights.split(',')]
    impacts_list = [i.strip() for i in impacts.split(',')]
    
    # Perform TOPSIS
    normalized = normalize_matrix(df)
    weighted = calculate_weighted_matrix(normalized, weights_list)
    ideal_best, ideal_worst = find_ideal_solutions(weighted, impacts_list)
    distance_best, distance_worst = calculate_distances(weighted, ideal_best, ideal_worst)
    topsis_scores = calculate_topsis_score(distance_best, distance_worst)
    ranks = calculate_rank(topsis_scores)
    
    # Create result dataframe
    result_df = df.copy()
    result_df['Topsis Score'] = topsis_scores.round(2)
    result_df['Rank'] = ranks
    
    # Save result
    result_df.to_csv(output_file, index=False)
    
    return True, "TOPSIS analysis completed successfully"

def send_email(recipient_email, result_file):
    """Send result file via email"""
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = recipient_email
        msg['Subject'] = 'TOPSIS Analysis Result'
        
        # Email body
        body = """
        Dear User,
        
        Your TOPSIS analysis has been completed successfully.
        
        Please find the result file attached.
        
        Best regards,
        TOPSIS Web Service
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach result file
        filename = os.path.basename(result_file)
        attachment = open(result_file, 'rb')
        
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename= {filename}')
        
        msg.attach(part)
        attachment.close()
        
        # Send email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_ADDRESS, recipient_email, text)
        server.quit()
        
        return True, "Email sent successfully"
    
    except Exception as e:
        return False, f"Failed to send email: {str(e)}"

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Handle TOPSIS analysis request"""
    try:
        # Get form data
        file = request.files.get('file')
        weights = request.form.get('weights', '').strip()
        impacts = request.form.get('impacts', '').strip()
        email = request.form.get('email', '').strip()
        
        # Validate inputs
        if not file:
            flash('Please upload a CSV file', 'error')
            return redirect(url_for('index'))
        
        if not weights:
            flash('Please enter weights', 'error')
            return redirect(url_for('index'))
        
        if not impacts:
            flash('Please enter impacts', 'error')
            return redirect(url_for('index'))
        
        if not email:
            flash('Please enter email address', 'error')
            return redirect(url_for('index'))
        
        # Validate email format
        if not validate_email(email):
            flash('Invalid email format', 'error')
            return redirect(url_for('index'))
        
        # Check file extension
        if not file.filename.endswith('.csv'):
            flash('Only CSV files are allowed', 'error')
            return redirect(url_for('index'))
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)
        
        # Generate output filename
        output_filename = f"result_{filename}"
        output_path = os.path.join(app.config['RESULT_FOLDER'], output_filename)
        
        # Perform TOPSIS
        success, message = perform_topsis(input_path, weights, impacts, output_path)
        
        if not success:
            for error in message:
                flash(error, 'error')
            # Clean up
            os.remove(input_path)
            return redirect(url_for('index'))
        
        # Send email
        email_success, email_message = send_email(email, output_path)
        
        # Clean up files
        os.remove(input_path)
        os.remove(output_path)
        
        if email_success:
            flash(f'TOPSIS analysis completed! Result sent to {email}', 'success')
        else:
            flash(f'Analysis completed but email failed: {email_message}', 'warning')
        
        return redirect(url_for('index'))
    
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)