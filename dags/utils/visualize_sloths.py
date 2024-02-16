import seaborn as sns
import matplotlib.pyplot as plt
from utils.load_sloth import load_sloth

def visualize_sloths():

    """FUNCTION visualize_sloths: Produces EDA plots for sloth dataset. 3 plots are generated, a boxplot, a correlation heatmap
    and bar plot showing the number of individuals in each category. 
    """

    #load sloth dataset
    sloths, sloths_X, sloths_y = load_sloth()

    #create boxplots of sloth data seperated by species
    plt.figure(figsize = (10, 8))
    fig, ((ax1, ax2, ax3, ax4)) = plt.subplots(nrows=1, ncols=4, figsize = (25, 12))
    sns.boxplot(ax=ax1, x = 'specie', y = 'claw_length_cm', hue = 'specie', data = sloths)
    sns.boxplot(ax=ax2, x = 'specie', y = 'size_cm', hue = 'specie', data = sloths)
    sns.boxplot(ax=ax3, x = 'specie', y = 'tail_length_cm', hue = 'specie', data = sloths)
    sns.boxplot(ax=ax4, x = 'specie', y = 'weight_kg', hue = 'specie', data = sloths)
    ax1.tick_params(axis='x', labelrotation=90)
    ax2.tick_params(axis='x', labelrotation=90)
    ax3.tick_params(axis='x', labelrotation=90)
    ax4.tick_params(axis='x', labelrotation=90)

    #save boxplot file
    sloth_boxplot = fig.get_figure()
    sloth_boxplot.savefig("/opt/airflow/Visualizations/boxplot.png") 
    sloth_boxplot.clf()
    sloth_boxplot.clear()

    #create correlation matrix
    plt.figure(figsize = (10, 8))
    plt.title("Correlation of sloth measurements")
    corr = sloths_X.corr()
    sns_heatmap = sns.heatmap(corr, annot = True)
    heatmap_fig = sns_heatmap.get_figure()
    heatmap_fig.savefig("/opt/airflow/Visualizations/heatmap.png") 
    heatmap_fig.clf()
    heatmap_fig.clear()

    #create plot to display number of individuals in each species
    plt.figure(figsize = (10, 8))
    plt.title("Number of individuals in each sloth species")
    bar_plot = sloths['specie'].value_counts().plot.bar()
    bar_fig = bar_plot.get_figure()
    bar_fig.savefig("/opt/airflow/Visualizations/sloth_distribution.png") 
    bar_fig.clf()
    bar_fig.clear()