import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# Read the crpto data
data = st.session_state['DataFrame']
volume_data=data.Volume.values.reshape(-1,1)
close_data=data.Close.values.reshape(-1,1)
random_variable=42
volume_train,volume_test,close_train,close_test=train_test_split(volume_data,close_data,test_size=0.3,random_state=random_variable)
print("Training and Test data updated successfully")
#btc_close_test_data = data_test.Close.values.reshape(-1, 1)

# Fit the KNN model
KNN_model = KNeighborsRegressor(n_neighbors=3).fit(volume_train, close_train)
closeData_KNN_predict = KNN_model.predict(close_test)

# Calculate metrics
MSE = mean_squared_error(close_test, closeData_KNN_predict)
R2_Score = round((r2_score(close_test, closeData_KNN_predict))*100,3)

# Create a Streamlit app
st.title(f"Artificial Intelligence Price Predictions")
with st.expander(f"{st.session_state['CoinPair']} AI Price Predictions"):
    st.write("Predicted prices using K-Nearest Neighbors Regressor")
    # st.write(f"Mean Squared Error: {MSE}")
    st.write(f"Accuracy Score% : {R2_Score}")
    # Display the plot
    st.header("Scatter Plot of AI Predicted vs Actual Price ")
    plt.scatter(close_test, closeData_KNN_predict, label='AI Predictions')
    plt.title(f"{st.session_state['CoinPair']} Actual and Predicted data")
    plt.xlabel('Close Test Data')
    plt.ylabel('Predicted Close Data')
    plt.legend()
    #plt.show()
    st.pyplot(plt)
    st.header("Scatter Plot of Actual and Predicted Close Prices vs Volume with Viridis Colormap")
    plt.scatter(volume_test, close_test, c=close_test, cmap='viridis', label='Actual Data')
    plt.scatter(volume_test, closeData_KNN_predict, c=closeData_KNN_predict, marker='x', cmap='viridis', label='Predicted Data')
    plt.xlabel('Volume')
    plt.ylabel('Close')
    plt.legend()
    st.pyplot(plt)
    # Create a DataFrame
    # predictions_table = pd.DataFrame({"Open": open_data,"Close": close_data,"Close (Predicted)": closeData_KNN_predict})
    #predictions_table = pd.DataFrame({"Close (Predicted)": closeData_KNN_predict, "Actual Close (Test)": close_test})
    predictions_table = pd.DataFrame({
    "Close (Predicted)": closeData_KNN_predict.flatten(),
    "Actual Close (Test)": close_test.flatten()
})
    

    # Optionally, display more details
    if st.checkbox("Show Data Details"):
        st.write(f"{st.session_state['CoinPair']} Price Predictions Data Table")
        #st.dataframe(closeData_KNN_predict)
        st.dataframe(predictions_table)

