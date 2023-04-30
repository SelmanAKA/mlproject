import os
import sys
from dataclasses import dataclass

from catboost import CatBoostRegressor
from sklearn.ensemble import(
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object,evaluate_models

# Extras for linear regression variations
from sklearn.linear_model import Lasso
from sklearn.linear_model import Ridge
from sklearn.linear_model import ElasticNet
from sklearn.linear_model import BayesianRidge

@dataclass
class ModelTrainerConfig:
    trained_model_file_path=os.path.join("artifacts","model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config=ModelTrainerConfig()

    def initiate_model_trainer(self,train_array,test_array):
        try:
            logging.info("split train and test inputs.")
            X_train,y_train,X_test,y_test=(
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )

            models = {
                "Lasso Regression": Lasso(),
                "Ridge Regression": Ridge(),
                "Elastic Net Regression": ElasticNet(),
                "Bayesian Ridge Regression": BayesianRidge(),
                #"Random Forest": RandomForestRegressor(),
                #"Decision Tree": DecisionTreeRegressor(),
                #"Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                #"XGBRegressor": XGBRegressor(),
                #"CatBoosting Regressor": CatBoostRegressor(verbose=False),
                #"AdaBoost Regressor": AdaBoostRegressor(),
            }
            
            params={
                "Lasso Regression":{
                    'alpha':[0.001,0.01,0.1,1,10],
                    'fit_intercept':[True,False],
                    'precompute':[True,False],
                    'warm_start':[True,False],
                    'random_state': [42],
                    'selection':['cyclic','random'],
                },
                "Ridge Regression": {
                    'alpha': [0.001, 0.01, 0.1, 1, 10],
                    'fit_intercept': [True, False],
                    'solver': ['auto', 'svd', 'cholesky', 'lsqr', 'sparse_cg', 'sag', 'saga'],
                    'random_state': [42]
                },
                "Elastic Net Regression": {
                    "alpha": [0.001, 0.01, 0.1, 1, 10, 100],
                    "l1_ratio": [0.1, 0.5, 0.7, 0.9, 1],
                    "fit_intercept": [True, False],
                    'precompute':[True,False],
                    'warm_start':[True,False],
                    'random_state': [42],
                    'selection':['cyclic','random'],
                },
                "Bayesian Ridge Regression": {
                    "alpha_1": [1e-6, 1e-5, 1e-4],
                    "alpha_2": [1e-6, 1e-5, 1e-4],
                    "lambda_1": [1e-6, 1e-5, 1e-4],
                    "lambda_2": [1e-6, 1e-5, 1e-4],
                    "fit_intercept": [True, False]
                },
                "Linear Regression":{
                    'fit_intercept':[True,False],
                },
                #"Decision Tree": {
                #   'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                #    'splitter':['best','random'],
                #    'max_features':['sqrt','log2'],
                #},
                #"Random Forest":{
                #    'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                #    'max_features':['sqrt','log2',None],
                #    'n_estimators': [8,16,32,64,128,256]
                #},
                #"Gradient Boosting":{
                #    'loss':['squared_error', 'huber', 'absolute_error', 'quantile'],
                #    'learning_rate':[.1,.01,.05,.001],
                #    'subsample':[0.6,0.7,0.75,0.8,0.85,0.9],
                #    'criterion':['squared_error', 'friedman_mse'],
                #    'max_features':['sqrt','log2'],
                #    'n_estimators': [8,16,32,64,128,256]
                #},
                #"XGBRegressor":{
                #    'learning_rate':[.1,.01,.05,.001],
                #    'n_estimators': [8,16,32,64,128,256]
                #},
                #"CatBoosting Regressor":{
                #    'depth': [6,8,10],
                #    'learning_rate': [0.01, 0.05, 0.1],
                #    'iterations': [30, 50, 100]
                #},
                #"AdaBoost Regressor":{
                #    'learning_rate':[.1,.01,0.5,.001],
                #    'loss':['linear','square','exponential'],
                #    'n_estimators': [8,16,32,64,128,256]
                #}
            }


            model_report:dict=evaluate_models(X_train=X_train,y_train=y_train,X_test=X_test,y_test=y_test,models=models,param=params)

            best_model_score = max(sorted(model_report.values()))

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

            best_model = models[best_model_name]

            if best_model_score<0.6:
                raise CustomException("No best model found.")
        
            logging.info("selected best model")

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )
            predicted=best_model.predict(X_test)

            r2_square = r2_score(y_test,predicted)
            return r2_square, best_model_name

        except Exception as e:
            raise CustomException(e,sys)










