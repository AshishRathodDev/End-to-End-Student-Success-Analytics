import os
import sys
import pandas as pd
from src.exception import CustomException
from src.utils import load_object

class PredictPipeline:
    def __init__(self):
        # Using absolute paths is still the best practice
        try:
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
            self.model_path = os.path.join(project_root, 'src', 'model', 'model.pkl')
            self.preprocessor_path = os.path.join(project_root, 'src', 'preprocessor', 'preprocessor.pkl')
            
            self.model = load_object(file_path=self.model_path)
            self.preprocessor = load_object(file_path=self.preprocessor_path)
            print("PredictPipeline initialized successfully. Model and Preprocessor loaded.")
        except Exception as e:
            print(f"Error during PredictPipeline initialization: {e}")
            raise CustomException(e, sys)

    def predict(self, features):
        try:
            data_scaled = self.preprocessor.transform(features)
            preds = self.model.predict(data_scaled)
            return preds
        except Exception as e:
            raise CustomException(e, sys)

class CustomData:
    def __init__(self,
                 gender: str,
                 race_ethnicity: str,
                 parental_level_of_education: str,
                 lunch: str,
                 test_preparation_course: str,
                 reading_score: int,
                 writing_score: int):
        self.gender = gender
        self.race_ethnicity = race_ethnicity
        self.parental_level_of_education = parental_level_of_education
        self.lunch = lunch
        self.test_preparation_course = test_preparation_course
        self.reading_score = reading_score
        self.writing_score = writing_score

    def get_data_as_data_frame(self):
        try:
            # THIS IS THE MOST CRITICAL PART.
            # The keys here MUST EXACTLY MATCH the column names your preprocessor.pkl was trained on.
            custom_data_input_dict = {
                "gender": [self.gender],
                "race/ethnicity": [self.race_ethnicity], # This name with a slash is unusual but must match the training data
                "parental level of education": [self.parental_level_of_education], # This name with spaces is unusual
                "lunch": [self.lunch],
                "test preparation course": [self.test_preparation_course], # This name with spaces is unusual
                "reading score": [self.reading_score], # This name with a space is unusual
                "writing score": [self.writing_score], # This name with a space is unusual
            }
            return pd.DataFrame(custom_data_input_dict)
        except Exception as e:
            raise CustomException(e, sys)

# ==========================================================
# ===                 SELF-TESTING BLOCK                 ===
# ==========================================================
# Yeh code sirf tab chalega jab app start hoga.
# Yeh Flask se alag, is file ko test karega.
# Agar is block mein error aaya, toh woh CONTAINER LOGS mein 100% dikhega.
if __name__ == "__main__":
    print("\n\n[SELF-TEST] Running a test on predict_pipeline.py...")
    try:
        # 1. Create dummy data, just like it would come from the form
        sample_data = CustomData(
            gender='female',
            race_ethnicity='group B',
            parental_level_of_education="bachelor's degree",
            lunch='standard',
            test_preparation_course='none',
            reading_score=72,
            writing_score=74
        )
        
        # 2. Convert it to a DataFrame
        sample_df = sample_data.get_data_as_data_frame()
        print("[SELF-TEST] Sample DataFrame created:")
        print(sample_df)
        
        # 3. Initialize the prediction pipeline
        pipeline = PredictPipeline()
        
        # 4. Make a prediction
        prediction_result = pipeline.predict(sample_df)
        print(f"[SELF-TEST] Prediction successful! Result: {prediction_result}")
        print("[SELF-TEST] The predict_pipeline.py file is working correctly.\n\n")

    except Exception as e:
        print("\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!! [SELF-TEST] FAILED! Error in predict_pipeline.py !!!")
        print(f"!!! Error details: {e} !!!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")