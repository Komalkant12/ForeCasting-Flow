from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'  # Set the folder where uploaded files will be saved

@app.route('/', methods=['GET'])
def hello_world():
    # Your machine learning model prediction logic here
    # data = request.json
    # prediction = your_ml_model.predict(data['input'])
    return render_template('Body.html')

@app.route('/', methods=['POST'])
def predict():
    if 'csvfile' in request.files:
        csvfile = request.files['csvfile']  # Corrected the file input name
        if csvfile.filename != '':
            filename = secure_filename(csvfile.filename)
            csv_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            csvfile.save('F:/Sales forecasting/Sales forecasting/static')  # Save the uploaded CSV file

            # Your machine learning model prediction logic here
            # prediction = your_ml_model.predict(csv_path)

            return render_template('result.html', prediction="Your prediction goes here")  # Corrected the template name
    return "No CSV file provided."

if __name__ == '__main__':
    app.run(port=3000, debug=True)
