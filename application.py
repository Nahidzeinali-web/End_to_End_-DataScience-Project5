# Import required libraries
import joblib  # For loading the pre-trained machine learning model
import numpy as np  # For numerical operations and array handling
from config.paths_config import MODEL_OUTPUT_PATH  # Path where the trained model is saved
from flask import Flask, render_template, request  # Flask web framework components

# Initialize Flask application
app = Flask(__name__)

# Load the trained model from the specified file path
loaded_model = joblib.load(MODEL_OUTPUT_PATH)

# Define the main route for the web application
@app.route('/', methods=['GET', 'POST'])
def index():
    # Handle form submission (POST request)
    if request.method == 'POST':
        # Extract features from HTML form input and convert them to appropriate data types
        lead_time = int(request.form["lead_time"])
        no_of_special_request = int(request.form["no_of_special_request"])
        avg_price_per_room = float(request.form["avg_price_per_room"])
        arrival_month = int(request.form["arrival_month"])
        arrival_date = int(request.form["arrival_date"])
        market_segment_type = int(request.form["market_segment_type"])
        no_of_week_nights = int(request.form["no_of_week_nights"])
        no_of_weekend_nights = int(request.form["no_of_weekend_nights"])
        type_of_meal_plan = int(request.form["type_of_meal_plan"])
        room_type_reserved = int(request.form["room_type_reserved"])

        # Create a NumPy array with the input features in the correct shape
        features = np.array([[lead_time, no_of_special_request, avg_price_per_room,
                              arrival_month, arrival_date, market_segment_type,
                              no_of_week_nights, no_of_weekend_nights,
                              type_of_meal_plan, room_type_reserved]])

        # Use the loaded model to make a prediction based on the input features
        prediction = loaded_model.predict(features)

        # Render the HTML template with the prediction result
        return render_template('index.html', prediction=prediction[0])
    
    # For GET requests, just render the page with no prediction initially
    return render_template("index.html", prediction=None)

# Entry point to run the Flask app on host 0.0.0.0 and port 8080
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
