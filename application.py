from flask import Flask, request, render_template 
import numpy as np
import pandas as pd
import traceback # Import traceback for detailed error printing

from src.pipeline.predict_pipeline import PredictPipeline, CustomData

application = Flask(__name__)
app = application

# --- Home Page Route ---
@app.route('/')
def index():
    return render_template('index.html')

# --- Prediction Route ---
@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    print(f"\n\n======= [START] Request received for /predictdata with method: {request.method} =======")
    if request.method == 'GET':
        print("[INFO] Method is GET, rendering home.html")
        return render_template('home.html')
    else:
        try:
            print("[INFO] Method is POST, starting data processing...")
            
            data = CustomData(
                gender=request.form.get('gender'),
                race_ethnicity=request.form.get('race_ethnicity'), 
                parental_level_of_education=request.form.get('parental_level_of_education'), 
                lunch=request.form.get('lunch'),
                test_preparation_course=request.form.get('test_preparation_course'), 
                reading_score=int(request.form.get('reading_score')), 
                writing_score=int(request.form.get('writing_score'))  
            )
            print("[SUCCESS] Step 1/5: CustomData object created successfully.")
            
            pred_df = data.get_data_as_data_frame()
            print("[SUCCESS] Step 2/5: DataFrame created successfully.")
            print("--- DataFrame Content ---")
            print(pred_df)
            print("-------------------------")
            
            predict_pipeline = PredictPipeline()
            print("[SUCCESS] Step 3/5: PredictPipeline initialized.")
            
            results = predict_pipeline.predict(pred_df)
            print(f"[SUCCESS] Step 4/5: Prediction successful. Raw result: {results}")
            
            final_result = round(results[0], 2)
            print(f"[SUCCESS] Step 5/5: Final result calculated: {final_result}")
            
            print("[FINAL] Now rendering home.html with the result.")
            return render_template('home.html', results=final_result)

        except Exception as e:
            # This will now catch any possible error and print a full traceback
            print(f"\n\n!!!!!!!!!!!!! CATASTROPHIC ERROR IN /predictdata !!!!!!!!!!!!!")
            print(f"Error Type: {type(e).__name__}, Details: {e}")
            print(f"--- FULL STACK TRACE ---")
            traceback.print_exc() # This prints the exact line of failure
            print(f"--------------------------")
            print(f"Form Data Received: {request.form}")
            print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
            
            return render_template('home.html', error_message=f"An error occurred. Please check the logs for details.")

# --- Debug Route ---
@app.route('/debug')
def debug():
    return "App is running fine!"    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050)