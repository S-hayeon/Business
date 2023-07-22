import streamlit as st
import pandas as pd

def main():
    st.title("Forex Risk Management Application")

    # Create or load the trade dataframe
    trade_data = load_trade_data()

    # User inputs for a new trade
    st.header("Enter New Trade")
    trade_date = st.date_input("Date")
    currency_pair = st.text_input("Currency Pair (e.g., EUR/USD)")
    strategy_used = st.text_input("Strategy Used")
    risk_to_reward_ratio = st.slider("Risk to Reward Ratio", min_value=1, max_value=5, value=2)
    risk_per_trade = st.number_input("Risk per Trade (%)", min_value=0.1, max_value=5.0, value=2.0, step=0.1)
    risk_tolerance = st.radio("Risk Tolerance", ["Low", "Medium", "High"])

    if st.button("Add Trade"):
        # Add the new trade to the dataframe
        trade_data = add_trade(trade_data, trade_date, currency_pair, strategy_used, risk_to_reward_ratio,
                               risk_per_trade, risk_tolerance)
        st.success("Trade added successfully!")

    # Calculate and display risk per trade and maximum exposure
    total_risk_capital = calculate_total_risk_capital(trade_data)
    risk_per_trade = (total_risk_capital * risk_per_trade) / 100
    maximum_exposure = risk_per_trade * total_risk_capital / 100

    st.header("Risk Management")
    st.write(f"Risk per Trade: {risk_per_trade:.2f} USD")
    st.write(f"Maximum Exposure: {maximum_exposure:.2f} USD")
    st.write(f"Risk Tolerance: {risk_tolerance}")

    # Calculate and display the count of trades and win-rate
    total_trades = len(trade_data)
    total_wins = sum(trade_data["Win"])
    win_rate = (total_wins / total_trades) * 100 if total_trades > 0 else 0

    st.header("Trades Summary")
    st.dataframe(trade_data)
    st.write(f"Total Trades: {total_trades}")
    st.write(f"Win-Rate: {win_rate:.2f}%")

    # Calculate and display the equity drawdown
    equity_drawdown = calculate_equity_drawdown(trade_data, total_risk_capital)
    st.header("Equity Drawdown")
    st.write(f"Equity Drawdown: {equity_drawdown:.2f}%")

    # Export the trade dataframe to an Excel file
    if st.button("Export Trades"):
        export_to_excel(trade_data)
        st.success("Trades exported to 'trades_data.xlsx'")

    # Provide a download link for the Excel file
    st.download_button("Download Trades Data", data=trade_data.to_csv(index=False), file_name="trades_data.csv", mime="text/csv")

def load_trade_data():
    try:
        trade_data = pd.read_excel("trades_data.xlsx")
    except FileNotFoundError:
        trade_data = pd.DataFrame(columns=["Date", "Currency Pair", "Strategy", "Risk to Reward Ratio",
                                           "Risk per Trade", "Risk Tolerance", "Win"])
    return trade_data

def add_trade(trade_data, date, currency_pair, strategy, risk_to_reward_ratio, risk_per_trade, risk_tolerance):
    win = st.radio("Trade Result", ["Win", "Loss"])
    trade_data = trade_data.append({
        "Date": date,
        "Currency Pair": currency_pair,
        "Strategy": strategy,
        "Risk to Reward Ratio": risk_to_reward_ratio,
        "Risk per Trade": risk_per_trade,
        "Risk Tolerance": risk_tolerance,
        "Win": win == "Win"
    }, ignore_index=True)
    return trade_data

def calculate_total_risk_capital(trade_data):
    return trade_data["Risk per Trade"].sum()

def calculate_equity_drawdown(trade_data, total_risk_capital):
    equity = total_risk_capital
    max_equity = total_risk_capital
    for index, trade in trade_data.iterrows():
        if trade["Win"]:
            equity += (trade["Risk per Trade"] / 100) * trade["Risk to Reward Ratio"] * total_risk_capital
        else:
            equity -= trade["Risk per Trade"]
        max_equity = max(max_equity, equity)
    equity_drawdown = ((max_equity - equity) / max_equity) * 100
    return equity_drawdown

def export_to_excel(trade_data):
    trade_data.to_excel("trades_data.xlsx", index=False)

if __name__ == "__main__":
    main()
