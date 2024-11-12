from flask import Flask, jsonify, render_template
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

# Load CSV file
try:
    df = pd.read_csv('dump.csv')
except FileNotFoundError:
    print("Error: 'dump.csv' not found. Ensure it's in the same directory as app.py.")
    exit()

# Route to serve index.html
@app.route('/')
def home():
    return render_template('index.html')

# API to get list of companies
@app.route('/companies', methods=['GET'])
def get_companies():
    companies = df['index_name'].unique().tolist()  # Replace with actual column name
    return jsonify(companies)

# API to get data for a specific company
@app.route('/company/<string:name>', methods=['GET'])
def get_company_data(name):
    company_data = df[df['index_name'] == name].to_dict(orient='records')  # Replace with actual column name
    if not company_data:
        return jsonify({'error': f'No data found for company: {name}'}), 404
    return jsonify(company_data)

if __name__ == '__main__':
    app.run(debug=True)
