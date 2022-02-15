# Race-Prediction
# 1. About
This repository is for the horse race prediction. </br>
Also, this reoisitory is totally for private use.  </br>
**Horse Race: Basically, it is a kind of gamble, we predict the fastest horse in the race.**</br>

These files are mostly written in Python and run on Jupyter Notebook. </br>
The following libraries are used; </br>  
- **Requests**
- **BeautifulSoup**
- **Selenium** 
- **Pandas** 
- **Numpy** 
- **Scikit-Learn**
- **Tensorflow** 
- **Matplotlib**
  

# 2. Overview (ideas)
1. *Scraping* </br>
The first step is to get race data with results from this Web site (https://www.netkeiba.com/). </br>
Finally, the temporory pure race data csv file are made through the following procedure; </br>

- get all url of race and horse data 
- save all race and horse data html 
- scrape necessary data from these html files 
</br>

2. *Making data* </br>
After creating initial race and horse data csv files, purified and sofisticated data are created. </br>
For example, the pedigree and previous race results of the horse are considered.  </br>
 </br>
 
3. *Creating models* </br>
I created two types of model. </br>

+ **ResRace**: &emsp;&ensp;it is based on Resnet, which has skipping connections, but ResRace completely consists of </br>
  &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;fully-connected layers (multilayer perceptrons) , not CNN.  
+ **TransRace**:&emsp;it is based on Transformer, which has self-attention architecture, so the data should be </br>
  &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;a sequential shape. This point is challenging for me. 
</br>

4. *Predict* </br>
The most ambitious object is to predict the results of upcoming race to win horse voting tickets, </br>
using above pre-trianed models.  </br>

# 3. Implementation
1. *data_setup* </br>
To set up the final train data </br>

+ **main.ipynb**:&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;To get url, to open html, and to create csv files 
+ **purify_(horse/race)_ data.ipynb**:&emsp;To extract and adjust data 
+ **make_train_data.ipynb**:&emsp;&emsp;&emsp;&emsp;&emsp;To make the final train data 


2. *models* </br>
Each file is a distinct model </br>

+ **resnet.py**:&emsp;&emsp;&emsp;&ensp;it is ResRace. 
+ **transformer.py**:&emsp;it is TransRace. 


3. *training* </br>
To run and train models </br>

+ **resnet_train.ipynb**:&emsp;&emsp;&emsp;&ensp;it is for training ResRace model. 
+ **transformer_train.ipynb**:&emsp;it is for training TransRace model. 


4. *prediction* </br>
To predict the upcoming weekend race. </br>
