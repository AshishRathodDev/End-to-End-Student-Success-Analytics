import os
import sys


import numpy as np
import pandas as pd
import dill
from sklearn.metrics import r2_score
import pickle

from src.exception import CustomException 
from sklearn.model_selection import GridSearchCV


def save_object(file_path,obj):
    """
    Save the object to a file using numpy's save function.
    
    Parameters:
    file_path (str): The path where the object will be saved.
    obj: The object to be saved.
    """
    try:
        dir_path = os.path.dirname(file_path)
        
        os.makedirs(dir_path, exist_ok=True)


        with open(file_path, 'wb') as file_obj:
            dill.dump(obj, file_obj)
            
    except Exception as e:        
        raise Exception(e, sys)
    
def evaluate_models(X_train, y_train, X_test, y_test, models,param):
    """
    Evaluate multiple regression models and return their performance metrics.
    
    Parameters:
    X (np.ndarray): Training features.
    y_true (np.ndarray): True target values for training data.
    X_test (np.ndarray): Testing features.
    y_test (np.ndarray): True target values for testing data.
    models (dict): Dictionary of model names and their corresponding model instances.
    
    Returns:
    dict: A dictionary containing model names and their R2 scores.
    """
    try:
        report = {}
        
        for model_name,model in models.items():
            
            model.fit(X_train,y_train)
            param_grid = param.get(model_name, {})
            
            gs = GridSearchCV(model, param_grid, cv=3)
            gs.fit(X_train,y_train)
            
            best_model = gs.best_estimator_
            
            
            y_train_pred = best_model.predict(X_train)
            
            y_test_pred = best_model.predict(X_test)
            
            train_model_score = r2_score(y_train, y_train_pred)
            
            test_model_score = r2_score(y_test, y_test_pred)
            
            report[model_name] = test_model_score
            
        return report
    
    except Exception as e:
        raise CustomException(e, sys)
    
    
    
def load_object(file_path):
         try:
             with open(file_path, "rb") as file_obj:
                    return pickle.load(file_obj)

         except Exception as e:
                raise CustomException(e, sys)
   