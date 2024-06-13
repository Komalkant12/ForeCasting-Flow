import matplotlib

# Set the Matplotlib backend to 'Agg' before importing pyplot
matplotlib.use('Agg')

from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from statsmodels.tsa.arima.model import ARIMA
import statsmodels.api as sm
from pandas.plotting import autocorrelation_plot
from statsmodels.tsa.stattools import adfuller
from flask_mysqldb import MySQL

# Initialize Flask app
app = Flask(__name__)
# Set secret key for session management
app.secret_key = 'your_secret_key'

# Define upload folder
app.config['UPLOAD_FOLDER'] = "E:\\Projects\\Sales forecasting MAJOR\\Sales forecasting\\static"

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask_users'

# Initialize MySQL
mysql = MySQL(app)

# Home page route
@app.route('/')
def index():
    # Check if the user is logged in
    if 'username' in session:
        # Pass the username to the template
        return render_template('Body.html', username=session['username'])
    else:
        return render_template('Body.html')

# Header template route
@app.route('/header.html')
def header_template():
    return render_template('header.html')

# Footer template route
@app.route('/footer.html')
def footer_template():
    return render_template('footer.html')

# Dashboard route
@app.route('/dashboard.html')
def dashboard():
    return render_template('dashboard.html')

# Sales input route
@app.route('/sales_input')
def sales_input():
    return render_template('Sales.html')

# Data Report route
@app.route('/report')
def report():
    return render_template('data_report.html')

# Login route
@app.route('/login')
def login():
    return render_template('login.html')

# Signup route
@app.route('/signup')
def signup():
    return render_template('register.html')

# Route to handle the login form submission
@app.route('/login_submit', methods=['POST'])
def login_submit():
    email = request.form['email']
    password = request.form['password']

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM user_data WHERE email = %s AND password = %s", (email, password))
    user = cursor.fetchone()

    if user:
        # User found, redirect to dashboard or another page
        flash('Login successful!', 'success')
        return redirect(url_for('index'))
    else:
        # User not found, redirect back to login page with error message
        flash('Invalid email or password. Please try again.', 'error')
        return redirect(url_for('login'))

# Route to handle the signup form submission
@app.route('/signup_submit', methods=['POST'])
def signup_submit():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM user_data WHERE email = %s", (email,))
    existing_user = cursor.fetchone()

    if existing_user:
        flash('Email already exists. Please use a different email.', 'error')
        return redirect(url_for('signup'))
    else:
        cursor.execute("INSERT INTO user_data (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
        mysql.connection.commit()
        flash('Sign up successful! You can now login.', 'success')
        return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
   # Check if the user is logged in
    if 'username' in session:
        # Clear the user session
        session.pop('username')
        # Redirect to the login page with a success message
        return redirect(url_for('login', message='You have been successfully logged out.'))

    # If the user is not logged in, redirect to the login page
    return redirect(url_for('login'))


# Route to display the upload form
@app.route('/upload_form')
def upload_form():
    return render_template('Res.html')

# Function to perform ADF test on sales data
def adfuller_test(sales):
    result = adfuller(sales)
    labels = ['ADF Test Statistic', 'p-value', '#Lags Used', 'Number of Observations Used']
    for value, label in zip(result, labels):
        print(label + ' : ' + str(value))
    if result[1] <= 0.05:
        print("Strong evidence against the null hypothesis (Ho), reject the null hypothesis. Data has no unit root and is stationary.")
    else:
        print("Weak evidence against null hypothesis, time series has a unit root, indicating it is non-stationary.")

# Route to handle file upload and perform time series analysis
@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if file was uploaded
    if 'file' in request.files:
        uploaded_file = request.files['file']
        # Check if file name is not empty
        if uploaded_file.filename != '':
            # Define file path
            filename = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            # Save the uploaded file
            uploaded_file.save(filename)
            # Read CSV file
            df = pd.read_csv(filename)
            # Preprocess data
            df.columns = ["Month", "Sales"]
            df.drop([105, 106], axis=0, inplace=True)
            df['Month'] = pd.to_datetime(df['Month'])
            df.set_index('Month', inplace=True)
            
            # Plotting
            df.plot(figsize=(12, 6))
            plt.xlabel('Month')
            plt.ylabel('Sales')
            plt.title('Monthly Champagne Sales')
            img = BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()
            plt.close()

            # Perform ADF test
            adfuller_test(df['Sales'])

            # Autocorrelation Plot
            autocorrelation_plot(df['Sales'])
            plt.xlabel('Lag')
            plt.ylabel('Autocorrelation')
            plt.title('Autocorrelation Plot')
            img4 = BytesIO()
            plt.savefig(img4, format='png')
            img4.seek(0)
            plot_url4 = base64.b64encode(img4.getvalue()).decode()
            plt.close()

            # ARIMA model
            model = ARIMA(df['Sales'], order=(1, 1, 1))
            model_fit = model.fit()

            # Plot Sales and Forecast
            df['forecast'] = model_fit.predict(start=90, end=120, dynamic=True)
            df[['Sales', 'forecast']].plot(figsize=(12, 6))
            plt.xlabel('Month')
            plt.ylabel('Sales')
            plt.title('Sales Forecast (ARIMA)')
            img1 = BytesIO()
            plt.savefig(img1, format='png')
            img1.seek(0)
            plot_url1 = base64.b64encode(img1.getvalue()).decode()
            plt.close()

            # SARIMAX model
            model = sm.tsa.statespace.SARIMAX(df['Sales'], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
            results = model.fit()
            df['forecast'] = results.predict(start=90, end=103, dynamic=True)
            df[['Sales', 'forecast']].plot(figsize=(12, 8))
            img2 = BytesIO()
            plt.savefig(img2, format='png')
            img2.seek(0)
            plot_url2 = base64.b64encode(img2.getvalue()).decode()
            plt.close()

            # Forecast future sales
            future_dates = [df.index[-1] + pd.DateOffset(months=x) for x in range(0, 24)]
            future_datest_df = pd.DataFrame(index=future_dates[1:], columns=df.columns)
            future_df = pd.concat([df, future_datest_df])
            future_df['forecast'] = results.predict(start=104, end=120, dynamic=True)
            future_df[['Sales', 'forecast']].plot(figsize=(12, 8))
            plt.xlabel('Month')
            plt.ylabel('Sales')
            plt.title('Sales Forecast (SARIMAX)')
            img3 = BytesIO()
            plt.savefig(img3, format='png')
            img3.seek(0)
            plot_url3 = base64.b64encode(img3.getvalue()).decode()
            plt.close()
            
            # Render template with plot URLs
            return render_template('Res.html', plot_url=plot_url, plot_url1=plot_url1, plot_url2=plot_url2, plot_url3=plot_url3, plot_url4=plot_url4)
    
    # Return message if no file was provided
    return "No file provided."

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
