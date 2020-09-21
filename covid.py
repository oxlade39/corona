import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats


def get_data(url: str, value_name: str) -> pd.DataFrame:
    df = pd.read_csv(url).drop(columns=["Lat", "Long"])
    time_series = pd.melt(df, id_vars=['Country/Region', 'Province/State'], var_name='Date', value_name=f"Cum. {value_name}")
    time_series['Province/State'] = time_series['Province/State'].fillna('N/A')
    time_series['Date'] = pd.to_datetime(time_series['Date'])
    time_series.sort_values(by=['Country/Region', 'Province/State', 'Date'], inplace=True)
    time_series[value_name] = time_series.groupby(['Country/Region', 'Province/State'])[f"Cum. {value_name}"].diff().fillna(0)
    return time_series


def get_combined_covid_data(country: str, province: str = 'N/A') -> pd.DataFrame:
    cases_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
    deaths_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
    combined = pd.merge(
        get_data(cases_url, 'Cases'), 
        get_data(deaths_url, 'Deaths'), 
        on=['Country/Region', 'Province/State', 'Date'])

    return combined.loc[(combined['Country/Region'] == country) & (combined['Province/State'] == province)].reset_index(drop=True)