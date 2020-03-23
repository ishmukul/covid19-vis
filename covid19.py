import pandas as pd
import matplotlib.pyplot as plt
import os
from timeit import default_timer as timer

plt.close('all')  # Close any existing plot
Dpi = 150  # Pixel count for figures
FlagFig = 1  # Flag for activating all figure flags
if FlagFig == 0:
    FlagFigWorld = FlagFigCountry = FlagFigProvince = 0  # Condition for not plotting any figure
else:
    FlagFigCountry = 1  # flag for plotting Country
    FlagFigProvince = 1  # Flag for plotting Province
    FlagFigWorld = 1  # Flag for plotting World

# Create plot directory, if it does not exist
if not os.path.exists('./plots'):
    os.makedirs('./plots')
if not os.path.exists('./csv_out'):
    os.makedirs('./csv_out')

# Reading time series data. Data is in three separate files for confirmed cases, Cases that resulted in Deaths,
# and cases that recovered
# Confirmed cases
FilePath_Confirmed = './data/time_series_19-covid-Confirmed.csv'
DataConfirmed = pd.read_csv(FilePath_Confirmed)

# Death cases
FilePath_Deaths = './data/time_series_19-covid-Deaths.csv'
DataDeaths = pd.read_csv(FilePath_Deaths)

# Recovered cases
FilePath_Recovered = './data/time_series_19-covid-Recovered.csv'
DataRecovered = pd.read_csv(FilePath_Recovered)

# Diagnostic checks. Uncomment if required.
# print(DataConfirmed.describe())
# print(DataDeath.describe())
# print(DataRecovered.describe())

# Now I will pick indexes for the data file. These indexes will be helpful in shortening code lines.
# These are common in all three files. Therefore, common for all feature extraction.
# IndexDate is important as it defines number of days to start data extraction. As an example 1 will start from when
# data is available, and 20 will add 20 days in the cut-off. One may be interested in just analysing last 10 days and in
# that case, adjust this number accordingly.
# Index of Latitude, Longitude, Province/State, Country/Region
IndexLong = DataConfirmed.columns.get_loc('Long')  # Index of Longitude in Column header
IndexLat = DataConfirmed.columns.get_loc('Lat')  # Index of Latitude in Column header
IndexCountry = DataConfirmed.columns.get_loc('Country/Region')  # Index of Country/Region in Column header
IndexProvince = DataConfirmed.columns.get_loc('Province/State')  # Index of Province/State in Column header
IndexDate = IndexLong + 1  # Date of 22 Jan 2020, This index can be change to reset the starting date in plots
LastDate = DataConfirmed.columns[-1]


# Define some functions here

# ============================================
# Extracting world data by summing all indices.
def get_world_data(data1, data2, data3, start_date_index):
    data_confirmed = data1.sum()[start_date_index:]
    data_deaths = data2.sum()[start_date_index:]
    data_recovered = data3.sum()[start_date_index:]
    return data_confirmed, data_deaths, data_recovered


# ============================================
# Extracting data for individual countries
def get_country_data(data1, data2, data3, country_name, start_date_index):
    data_confirmed = data1[data1['Country/Region'] == country_name].sum()[start_date_index:]
    data_deaths = data2[data2['Country/Region'] == country_name].sum()[start_date_index:]
    data_recovered = data3[data3['Country/Region'] == country_name].sum()[start_date_index:]
    return data_confirmed, data_deaths, data_recovered


# ============================================
# Extracting data for each province, if available. e.g. US and Canada
def get_province_data(data1, data2, data3, province_name, start_date_index):
    data_confirmed = data1[data1['Province/State'] == province_name].sum()[start_date_index:]
    data_deaths = data2[data2['Province/State'] == province_name].sum()[start_date_index:]
    data_recovered = data3[data3['Province/State'] == province_name].sum()[start_date_index:]
    return data_confirmed, data_deaths, data_recovered


# ============================================
# Write data to csv files. One file will generated for each execution.
# Format is: Rows=Cases; Columns=Date,Confirmed,Deaths,Recovered
def write_data_csv(data1, data2, data3, name):
    a = pd.concat([data1, data2, data3], axis=1)
    a.index.name = 'Date'
    a.columns = ['Confirmed', 'Deaths', 'Recovered']
    name = name.replace("*", "")  # added because some names has * in their name
    name = name.replace(",", "")  # added because some names has , in their name
    name = name.replace(" ", "_")  # added because some names has _ in their name
    filename = name + '.csv'
    a.to_csv("./csv_out/" + filename)


# ============================================
# Visualization: plotting all three cases in a single plot.
def plot_fig(data1, data2, data3, name, save_option):
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
    plt.title('# of COVID-19 cases in %s' % name)
    plt.legend(loc='best')
    if save_option == 1:
        name = name.replace("*", "")  # added because some names has * in their name
        name = name.replace(",", "")  # added because some names has , in their name
        name = name.replace(" ", "_")  # added because some names has space in their name

        filename = name + '.png'
        plt.savefig("./plots/" + filename)  # FIle saving
    plt.close()  # Had to use this in iPython. Number of graphs in memory exploded. Will search for some better method.
    return 0


# Time to use functions
# ============================================
# World data
start_time = timer()  # A timer
# Get world data
WorldConfirmed, WorldDeaths, WorldRecovered = get_world_data(DataConfirmed, DataDeaths, DataRecovered, IndexDate)
write_data_csv(WorldConfirmed, WorldDeaths, WorldRecovered, 'World')
if FlagFigWorld == 1:
    plot_fig(WorldConfirmed, WorldDeaths, WorldRecovered, 'World', 1)  # Plot world data

end_time = timer()
print('Time taken for processing world data %0.3f seconds.' % (end_time - start_time))

# ============================================
# Analyze individual countries
CaseThreshold = 100  # Select countries if this number of cases occurred on last date of data
CountryList = DataConfirmed[DataConfirmed[LastDate] > CaseThreshold]['Country/Region'].value_counts().index
print('\nNumber of countries with more than %d cases is %d. \n' % (CaseThreshold, len(CountryList)))
# CountryList = ["Canada", "US"]  # Adding individual countries of interest
# CountryList = DataConfirmed['Country/Region'].value_counts().index  # Calculates full country list

start_time = timer()
for Country in CountryList:
    start_time_ind = timer()
    CountryConfirmed, CountryDeaths, CountryRecovered = get_country_data(DataConfirmed, DataDeaths, DataRecovered,
                                                                         Country, IndexDate)
    FileName = Country
    write_data_csv(CountryConfirmed, CountryDeaths, CountryRecovered, FileName)
    if FlagFigCountry == 1:
        plot_fig(CountryConfirmed, CountryDeaths, CountryRecovered, FileName, 1)

    end_time_ind = timer()
    print("Country:%s, Confirmed:%d, Deaths:%d, Recovered:%d, Processing time:%0.3f s. "
          % (FileName, CountryConfirmed[-1], CountryDeaths[-1], CountryRecovered[-1], (end_time_ind - start_time_ind)))

print('\n')
# ============================================
# Analyze for Provinces
for Country in CountryList:
    start_time_ind = timer()
    ProvinceList = DataConfirmed[DataConfirmed['Country/Region'] == Country]['Province/State']
    ProvinceList = ProvinceList.dropna()
    for Province in ProvinceList:
        ProvinceConfirmed, ProvinceDeaths, ProvinceRecovered = get_province_data(DataConfirmed, DataDeaths,
                                                                                 DataRecovered, Province, IndexDate)
        FileName = Country + '_' + Province
        write_data_csv(ProvinceConfirmed, ProvinceDeaths, ProvinceRecovered, FileName)
        if FlagFigProvince == 1:
            plot_fig(ProvinceConfirmed, ProvinceDeaths, ProvinceRecovered, FileName, 1)

        end_time_ind = timer()
        print("Province:%s, Confirmed:%d, Deaths:%d, Recovered:%d, Processing time:%0.3f s. "
              % (FileName, ProvinceConfirmed[-1], ProvinceDeaths[-1], ProvinceRecovered[-1],
                 (end_time_ind - start_time_ind)))

end_time = timer()
# ============================================
# Print total time
print('Total time taken for plotting is %0.3f seconds.' % (end_time - start_time))
