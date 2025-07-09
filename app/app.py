from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd
from pathlib import Path

app = Flask(__name__)

# Loding the trained model
BASE_DIR = Path(__name__).resolve().parent
MODEL_PATH = (BASE_DIR / "models" / "personality_classifier_model.pkl").resolve()
model = joblib.load(MODEL_PATH)

@app.route('/')
def index():
   return render_template("index.html")

@app.route('/submit', methods=["POST"])
def submit():
   data = request.get_json()

   columns = [
      "Time_spent_Alone", 
      "Social_event_attendance", 
      "Going_outside", 
      "Friends_circle_size", 
      "Post_frequency", 
      "Stage_fear", 
      "Drained_after_socializing"
   ]
   input_df = pd.DataFrame([[
      float(data["Time_spent_alone"]),
      float(data["Social_event_attendance"]),
      float(data["Going_outside"]),
      float(data["Friends_circle_size"]),
      float(data["Post_frequency"]),
      int(data["Stage_fear"]),
      int(data["Drained_after_socializing"])
   ]], columns=columns)

   personality = model.predict(input_df)[0]
   probability = model.predict_proba(input_df)[0] 

   return jsonify({
      "prediction": int(personality),
      "confidence": float(round(max(probability) * 100, 2)),
      "input": input_df.to_dict(orient="records")
   })

if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0', port=5000)