import pandas as pd
import worldbank as wb
class Economic:
  def interest(self,Country):
    #Appproach 1: FRED Daily Latest data https://fred.stlouisfed.org/series/REAINTRATREARAT1YE
    #Appproach 2:Indicator: FR.INR.RINR
    #Details Real interest rate (%)
    #wb.get_series('FR.INR.RINR')
    series=pd.DataFrame(wb.get_series('FR.INR.RINR',date='2000:2023'))
    # Filter the DataFrame based on the specified country
    interestDF = series[series['Country'] == str(Country)]
    return interestDF
  def inflation(self,Country):
    #Indicator: FP.CPI.TOTL.ZG 
    #Details Inflation, consumer prices (annual %)
    #wb.get_series('FP.CPI.TOTL.ZG')
    series=pd.DataFrame(wb.get_series('FP.CPI.TOTL.ZG',date='2000:2023'))
    # Filter the DataFrame based on the specified country
    inflationDF = series[series['Country'] == str(Country)]
    return inflationDF
      
      
