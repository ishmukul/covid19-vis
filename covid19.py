import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from timeit import default_timer as timer

# Create plot directory, if it does not exist
if not os.path.exists('./plots'):
    os.makedirs('./plots')

# url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series" \
#       "/time_series_19-covid-Confirmed.csv "

plt.close('all')
Dpi = 150  # Pixel count for figures
FlagFigCountry = 1
FlagFigProvince = 1
FlagFigWorld = 1
FlagFig = 1
if FlagFig == 0:
    FlagFigWorld = FlagFigCountry = FlagFigProvince = 0

# FigNum = 0  # Redundant. A counter for Figure number. Add FigNum+=1 at the start of each figure.

# File readout here
FilePath_Confirmed = './data/time_series_19-covid-Confirmed.csv'
DataConfirmed = pd.read_csv(FilePath_Confirmed)

FilePath_Deaths = './data/time_series_19-covid-Deaths.csv'
DataDeaths = pd.read_csv(FilePath_Deaths)

FilePath_Recovered = './data/time_series_19-covid-Recovered.csv'
DataRecovered = pd.read_csv(FilePath_Recovered)

# Diagnostic checks. Uncomment if required.
# print(DataConfirmed.describe())
# print(DataDeath.describe())
# print(DataRecovered.describe())

# Index of Latitude, Longitude, Province/State, Country/Region
IndexLong = DataConfirmed.columns.get_loc('Long')  # Index of Longitude in Column header
IndexLat = DataConfirmed.columns.get_loc('Lat')  # Index of Latitude in Column header
IndexCountry = DataConfirmed.columns.get_loc('Country/Region')  # Index of Country/Region in Column header
IndexProvince = DataConfirmed.columns.get_loc('Province/State')  # Index of Province/State in Column header
IndexDate = IndexLong + 1  # Date of 22 Jan 2020, This index can be change to reset the starting date in plots
LastDate = DataConfirmed.columns[-1]


# Some functions defined here that will be used in future
# Visualization

def plot_fig_country(data1, data2, data3, country, savefig):
    plt.figure(figsize=plt.figaspect(0.8), dpi=Dpi)
    norm = 1000.0
    # Let's calculate number of days from 22 Jan 2020 (First date in this dataset) = len(data1)
    # It is assuming that dataset was updated everyday and it has record for each date.
    plt.plot(range(len(data1)), data1 / norm, '-k', Linewidth=3, label='Confirmed')
    plt.plot(range(len(data2)), data2 / norm, '-r', Linewidth=3, label='Deaths')
    plt.plot(range(len(data3)), data3 / norm, '-g', Linewidth=3, label='Recovered')
    plt.xlim([0, len(data1) + 1])
    plt.xlabel('# of Days from %s' % DataConfirmed.columns[IndexDate])
    plt.ylabel('# of Cases (in multiples of %dK)' % int(norm / 1000))
    plt.title('# of COVID-19 cases in %s' % country)
    plt.legend(loc='best')
    if savefig == 1:
        country = country.replace("*", "")  # added because some countries has * in their name
        filename = country + '.png'
        plt.savefig("./plots/" + filename)  # FIle saving
    plt.close()
    return 0


def plot_fig_province(data1, data2, data3, country, province, savefig):
    plt.figure(figsize=plt.figaspect(0.8), dpi=Dpi)
    norm = 1.0
    # Let's calculate number of days from 22 Jan 2020 (First date in this dataset) = len(data1)
    # It is assuming that dataset was updated everyday and it has record for each date.
    plt.plot(range(len(data1)), data1 / norm, '-k', Linewidth=3, label='Confirmed')
    plt.plot(range(len(data2)), data2 / norm, '-r', Linewidth=3, label='Deaths')
    plt.plot(range(len(data3)), data3 / norm, '-g', Linewidth=3, label='Recovered')
    plt.xlim([0, len(data1) + 1])
    plt.xlabel('# of Days from %s' % DataConfirmed.columns[IndexDate])
    plt.ylabel('# of Cases')
    plt.title('# of COVID-19 cases in %s' % province)
    plt.legend(loc='best')
    if savefig == 1:
        country = country.replace("*", "")  # added because some countries has * in their name
        filename = country + '_' + province + '.png'
        plt.savefig("./plots/" + filename)  # FIle saving
    plt.close()
    return 0


def get_world_data(data1, data2, data3, start_date_index):
    data_confirmed = data1.sum()[start_date_index:]
    data_deaths = data2.sum()[start_date_index:]
    data_recovered = data3.sum()[start_date_index:]
    return data_confirmed, data_deaths, data_recovered


def get_country_data(data1, data2, data3, country_name, start_date_index):
    data_confirmed = data1[data1['Country/Region'] == country_name].sum()[start_date_index:]
    data_deaths = data2[data2['Country/Region'] == country_name].sum()[start_date_index:]
    data_recovered = data3[data3['Country/Region'] == country_name].sum()[start_date_index:]
    return data_confirmed, data_deaths, data_recovered


def get_province_data(data1, data2, data3, province_name, start_date_index):
    data_confirmed = data1[data1['Province/State'] == province_name].sum()[start_date_index:]
    data_deaths = data2[data2['Province/State'] == province_name].sum()[start_date_index:]
    data_recovered = data3[data3['Province/State'] == province_name].sum()[start_date_index:]
    return data_confirmed, data_deaths, data_recovered


# Analysing full world data set by summing all the counts.
# World variable
start_time = timer()
# Use functions defined above and get world data
WorldConfirmed, WorldDeaths, WorldRecovered = get_world_data(DataConfirmed, DataDeaths, DataRecovered, IndexDate)

# Visualization
if FlagFigWorld == 1:
    plot_fig_country(WorldConfirmed, WorldDeaths, WorldRecovered, 'World', 1)  # Plot world data

end_time = timer()
print('Time taken for processing world data %0.3f seconds.' % (end_time - start_time))

# Analyze individual countries
CaseThreshold = 100
CountryList = DataConfirmed[DataConfirmed[LastDate] > CaseThreshold]['Country/Region'].value_counts().index
print('\nNumber of countries with more than %d cases is %d. \n' % (CaseThreshold, len(CountryList)))
# CountryList = ["Canada", "US"]  # Adding individual countries of interest
# CountryList = DataConfirmed['Country/Region'].value_counts().index  # Calculates full country list

start_time = timer()
for Country in CountryList:
    start_time_ind = timer()
    CountryConfirmed, CountryDeaths, CountryRecovered = get_country_data(DataConfirmed, DataDeaths, DataRecovered,
                                                                         Country, IndexDate)
    if FlagFigCountry == 1:
        plot_fig_country(CountryConfirmed, CountryDeaths, CountryRecovered, Country, 1)

    end_time_ind = timer()
    print("Country:%s, Confirmed:%d, Deaths:%d, Recovered:%d, Processing time:%0.3f s. "
          % (Country, CountryConfirmed[-1], CountryDeaths[-1], CountryRecovered[-1], (end_time_ind - start_time_ind)))

print('\n')
for Country in CountryList:
    start_time_ind = timer()
    ProvinceList = DataConfirmed[DataConfirmed['Country/Region'] == Country]['Province/State']
    ProvinceList = ProvinceList.dropna()
    for Province in ProvinceList:
        ProvinceConfirmed, ProvinceDeaths, ProvinceRecovered = get_province_data(DataConfirmed, DataDeaths,
                                                                                 DataRecovered, Province, IndexDate)
        if FlagFigProvince == 1:
            plot_fig_province(ProvinceConfirmed, ProvinceDeaths, ProvinceRecovered, Country, Province, 1)

        end_time_ind = timer()
        print("Province:%s, Confirmed:%d, Deaths:%d, Recovered:%d, Processing time:%0.3f s. "
              % (Province, ProvinceConfirmed[-1], ProvinceDeaths[-1], ProvinceRecovered[-1],
                 (end_time_ind - start_time_ind)))

end_time = timer()
print('Total time taken for plotting is %0.3f seconds.' % (end_time - start_time))
