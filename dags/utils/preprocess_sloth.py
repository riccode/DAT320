from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from utils.files_util import save_files
from utils.load_sloth import load_sloth

def preprocess_sloths():

    """FUNCTION PREPROCESS_SLOTHS: Load in sloth data, train/test/split the dataset and save the training files to the "data" folder.
    """

    #load in sloth dataset
    sloths, sloths_X, sloths_y = load_sloth()

    #train/test/split
    sloths_X_train, sloths_X_test, sloths_y_train, sloths_y_test = train_test_split(sloths_X, sloths_y, shuffle=True, test_size=0.3, random_state=42)
    sloths_X_train.name = 'x_train_sloth'
    sloths_X_test.name = 'x_test_sloth'
    sloths_y_train.name = 'y_train_sloth'
    sloths_y_test.name = 'y_test_sloth'

    #save data
    save_files([sloths_X_train, sloths_X_test, sloths_y_train, sloths_y_test])