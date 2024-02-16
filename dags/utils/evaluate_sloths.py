from utils.files_util import save_files, load_files
import pickle
from sklearn.datasets import make_blobs
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_auc_score
from utils.files_util import save_files, load_files 
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from datetime import datetime
import pandas as pd
import utils.ml_pipeline_config as config
import plotly.express as px
from sqlalchemy import create_engine



def evaluate_sloths():

    """FUNCTION PREPROCESS_SLOTHS: Evaluate a decision tree and random forest model for the sloth data. Evaluate using the 
    classification report. Write this report to the database. Use plotly to graph the model accuracies. 
    """

    #load training and test data
    x_train, x_test, y_train, y_test = load_files(['x_train_sloth', 'x_test_sloth', 'y_train_sloth', 'y_test_sloth'])

    #generate timestamp
    now = datetime.now().strftime("%Y%m%d_%H%M%S")

    #open model and evaluate using the classification report (for db) and accuracy score (for graphing)
    dt_filename = '/opt/airflow/models/dt_sloth_model.pkl'
    dt_model = pickle.load(open(dt_filename, 'rb'))
    dt_y_pred = dt_model.predict(x_test)
    dt_accuracy = accuracy_score(y_test, dt_y_pred)
    dt_report = classification_report(y_test, dt_y_pred,output_dict=True)

    #prepare data frame for input into postgres db
    df_dt = pd.DataFrame(dt_report).transpose()
    #columns cannot be named with underscores...
    df_dt = df_dt.rename(columns={'f1-score': 'f1score'})
    df_dt=df_dt.reset_index()
    df_dt = df_dt.rename(columns={'index': 'classification_param'})
    df_dt['model_datetime'] = now
    df_dt['type'] = 'Decision Tree'

    #print accuracy of model (for debugging)
    #print('Accuracy Score: \n', accuracy_score(y_test, dt_y_pred))
    #print('Classification Report: \n', classification_report(y_test, dt_y_pred))

    #same steps with random forest model
    rf_filename = '/opt/airflow/models/rf_sloth_model.pkl'
    rf_model = pickle.load(open(rf_filename, 'rb'))
    rf_y_pred = rf_model.predict(x_test)
    rf_accuracy = accuracy_score(y_test, rf_y_pred)
    rf_report = classification_report(y_test, rf_y_pred,output_dict=True)

    rf_dt = pd.DataFrame(rf_report).transpose()
    rf_dt = rf_dt.rename(columns={'f1-score': 'f1score'})
    rf_dt=rf_dt.reset_index()
    rf_dt = rf_dt.rename(columns={'index': 'classification_param'})
    rf_dt['model_datetime'] = now
    rf_dt['type'] = 'Random Forest'

    #print for debugging
    #print('Accuracy Score: \n', accuracy_score(y_test, rf_y_pred))
    #print('Classification Report: \n', classification_report(y_test.values, rf_y_pred))

    #write to database
    db_engine = config.params["db_engine"]
    db_schema = config.params["db_schema"]
    table_name = config.params["db_sloth_classification_report_table"] 
    engine = create_engine(db_engine)
    df_dt.to_sql(table_name, engine, schema=db_schema, if_exists='append', index=False)
    rf_dt.to_sql(table_name, engine, schema=db_schema, if_exists='append', index=False)

    #graph accuracies for dasbhoard
    data = [['Decision Tree', dt_accuracy], ['RandomForest', rf_accuracy]]
    df_all = pd.DataFrame(data, columns=['Model Name', 'Accuracy'])
    fig = px.bar(df_all, x='Model Name', y='Accuracy', title = 'Model Accuracies for Sloth Species Classification')
    fig.write_html("/opt/airflow/Visualizations/model_eval.html")

    #show plots for debugging
    #fig.show()