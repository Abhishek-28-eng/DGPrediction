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
                <h1>No student found with Unique_ID: {{ student_id }}</h1>
                <a href="/">Back to search</a>
                ''',
                student_id=student_id
            )
        
        # Convert student data to a dictionary for rendering
        student_data_dict = student_data.iloc[0].to_dict()
        return render_template_string(
            '''
            <h1>Student Details</h1>
            <table border="1">
                {% for key, value in student_data.items() %}
                <tr>
                    <th>{{ key }}</th>
                    <td>
                        {% if key == 'Interest_Percentages' %}
                            {{ value | tojson }}
                        {% else %}
                            {{ value }}
                        {% endif %}
                    </td>
                </tr>
                {% endfor %}
            </table>
            <a href="/">Back to search</a>
            ''',
            student_data=student_data_dict
        )
    
    # Display the form for entering Unique_ID
    return render_template_string(
        '''
        <h1>Search for Student by Unique_ID</h1>
        <form method="post">
            <label for="student_id">Enter Unique_ID:</label>
            <input type="text" id="student_id" name="student_id" required>
            <button type="submit">Search</button>
        </form>
        '''
    )

if __name__ == "__main__":
    app.run(debug=True)
