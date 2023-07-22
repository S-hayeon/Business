import streamlit as st
import pandas as pd

def main():
    st.title("Forex Risk Management Application")

    # Create or load the trade dataframe
    trade_data = load_trade_data()

    # User inputs for a new trade
    st.header("Enter New Trade")
    trade_dates = st.date_input("Date", [], key="dates")
    currency_pairs = st.text_input("Currency Pair (e.g., EUR/USD)", "", key="currency_pairs")
    strategy_useds = st.text_input("Strategy Used", "", key="strategies")
    risk_to_reward_ratios = st.slider("Risk to Reward Ratio", min_value=1, max_value=5, value=2, key="rr_ratios")
    risk_per_trades = st.number_input("Risk per Trade (%)", min_value=0.1, max_value=5.0, value=2.0, step=0.1, key="risk_per_trade")
    risk_tolerances = st.radio("Risk Tolerance", ["Low", "Medium", "High"], key="risk_tolerance")

    if st.button("Add Trade"):
        # Convert the multi-select inputs to lists
        trade_dates = list(trade_dates) if isinstance(trade_dates, tuple) else [trade_dates]
        currency_pairs = currency_pairs.split(",")
        strategy_useds = strategy_useds.split(",")

        # Convert risk_to_reward_ratios to a list
        risk_to_reward_ratios = [risk_to_reward_ratios] * len(trade_dates)

        # Add the new trade(s) to the dataframe
        for date, currency_pair, strategy_used, risk_to_reward_ratio in zip(
            trade_dates, currency_pairs, strategy_useds, risk_to_reward_ratios
        ):
            add_trade(trade_data, date, currency_pair.strip(), strategy_used.strip(),
                      risk_to_reward_ratio, risk_per_trades, risk_tolerances)
        st.success("Trade(s) added successfully!")

    # Calculate and display risk per trade and maximum exposure
    total_risk_capital = calculate_total_risk_capital(trade_data)
    risk_per_trade = (total_risk_capital * risk_per_trades) / 100
    maximum_exposure = risk_per_trade * total_risk_capital / 100

    st.header("Risk Management")
    st.write(f"Risk per Trade: {risk_per_trade:.2f} USD")
    st.write(f"Maximum Exposure: {maximum_exposure:.2f} USD")
    st.write(f"Risk Tolerance: {risk_tolerances}")

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

    # Import trades from an Excel file
    import_file = st.file_uploader("Import Trade Data (Excel)", type=["xlsx"])
    if import_file is not None:
        trade_data = pd.read_excel(import_file)
        st.success("Data successfully imported")

    # Export the trade dataframe to an Excel file
    df=export_to_excel(trade_data)
    # Provide a download link for the Excel file
    st.download_button("Download Trades Data", data=df, file_name="trades_data.xlsx", mime="text/xlsx")
    #st.download_button("Download Trades Data", data=trade_data.to_csv(index=False), file_name="trades_data.csv", mime="text/csv")
    st.success("Trades exported to 'trades_data.xlsx'")

def load_trade_data():
    try:
        trade_data = pd.read_excel("trades_data.xlsx")
    except FileNotFoundError:
        trade_data = pd.DataFrame(columns=["Date", "Currency Pair", "Strategy", "Risk to Reward Ratio",
                                           "Risk per Trade", "Risk Tolerance", "Win"])
    return trade_data

def add_trade(trade_data, date, currency_pair, strategy, risk_to_reward_ratio, risk_per_trade, risk_tolerance):
    win = st.radio("Trade Result", ["Win", "Loss"])
    new_trade = {
        "Date": date,
        "Currency Pair": currency_pair,
        "Strategy": strategy,
        "Risk to Reward Ratio": risk_to_reward_ratio,
        "Risk per Trade": risk_per_trade,
        "Risk Tolerance": risk_tolerance,
        "Win": win == "Win"
    }
    trade_data.loc[len(trade_data)] = new_trade
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

    # Avoid division by zero
    if max_equity == 0:
        return 0

    equity_drawdown = ((max_equity - equity) / max_equity) * 100
    return equity_drawdown

def export_to_excel(trade_data):
    df=trade_data.to_excel("trades_data.xlsx", index=False)
    return df

if __name__ == "__main__":
    main()
