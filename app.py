from flask import Flask, request, jsonify, send_from_directory
from flask import Flask, request, jsonify, send_from_directory, render_template, Response

import pandas as pd
import os
import json

app = Flask(__name__)

# Load your cleaned dataset
df_clean = pd.read_csv("Dataset/cleaned_college_data.csv")

from flask import render_template

@app.route("/")
def serve_frontend():
    return render_template("index.html")


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
            (df_filtered['Placement'] >= min_placement / 10)  # Convert input % to 10-point
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
    result['Placement'] = (result['Placement'] * 10).astype(int).astype(str) + '%'

    # Return result
    if result.empty:
        return jsonify({"message": "No colleges found matching your criteria."})
    else:
        return jsonify(json.loads(result.to_json(orient="records")))



from flask import Response  # Add this import at top if not already

@app.route("/download_colleges", methods=["GET"])
def download_colleges():
    state = request.args.get("state")
    max_fee = request.args.get("max_fee", type=float)
    min_placement = request.args.get("min_placement", type=float)
    course = request.args.get("course")
    top_n = request.args.get("top_n", default=10, type=int)

    df_filtered = df_clean.copy()

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
            (df_filtered['Placement'] >= min_placement / 10)
        ]
    if course:
        df_filtered = df_filtered[
            df_filtered['Stream'].notnull() & 
            df_filtered['Stream'].str.lower().str.contains(course.lower(), na=False)
        ]

    result = df_filtered[
        ['College_Name', 'State', 'UG_fee', 'Placement', 'Rating', 'Stream']
    ].sort_values(by='Placement', ascending=False).head(top_n)

    # Convert Placement to % for consistency in download
    result['Placement'] = (result['Placement'] * 10).astype(int).astype(str) + '%'

    csv_data = result.to_csv(index=False)

    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=colleges.csv"}
    )
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
