import matplotlib.pyplot as plt
import pickle
from utils.load_sloth import load_sloth
import pandas as pd
import itertools
import matplotlib.colors as mcolors

def sloth_feature_importances():
    
    """ FUNCTION SLOTH_FEATURE_IMPORTANCES: Determines the 2 most important features for the dataset and then plots them in a 
        scatter plot to visualize the distribution of the most important features. 
    """
    
    #load decision tree model
    filename = '/opt/airflow/models/dt_sloth_model.pkl'
    sloths_model = pickle.load(open(filename, 'rb'))

    #load raw data 
    sloths, sloths_X, sloths_y = load_sloth()
    sloths_features = sloths_X.columns

    #pull feature importances
    sloths_model.feature_importances_
    list(zip(sloths_features, sloths_model.feature_importances_))

    #write important features to dataframe    
    important_features = pd.DataFrame(list(zip(sloths_features, sloths_model.feature_importances_)), columns=['feature', 'importance'])
    important_features.set_index('feature', inplace=True)

    #plot important features in bar graph and save 
    fig, ax = plt.subplots(figsize=(10, 8))
    plt.title("Feature importance of sloth measurements")
    important_features.sort_values(by='importance').plot(kind='barh', ax= ax)
   
    fig = ax.get_figure()
    fig.savefig('/opt/airflow/Visualizations//feature_importances.png')
    fig.clf()

    #pull out top two important features and plot against each other    
    fi = important_features.sort_values(by='importance',ascending=False)
    fi.iloc[0,:]['importance'] 
    unique_species = sloths["specie"].unique()
    colors = itertools.cycle(mcolors.TABLEAU_COLORS)

    #loop through each sloth species nad plot
    fig, ax = plt.subplots()
    plt.title("Top 2 most important features for sloth model (decision tree)")
    for species in unique_species:
        sloth_species = sloths.loc[(sloths["specie"] == species), ["specie", fi.iloc[0,:].name , fi.iloc[1,:].name ]]
        ax.scatter(sloth_species[fi.iloc[0,:].name], sloth_species[fi.iloc[1,:].name],color=next(colors))



    #format plot and save    
    plt.legend(
            (unique_species.tolist()),
            scatterpoints=1,
            loc='lower left',
            ncol=unique_species.size,
            fontsize=8)

    #plt.title(fi.iloc[0,:].name +' vs ' + fi.iloc[1,:].name + ' of sloths')
    plt.xlabel(fi.iloc[0,:].name)
    plt.ylabel(fi.iloc[1,:].name )
    #plt.show()
    plt.savefig('/opt/airflow/Visualizations/sloth_scatter.png')
    plt.clf()