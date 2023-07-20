from economic import Economic
from fx import main
import streamlit as st
import sys
sys.path.append('/app/business')
if st.session_state["CurrencyPair"]=="":
  st.write("Enter FX currency pair to proceed!!")
else:
  def get_country_and_currency_from_pair(currency_pair):
    # Extract the first three characters as the first currency code and the last three as the second currency code
    currency1, currency2 = currency_pair[:3], currency_pair[-3:]

    # Search for the country corresponding to currency1 in the dictionary
    country1 = None
    for country, code in main.country_currency_pair.items():
        if code == currency1:
            country1 = country
            break

    # Search for the country corresponding to currency2 in the dictionary
    country2 = None
    for country, code in main.country_currency_pair.items():
        if code == currency2:
            country2 = country
            break

    # Check if the currency pair contains 'EUR' and store the associated countries in a list
    countries_with_eur = []
    if 'EUR' in currency_pair:
        for country, code in main.country_currency_pair.items():
            if code == 'EUR':
                countries_with_eur.append(country)

    return country1, currency1, country2, currency2, countries_with_eur
  country1, currency1, country2, currency2, countries_with_eur = get_country_and_currency_from_pair(st.session_state["CurrencyPair"])
  economic=Economic()
  st.write(interest=economic.interest(country1))
  st.write(inflation=economic.inflation(country1))
  st.write(interest=economic.interest(country2))
  st.write(inflation=economic.inflation(country2))
  if 'EUR' in st.session_state["CurrencyPair"]:
    for country in countries_with_eur:
      st.write(interest=economic.interest(country))
      st.write(inflation=economic.inflation(country1))

