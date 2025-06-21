from flask import Blueprint, render_template, redirect, url_for, request, flash, session,jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import numpy as np
import pickle
from datetime import datetime
from app import db
from app.models import User, LoanRequest
import json

main_bp = Blueprint('main', __name__)
model = pickle.load(open('logistic_regression_model.pkl', 'rb'))

@main_bp.route("/")
def home():
    if 'email' in session:
        return render_template("home.html", logged_in=True)
    return render_template("home.html")

@main_bp.route("/manage-request", methods=["GET", "POST"])
def manage_request():
    if 'email' not in session:
        return redirect(url_for('main.login'))
    
    user = User.query.filter_by(email=session['email']).first()
    requests = LoanRequest.query.filter_by(user_id=user.id).all()
    return render_template('requests.html', prediction=None, requests=requests)

@main_bp.route('/predict', methods=['POST'])
def predict():
    if 'email' not in session:
        return redirect(url_for('main.login'))
    
    try:
        form = request.form

        gender = 1 if form['Gender'] == 'Male' else 0
        married = 1 if form['Married'] == 'Yes' else 0
        dependents = int(form['Dependents'])
        education = 0 if form['Education'] == 'Graduate' else 1
        self_employed = 1 if form['Self_Employed'] == 'Yes' else 0
        credit_history = float(form['Credit_History'])
        
        area = {"Urban": 0, "Rural": 1, "Semiurban": 2}.get(form['Property_Area'], 2)
        
        total_income = float(form['ApplicantIncome']) + float(form['CoapplicantIncome'])
        log_total_income = np.log(total_income) if total_income > 0 else 0
        log_loan_amount = np.log(float(form['LoanAmount'])) if float(form['LoanAmount']) > 0 else 0
        log_loan_term = np.log(float(form['Loan_Amount_Term'])) if float(form['Loan_Amount_Term']) > 0 else 0

        features = np.array([[
            gender, married, dependents, education, self_employed,
            credit_history, area,
            log_total_income, log_loan_amount, log_loan_term
        ]])

        prediction = model.predict(features)[0]
        result = "Approved" if prediction == 1 else "Rejected"
        
        user = User.query.filter_by(email=session['email']).first()
        
        new_request = LoanRequest(
            user_id=user.id,
            gender=form['Gender'],
            married=form['Married'],
            dependents=form['Dependents'],
            education=form['Education'],
            self_employed=form['Self_Employed'],
            applicant_income=form['ApplicantIncome'],
            coapplicant_income=form['CoapplicantIncome'],
            loan_amount=form['LoanAmount'],
            loan_term=form['Loan_Amount_Term'],
            credit_history=form['Credit_History'],
            property_area=form['Property_Area'],
            prediction=result
        )
        db.session.add(new_request)
        db.session.commit()

        return render_template('requests.html', 
                            prediction=result,
                            requests=LoanRequest.query.filter_by(user_id=user.id).all())
    
    except Exception as e:
        return render_template('requests.html', 
                            prediction=f"Error: {str(e)}",
                            requests=[])

@main_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Please fill in all fields', 'error')
            return redirect(url_for('main.login'))
        
        user = User.query.filter_by(email=email).first()
        
        if not user or not check_password_hash(user.password, password):
            flash('Invalid email or password', 'error')
            return redirect(url_for('main.login'))
        
        session['email'] = email
        session['logged_in'] = True
        
        flash('Logged in successfully!', 'success')
        return redirect(url_for('main.home'))
    
    return render_template("login.html")

@main_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not email or not password or not confirm_password:
            flash('All fields are required!', 'error')
            return redirect(url_for('main.signup'))
        
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('main.signup'))
        
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists!', 'error')
            return redirect(url_for('main.signup'))

        new_user = User(
            email=email,
            password=generate_password_hash(password),
            authenticated=False
        )
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('main.login'))
    
    return render_template("signup.html")

@main_bp.route("/logout", methods=["GET", "POST"])  
def logout():
    session.clear()
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('main.home'))


@main_bp.route('/metrics')
def metrics_page():
    try:
        with open('model_metrics.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        required_keys = ['accuracy', 'f1', 'precision', 'recall']
        for key in required_keys:
            if key not in data or data[key] is None:
                raise ValueError(f"the {key} is not correct")
                
        return render_template('metrics.html', 
                            accuracy=data['accuracy'],
                            precision=data['precision'],
                            recall=data['recall'],
                            f1=data['f1'],
                            report=data)  
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main_bp.route('/eda')
def eda():
    return render_template('eda.html')

@main_bp.route("/delete/<int:request_id>", methods=["POST"])
def delete_request(request_id):
    if 'email' not in session:
        return redirect(url_for('main.login'))
    
    user = User.query.filter_by(email=session['email']).first()
    request_to_delete = LoanRequest.query.filter_by(id=request_id, user_id=user.id).first()
    
    if request_to_delete:
        db.session.delete(request_to_delete)
        db.session.commit()
        flash('Request deleted successfully', 'success')
    else:
        flash('Request not found or unauthorized', 'danger')
    
    return redirect(url_for('main.manage_request'))

