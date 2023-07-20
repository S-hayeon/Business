import streamlit as st
import sys
sys.path.append('/app/business')
from economic import Economic
from fx import main

if st.session_state["CurrencyPair"]=="":
  st.write("Enter FX currency pair to proceed!!")
else:
  def get_country_and_currency_from_pair(currency_pair):
    # Extract the first three characters as the first currency code and the last three as the second currency code
    currency1, currency2 = currency_pair[:3], currency_pair[-3:]

    # Search for the country corresponding to currency1 in the dictionary
    country1 = None
    for country, code in main.country_currencyPair.items():
        if code == currency1:
            country1 = country
            break

    # Search for the country corresponding to currency2 in the dictionary
    country2 = None
    for country, code in main.country_currencyPair.items():
        if code == currency2:
            country2 = country
            break

    # Check if the currency pair contains 'EUR' and store the associated countries in a list
    countries_with_eur = []
    if 'EUR' in currency_pair:
        for country, code in main.country_currencyPair.items():
            if code == 'EUR':
                countries_with_eur.append(country)

    return country1, currency1, country2, currency2, countries_with_eur
  country1, currency1, country2, currency2, countries_with_eur = get_country_and_currency_from_pair(st.session_state["CurrencyPair"])
  economic=Economic()
  interest1=economic.interest(country1)
  inflation1=economic.inflation(country1)
  interest2=economic.interest(country2)
  inflation2=economic.inflation(country2)
  # Use st.beta_columns to create two columns for displaying DataFrames side by side
  col1, col2 = st.columns(2)
  # Display the DataFrames in each column
  with col1:
    st.header(f"Currency 1: {currency1}")
    st.write("Interest Rates")
    st.dataframe(interest1)
    st.write("Inflation Rates")
    st.dataframe(inflation1)
  with col2:
    st.header(f"Currency 2: {currency2}")
    st.write("Interest Rates")
    st.dataframe(interest2)
    st.write("Inflation Rates")
    st.dataframe(inflation2)
  if 'EUR' in st.session_state["CurrencyPair"]:
    for country in countries_with_eur:
      st.write("Showing data for Europe")
      st.write("Interest Rates")
      interest=economic.interest(country)
      st.dataframe(interest)
      st.write("Inflation Rates")
      inflation=economic.inflation(country)
      st.dataframe(inflation)

