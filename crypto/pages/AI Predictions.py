import streamlit as st
import pandas as pd
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# Read the BTC data
df = st.session_state['DataFrame']
rows_count = len(df.index)

# Conventional 70-30 rule for training and validation data set
train_rows = int(0.7 * rows_count)
test_rows = int(0.3 * rows_count)
data = df.tail(rows_count)
data_test = df.head(test_rows)

open_data = data.Open.values.reshape(-1, 1)
close_data = data.Close.values.reshape(-1, 1)
#btc_close_test_data = data_test.Close.values.reshape(-1, 1)

# Fit the KNN model
KNN_model = KNeighborsRegressor(n_neighbors=3).fit(open_data, close_data)
closeData_KNN_predict = KNN_model.predict(open_data)

# Calculate metrics
MSE = mean_squared_error(close_data, closeData_KNN_predict)
R2_Score = r2_score(close_data, closeData_KNN_predict)

# Create a Streamlit app
st.title("BTC-USDT Predicted Data")
st.write("Predicted prices using K-Nearest Neighbors Regressor")
st.write(f"Mean Squared Error: {MSE}")
st.write(f"R-squared (R2) Score: {R2_Score}")

# Display the plot
plt.title("BTC-USDT Predicted data")
plt.scatter(open_data, closeData_KNN_predict, label='Predicted data')
st.pyplot(plt)

# Optionally, display more details
if st.checkbox("Show Data Details"):
    st.write("BTC Open Data:")
    st.write(open_data)
    st.write("BTC Close Data:")
    st.write(close_data)
    st.write("Predicted Close Data:")
    st.write(closeData_KNN_predict)
