# Fred https://github.com/mortada/fredapi
import pandas as pd
import world_bank_data as wb
from fredapi import Fred
class Economic:
  def __init__(self):
    self.key=None
  def interest(self,Country):
    #Appproach 1: FRED Daily Latest data https://fred.stlouisfed.org/series/REAINTRATREARAT1YE
    #Appproach 2:Indicator: FR.INR.RINR
    #Details Real interest rate (%)
    #wb.get_series('FR.INR.RINR')
    # Fetch the data as a Series
    series = wb.get_series('FR.INR.RINR', date='2000:2023')
    # Convert the Series to a DataFrame
    df = pd.DataFrame({'Value': series})
    # Reset the index to move 'Country' and 'Year' from the MultiIndex to regular columns
    df = df.reset_index()
    # Filter the DataFrame based on the specified country
    interestDF = df[df['Country'] == str(Country)]
    # Reset the index to remove the existing index and create a new default integer index
    interestDF = interestDF.reset_index(drop=True)
    # Drop the "Series" column from interestDF
    interestDF = interestDF.drop(columns='Series')
    # Sort the DataFrame in descending order based on the "Year" column
    interestDF = interestDF.sort_values(by='Year', ascending=False)
    return interestDF
  def inflation(self,Country):
    #Indicator: FP.CPI.TOTL.ZG 
    #Details Inflation, consumer prices (annual %)
    #wb.get_series('FP.CPI.TOTL.ZG')
    series=wb.get_series('FP.CPI.TOTL.ZG',date='2000:2023')
    # Convert the Series to a DataFrame
    df = pd.DataFrame({'Value': series})
    # Reset the index to move 'Country' and 'Year' from the MultiIndex to regular columns
    df = df.reset_index()
    # Filter the DataFrame based on the specified country
    inflationDF = df[df['Country'] == str(Country)]
    # Reset the index to remove the existing index and create a new default integer index
    inflationDF=inflationDF.reset_index(drop=True)
    # Drop the "Series" column from inflationDF
    inflationDF = inflationDF.drop(columns='Series')
    # Sort the DataFrame in descending order based on the "Year" column
    inflationDF = inflationDF.sort_values(by='Year', ascending=False)
    return inflationDF
  def fred_Data(self):
    fred = Fred(api_key=self.key)
    #data = fred.get_series_latest_release('GDP')
    data = fred.get_series_latest_release('REAINTRATREARAT10Y') #https://fred.stlouisfed.org/series/REAINTRATREARAT10Y 
    return data
  
      
      
