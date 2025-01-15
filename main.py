from flask import Flask, request, render_template_string
import pandas as pd
from TopInterest import output_df

app = Flask(__name__)


output_df = pd.DataFrame(output_df)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get the Unique_ID entered by the user
        student_id = request.form.get("student_id").strip()  # Remove extra spaces
        
        # Filter the DataFrame for the given Unique_ID
        student_data = output_df.loc[output_df["Unique_ID"] == student_id]
        
        if student_data.empty:
            # If no matching Unique_ID is found
            return render_template_string(
                '''
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <title>Student Search</title>
                    <style>
                        body { font-family: Arial, sans-serif; text-align: center; }
                        h1 { color: #ff4c4c; }
                        a { text-decoration: none; color: #007bff; }
                    </style>
                </head>
                <body>
                    <h1>No student found with Unique_ID: {{ student_id }}</h1>
                    <a href="/">Back to search</a>
                </body>
                </html>
                ''',
                student_id=student_id
            )
        
        # Convert student data to a dictionary for rendering
        student_data_dict = student_data.iloc[0].to_dict()
        interest_data = {k: v for k, v in student_data_dict.items() if k not in ["Unique_ID", "Computed_Final_Interests"]}

        return render_template_string(
            '''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <title>Student Details</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; }
                    table { border-collapse: collapse; width: 80%; margin: auto; }
                    th, td { border: 1px solid #ddd; padding: 8px; text-align: center; }
                    th { background-color: #4CAF50; color: white; }
                    .chart-container { width: 60%; margin: auto; padding: 20px; }
                    a { text-decoration: none; color: #007bff; }
                </style>
                <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            </head>
            <body>
                <h1>Student Details</h1>
                <table>
                    <tr><th>Unique_ID</th><td>{{ student_data['Unique_ID'] }}</td></tr>
                    <tr><th>Final Interests</th><td>{{ student_data['Computed_Final_Interests'] }}</td></tr>
                </table>
                <div class="chart-container">
                    <canvas id="interestChart"></canvas>
                </div>
                <a href="/">Back to search</a>

<script>
    const ctx = document.getElementById('interestChart').getContext('2d');
    const data = {
        labels: {{ interest_data.keys()|list|tojson }},  // Convert dict_keys to a list
        datasets: [{
            label: 'Interest Levels',
            data: {{ interest_data.values()|list|tojson }},  // Convert dict_values to a list
            backgroundColor: [
                'rgba(75, 192, 192, 0.2)',
                'rgba(255, 159, 64, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 205, 86, 0.2)',
                'rgba(201, 203, 207, 0.2)',
                'rgba(54, 162, 235, 0.2)'
            ],
            borderColor: [
                'rgba(75, 192, 192, 1)',
                'rgba(255, 159, 64, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 205, 86, 1)',
                'rgba(201, 203, 207, 1)',
                'rgba(54, 162, 235, 1)'
            ],
            borderWidth: 1
        }]
    };
    const config = {
        type: 'bar',
        data: data,
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    };
    new Chart(ctx, config);
</script>

            </body>
            </html>
            ''',
            student_data=student_data_dict,
            interest_data=interest_data
        )
    
    # Display the form for entering Unique_ID
    return render_template_string(
        '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <title>Search Student</title>
            <style>
                body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
                input, button { padding: 10px; font-size: 16px; }
                button { background-color: #4CAF50; color: white; border: none; cursor: pointer; }
                button:hover { background-color: #45a049; }
            </style>
        </head>
        <body>
            <h1>Search for Student by Unique_ID</h1>
            <form method="post">
                <label for="student_id">Enter Unique_ID:</label>
                <input type="text" id="student_id" name="student_id" required>
                <button type="submit">Search</button>
            </form>
        </body>
        </html>
        '''
    )

if __name__ == "__main__":
    app.run(debug=True)

