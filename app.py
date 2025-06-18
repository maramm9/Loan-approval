from flask import Flask, render_template, redirect, url_for, request,flash, session
from metrics import get_model_metrics
from werkzeug.security import generate_password_hash, check_password_hash 
import pandas as pd
import numpy as np
import pickle


app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for sessions
model = pickle.load(open('model.pkl', 'rb'))


submitted_requests = []

users = {}

@app.route("/")
def home():
    if 'email' in session:
        return render_template("home.html", logged_in=True)
    return render_template("home.html")


requests_data = []
@app.route("/manage-request", methods=["GET", "POST"])
def manage_request():
    return render_template('requests.html', prediction=None, requests=submitted_requests)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        form = request.form
        gender = 1 if form['Gender'] == 'Male' else 0
        married = 1 if form['Married'] == 'Yes' else 0
        dependents = int(form['Dependents'])
        education = 0 if form['Education'] == 'Graduate' else 1
        self_employed = 1 if form['Self_Employed'] == 'Yes' else 0
        applicant_income = float(form['ApplicantIncome'])
        coapplicant_income = float(form['CoapplicantIncome'])
        loan_amount = float(form['LoanAmount'])
        loan_term = float(form['Loan_Amount_Term'])
        credit_history = float(form['Credit_History'])
        property_area = form['Property_Area']

        area = {
            "Urban": [1, 0, 0],
            "Rural": [0, 1, 0],
            "Semiurban": [0, 0, 1]
        }.get(property_area, [0, 0, 1])

        features = np.array([[gender, married, dependents, education, self_employed,
                            applicant_income, coapplicant_income, loan_amount,
                            loan_term, credit_history] + area])

        prediction = model.predict(features)[0]
        result = "Approved" if prediction == 1 else "Rejected"

        entry = {
            "Gender": form['Gender'],
            "Married": form['Married'],
            "Dependents": form['Dependents'],
            "Education": form['Education'],
            "Self_Employed": form['Self_Employed'],
            "ApplicantIncome": form['ApplicantIncome'],
            "LoanAmount": form['LoanAmount'],
            "Credit_History": form['Credit_History'],
            "Property_Area": form['Property_Area'],
            "prediction": result
        }
        submitted_requests.append(entry)

        return render_template('requests.html', 
                            prediction=result,
                            requests=submitted_requests)

    except Exception as e:
        error_message = f"Error in input data! {str(e)}"
        return render_template('requests.html', 
                            prediction=error_message,
                            requests=submitted_requests)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Please fill in all fields', 'error')
            return redirect(url_for('login'))
        
        if email not in users or not check_password_hash(users[email]['password'], password):
            flash('Invalid email or password', 'error')
            return redirect(url_for('login'))
        
        # Set session variables
        session['email'] = email
        session['logged_in'] = True  # Additional flag for easy checking
        
        flash('Logged in successfully!', 'success')
        return redirect(url_for('home'))
    
    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not email or not password or not confirm_password:
            flash('All fields are required!', 'error')
            return redirect(url_for('signup'))
        
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('signup'))
        
        if email in users:
            flash('Email already exists!', 'error')
            return redirect(url_for('signup'))
        
        users[email] = {
            'password': generate_password_hash(password),
            'authenticated': False
        }
        
        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template("signup.html")

@app.route("/logout", methods=["GET", "POST"])  
def logout():
    session.clear()
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('home'))

@app.route("/metrics")
def metrics_page():
    report = get_model_metrics()
    return render_template("metrics.html", report=report)



if __name__ == "__main__":
    app.run(debug=True)
