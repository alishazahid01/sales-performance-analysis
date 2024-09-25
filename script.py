"""Using OPENAI Version == 0.28 as the latest version 
   doesn't support this"""

"""Run Code using terminal ---> python script.py"""

"""Access the API Endpoints using a web browser"""
# http://127.0.0.1:5000/api/rep_performance?employee_id=1
# Replace 1 with the actual employee_id you want to analyze.

# http://127.0.0.1:5000/api/team_performance

# http://127.0.0.1:5000/api/performance_trends?time_period=monthly


# Importing necessary libraries
import pandas as pd  
import os  
from flask import Flask, jsonify, request  
import openai  

# OpenAI API Key 
# Note this api key limit is already exceed, so kindly use your openai API key for testing
openai.api_key = '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'

app = Flask(__name__)

class SalesTeamPerformance:

    def data_ingestion(self, file_path):
        # Check if the file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        
        # Read the file based on its extension
        if file_path.endswith('.csv'):
            return pd.read_csv(file_path)
        elif file_path.endswith('.json'):
            return pd.read_json(file_path)
        else:
            raise ValueError("Unsupported file format.")
    
    def generate_llm_feedback(self, prompt):
        """Call OpenAI's GPT to generate feedback based on the input prompt."""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150
            )
            return response['choices'][0]['message']['content'].strip()  
        except Exception as e:
            return f"Error generating feedback from LLM: {e}"
    
    def analyze_individual_performance(self, sales_data, employee_id):
        # Filter data for the specific employee
        emp_data = sales_data[sales_data['employee_id'] == employee_id]
        if emp_data.empty:
            return f"No data found for employee with ID {employee_id}"
        
        # You can calculate different metrics based on the available columns
        tours_booked = emp_data['tours_booked'].sum()
        revenue_confirmed = emp_data['revenue_confirmed'].sum()
        prompt = f"Employee {employee_id} has booked {tours_booked} tours and confirmed revenue of {revenue_confirmed}. Provide feedback."
        
        # Generate feedback using OpenAI LLM
        feedback = self.generate_llm_feedback(prompt)
        
        return feedback
    
    def analyze_team_performance(self, sales_data):
        # Analyze overall team performance
        total_tours_booked = sales_data['tours_booked'].sum()
        total_revenue_confirmed = sales_data['revenue_confirmed'].sum()
        prompt = f"The sales team has booked a total of {total_tours_booked} tours with confirmed revenue of {total_revenue_confirmed}. Provide overall team performance feedback."
        
        # Generate feedback using OpenAI LLM
        feedback = self.generate_llm_feedback(prompt)
        
        return feedback
    
    def analyze_performance_trends(self, sales_data, time_period):
        # Simulate performance trends analysis for now
        prompt = f"Analyze sales trends for the period '{time_period}' and provide insights on sales growth and future forecasts."
        
        # Generate feedback using OpenAI LLM
        feedback = self.generate_llm_feedback(prompt)
        
        return feedback


# Starting running SalesTeamPerformance() class
sales_team_performance = SalesTeamPerformance()

# Load the sales data once when the application starts
file_path = r"D:\Home_Assessment\sales_performance_data.csv"
try:
    sales_data = sales_team_performance.data_ingestion(file_path)
except Exception as e:
    print(f"Error: {e}")
    sales_data = pd.DataFrame()

# Testinnggggg
"""
for column in sales_data.columns:
    print(column)"""

# API Endpoints

# 1. Individual Employee Performance Analysis
@app.route('/api/rep_performance', methods=['GET'])
def rep_performance():
    employee_id = request.args.get('employee_id', type=int)
    if employee_id is None:
        return jsonify({"error": "Please provide a valid employee_id."}), 400
    feedback = sales_team_performance.analyze_individual_performance(sales_data, employee_id)
    return jsonify({"feedback": feedback})

# 2. Overall Sales Team Performance Summary
@app.route('/api/team_performance', methods=['GET'])
def team_performance():
    feedback = sales_team_performance.analyze_team_performance(sales_data)
    return jsonify({"feedback": feedback})

# 3. Sales Performance Trends and Forecasting
@app.route('/api/performance_trends', methods=['GET'])
def performance_trends():
    time_period = request.args.get('time_period', default="monthly")
    feedback = sales_team_performance.analyze_performance_trends(sales_data, time_period)
    return jsonify({"feedback": feedback})

# Run the Flask API server
if __name__ == "__main__":
    app.run(debug=True)
