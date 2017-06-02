# dssd-fbeta

# [Data section](data/)
Contains different datasets. Note that the data are in **.arff** format with a different style from the one used in http://mulan.sourceforge.net/. There are three types of attributes: 
- **numeric**: for numerical attributes (the numerical pattern space will be the one presented in [Kaytoue-2011](https://hal.archives-ouvertes.fr/inria-00584371/document).
- **symbolic**: for nominal attributes.
- **boolean**: for boolean attributes (special case of nominal attributes where only the presence of the item is considered in the pattern space).
Note that in order to ignore attributes, the keyword **ignore** is used, as shown in [data/reducedFlags.arff](data/reducedFlags.arff).

The boxplots of the label distributions of the six datasets in [data](data/) are given in this sections. The **dynamic beta** is also plotted where the two parameters **xbeta** and **lbeta** are given in [scripts/xlbetas.csv](scripts/xlbetas.csv). Note that, for [data/reducedFlags.arff](data/reducedFlags.arff) the  **xbeta** and **lbeta** parameters are computed automatically using the approach presented in the **section 7.2 (page 17)** of the [paper](paper/mlj17.pdf). 

![](data/CAL500.png?raw=true)
![](data/enron.png?raw=true)

# [Experiments section](experiments/)

## [xlbeta](experiments/xlbeta) 
The script given in [xlbeta experiment](experiments/xlbeta) show how to draw the **boxplot** with its **dynamic beta plot** for the desired dataset. Please read [xp.sh](experiments/xlbeta/xp.sh) to see how to plot the desired dataset. The used script (to customize manually **xbeta** and **lbeta** parameters) is given in [script.py](scripts/script.py).

## [mcts](experiments/mcts)
The main experiments results of the paper is given by the script [xp.sh](experiments/mcts/xp.sh). Please comment the undesired files before launching the script. 

Note that the last line of the script ```./launch.sh ../../data/reducedFlags.arff numeric 1``` contains a second parameter ```1``` which is used to test the **MCTS** method against the **complete method** via a **boxplot** as shown in the below image. Note that when testing against the **complete method**, the dataset should be small (the number of patterns is combinatorial). 

![](experiments/mcts/results/reducedFlags_numeric_6_200_0.5_jaccardSupportDescription/boxplot-RelativeFBeta.png?raw=true)

For the exhaustive list of Figures please launch simply the script [xp.sh](experiments/mcts/xp.sh). The list of results and Figures will be generated in [experiments/mcts/results](experiments/mcts/results) folder.

## [beam](experiments/beam)
This section give the results shown in the **section 7.5 (page 19)** of the [paper](paper/mlj17.pdf) using **beam search algorithm**. As in the beforehand section, in order to get the exhaustive list of figures, please launch [xp.sh](experiments/beam/xp.sh). Comment the undesired files before launching the script.

