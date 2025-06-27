from flask import Flask, request, jsonify, send_from_directory
import pandas as pd
import os
import json

app = Flask(__name__)

# Load your cleaned dataset
df_clean = pd.read_csv("C:/Users/shubh/OneDrive/Desktop/Projects/Chat_Bot/Dataset/cleaned_college_data.csv")

@app.route("/")
def serve_frontend():
    # Serve the index.html file
    return send_from_directory(os.getcwd(), "index.html")

@app.route("/get_colleges", methods=["GET"])
def get_colleges():
    # Get query parameters
    state = request.args.get("state")
    max_fee = request.args.get("max_fee", type=float)
    min_placement = request.args.get("min_placement", type=float)
    course = request.args.get("course")
    top_n = request.args.get("top_n", default=10, type=int)

    # Make a copy of the dataframe to filter
    df_filtered = df_clean.copy()

    # Apply filters
    if state:
        df_filtered = df_filtered[
            df_filtered['State'].notnull() &
            (df_filtered['State'].str.lower() == state.lower())
        ]
    if max_fee:
        df_filtered = df_filtered[
            df_filtered['UG_fee'].notnull() &
            (df_filtered['UG_fee'] <= max_fee)
        ]

    if min_placement:
        df_filtered = df_filtered[
            df_filtered['Placement'].notnull() &
            (df_filtered['Placement'] >= min_placement)
        ]

    if course:
        df_filtered = df_filtered[
            df_filtered['Stream'].notnull() &
            df_filtered['Stream'].str.lower().str.contains(course.lower(), na=False)
        ]

    # Prepare result
    result = df_filtered[
        ['College_Name', 'State', 'UG_fee', 'Placement', 'Rating', 'Stream']
    ].sort_values(by='Placement', ascending=False).head(top_n)

    # Return result
    if result.empty:
        return jsonify({"message": "No colleges found matching your criteria."})
    else:
        return jsonify(json.loads(result.to_json(orient="records")))

if __name__ == "__main__":
    app.run(debug=True)
