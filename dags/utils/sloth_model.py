from sklearn.metrics import classification_report, confusion_matrix
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from utils.files_util import save_files, load_files 
from sklearn.preprocessing import StandardScaler
import pickle
import matplotlib.pyplot as plt

def sloth_model():    

    """FUNCTION SLOTH_MODEL: Load in sloth data. Run through default Random Forest and Decision Tree models. Save to a file.
    """

    #load in training and test data
    x_train, x_test, y_train, y_test = load_files(['x_train_sloth', 'x_test_sloth', 'y_train_sloth', 'y_test_sloth'])

    #decision tree model
    dt_model = DecisionTreeClassifier(random_state = 42, max_depth = 4)
    dt_model.fit(x_train, y_train)
    dt_filename = '/opt/airflow/models/dt_sloth_model.pkl'
    dt_output = open(dt_filename, 'wb')
    pickle.dump(dt_model, dt_output)
    dt_output.close()

    #random forest model
    rf_model = RandomForestClassifier(random_state = 42)
    rf_model.fit(x_train, y_train)
    rf_filename = '/opt/airflow/models/rf_sloth_model.pkl'
    rf_output = open(rf_filename, 'wb')
    pickle.dump(rf_model, rf_output)
    rf_output.close()