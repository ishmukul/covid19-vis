# Time-series data for COVID-19 cases

Time-series data downloaded from:
Novel Coronavirus (COVID-19) Cases, provided by John Hopkins University CSSE github account. 
All details regarding data are provided in the link below.  
https://github.com/CSSEGISandData/COVID-19

# Data extraction for COVID-19 cases
This script extracts data for confirmed cases, cases that resulted in deaths, and recovered cases for each country 
and province, and writes data into a separate csv file.   

Visualization: Plots line plots for each country and province.  
Pie charts: Plots pie chart for countries with Province data.  

Directory structure:  
Readme.md : This Readme file.  
covid19.py : Main python script for processing data.  
data: Folder with data from CSSE account.  
csv_out: Folder with output csv files. Filename are Country_Province.csv  
plots: generated plots from this script. Filename are Country_Province.csv, e.g. [Canada.png](https://github.com/ishmukul/covid19-vis/blob/master/plots/Canada.png)   
pie_chart: generated pie charts for countries with province/state data. Filename are Country_Name.png, e.g. [Canada.png](https://github.com/ishmukul/covid19-vis/blob/master/pie_chart/Canada.png)  

<img src="https://github.com/ishmukul/covid19-vis/blob/master/plots/Canada.png" alt="Cases in Canada" width="400"/>
<img src="https://github.com/ishmukul/covid19-vis/blob/master/pie_chart/Canada.png" alt="Cases in Canada" width="400"/>

## Update:  
This script was written before data format change for US. Therefore, this script doe not update data for US.
