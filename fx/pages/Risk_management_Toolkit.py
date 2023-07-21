import streamlit as st

def main():
    st.title("Forex Risk Management Application")

    # User inputs for risk management elements
    risk_capital = st.number_input("Risk Capital (USD)", value=10000.0)
    risk_per_trade = st.slider("Risk per Trade (%)", min_value=0.1, max_value=5.0, value=2.0, step=0.1)
    risk_to_reward_ratio = st.slider("Risk to Reward Ratio", min_value=1, max_value=5, value=2)

    # Calculate maximum exposure based on risk per trade
    maximum_exposure = (risk_capital * risk_per_trade) / 100

    # User input for risk tolerance
    risk_tolerance = st.radio("Risk Tolerance", ["Low", "Medium", "High"])

    # Display calculated maximum exposure and risk tolerance
    st.write(f"Maximum Exposure: {maximum_exposure:.2f} USD")
    st.write(f"Risk Tolerance: {risk_tolerance}")

    # Equity drawdown and win-rate inputs
    equity_drawdown = st.number_input("Equity Drawdown (%)", value=10.0)
    win_rate = st.slider("Win-Rate (%)", min_value=50, max_value=100, value=70)

    # Display analysis based on equity drawdown and win-rate
    st.write(f"Equity Drawdown: {equity_drawdown:.2f}%")
    st.write(f"Win-Rate: {win_rate}%")

    # Provide suggestions based on the analysis
    if equity_drawdown > 20.0:
        st.warning("High equity drawdown! Consider reevaluating your risk management.")
    elif win_rate < 60:
        st.warning("Low win-rate! Review your trading strategy for potential improvements.")
    else:
        st.success("Your risk management and trading strategy seem on track for success!")

if __name__ == "__main__":
    main()
