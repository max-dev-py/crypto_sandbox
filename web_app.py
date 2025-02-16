import streamlit as st
import pandas as pd

from dummy_robot.price_fetcher import get_ccxt_df
from dummy_robot.strategy_tester import analyze_robot_trading
from dummy_robot.cinco import CincoRobot

st.set_page_config(page_title='Crypto-looser strategy simulator!',
                   # page_icon=None,
                   page_icon=":crypto:",
                   layout="wide",
                   initial_sidebar_state="auto",
                   menu_items=None
                   )


@st.cache_data  # 👈 Add the caching decorator
def load_data(symbol, timeframe="1d", limit=1000):
    df = get_ccxt_df(symbol=symbol, timeframe=timeframe, limit=limit)
    return df


if 'ticker' not in st.session_state:
    st.session_state.ticker = "BTC/USDT"

if 'timeframe' not in st.session_state:
    st.session_state.timeframe = "1d"

if 'price_limit' not in st.session_state:
    st.session_state.price_limit = 1000

df = load_data(
    symbol=st.session_state.ticker,
    timeframe=st.session_state.timeframe,
    limit=int(st.session_state.price_limit)
)

with (st.sidebar):
    st.header("Assumptions:")
    st.text_input("Ticker", key="ticker", help='Crypto ticker')
    st.radio("Time-frame", ['1d', '1h'], key="timeframe", help='Price frequency', )
    st.number_input("Price limit", key="price_limit", help='Price limit', step=1)
    st.number_input("Initial amount", key="amount", value=10000, help='Money amount')
    st.number_input("Buy rate", key="buy_rate", value=5.0, help='Buy rate.%', format='%.2f')
    st.number_input("Profit rate", key="profit_rate", value=5.0, help='Profit rate%', format='%.2f')
    st.number_input("Save rate", key="save_rate", value=5.0, format='%.2f', step=0.1,
                    help='Which part of crypto-currency will not be sold. %')
    st.number_input("Investment rate", key="amount_rate", value=5.0,
                    help='Which part of amount will be invested.%', format='%.2f', step=0.1)
    start_date = pd.to_datetime(
        st.date_input(
            "Choose first investment date:",
            df.timestamp.min(),
            min_value=df.timestamp.min(),
            max_value=df.timestamp.max(),
        )
    )
    end_date = pd.to_datetime(
        st.date_input(
            "Choose finish investment date:",
            df.timestamp.max(),
            min_value=df.timestamp.min(),
            max_value=df.timestamp.max(),
        )
    )

norm_result = analyze_robot_trading(df[df.timestamp >= start_date][df.timestamp <= end_date],
                                    CincoRobot,
                                    amount=float(st.session_state.amount),
                                    buy_rate=1 - float(st.session_state.buy_rate) / 100,
                                    profit_rate=1 + float(st.session_state.profit_rate) / 100,
                                    save_rate=float(st.session_state.save_rate) / 100,
                                    amount_rate=float(st.session_state.amount_rate) / 100,
                                    )

reversed_df = df.copy()
reversed_df['close'] = pd.Series(df['close'].values[::-1], index=df.index)

reversed_result = analyze_robot_trading(
    reversed_df[reversed_df.timestamp >= start_date][reversed_df.timestamp <= end_date],
    # df[df.timestamp >= start_date].sort_index(ascending=False).copy(),
    CincoRobot,
    amount=float(st.session_state.amount),
    buy_rate=1 - float(st.session_state.buy_rate) / 100,
    profit_rate=1 + float(st.session_state.profit_rate) / 100,
    save_rate=float(st.session_state.save_rate) / 100,
    amount_rate=float(st.session_state.amount_rate) / 100,
)

df_total = pd.DataFrame({'Total': norm_result['df'].Total,
                         'Reversed Total': reversed_result['df'].Total,
                         'Date': norm_result['df'].Date})

st.title('Crypto-looser strategy simulator!')

cols = st.columns(2)
cols[0].header('Normal strategy')
cols[1].header('Reversed strategy')
cols[0].write(f'Initial amount: {norm_result["amount"]:,.2f}')
cols[1].write(f'Initial amount: {reversed_result["amount"]:,.2f}')
cols[0].write(f'Final Amount: {norm_result["current_amount"]:,.2f}')
cols[1].write(f'Final Amount: {reversed_result["current_amount"]:,.2f}')
cols[0].markdown(f'**Profit**: :blue-background[{norm_result['profit']:,.2f}]')
cols[1].markdown(f'**Profit**: :blue-background[{reversed_result['profit']:,.2f}]')
cols[0].write(f'Investment: {norm_result['investment']:,.2f}')
cols[1].write(f'Investment: {reversed_result['investment']:,.2f}')
cols[0].write(f'Total values: {norm_result['total_value']:,.2f}')
cols[1].write(f'Total values: {reversed_result['total_value']:,.2f}')
cols[0].write(f'Margin: {norm_result['margin']:.2%}')
cols[1].write(f'Margin: {reversed_result['margin']:.2%}')
cols[0].write(f'Yield: {norm_result['yield']:.2%}')
cols[1].write(f'Yield: {reversed_result['yield']:.2%}')
cols[0].write(f'Days: {norm_result['days']}')
cols[1].write(f'Days: {reversed_result['days']}')
cols[0].write(f'Modified Margin: {norm_result['modified_margin']:.2%}')
cols[1].write(f'Modified Margin: {reversed_result['modified_margin']:.2%}')
cols[0].markdown(f'Modified Yield: :blue-background[{norm_result['modified_yield']:.2%}]')
cols[1].markdown(f'Modified Yield: :blue-background[{reversed_result['modified_yield']:.2%}]')
cols[0].write(f'Quantity: {norm_result["quantity"]:,.2f} price {norm_result['price']:,.2f}')
cols[1].write(f'Quantity: {reversed_result["quantity"]:,.2f} price {reversed_result['price']:,.2f}')
cols[0].write(f'Min amount: {norm_result["min_amount"]:,.2f} Max amount {norm_result['max_amount']:,.2f}')
cols[1].write(f'Min amount: {reversed_result["min_amount"]:,.2f} Max amount {reversed_result['max_amount']:,.2f}')
cols[0].write(f'Min total: {norm_result["min_total"]:,.2f} Max total {norm_result['max_total']:,.2f}')
cols[1].write(f'Min total: {reversed_result["min_total"]:,.2f} Max total {reversed_result['max_total']:,.2f}')
cols[0].write(f'Deals: {norm_result['deals_count']}')
cols[1].write(f'Deals: {reversed_result['deals_count']}')
cols[0].write(f'From: {norm_result['from'].date()} to: {norm_result['to'].date()}')
cols[1].write(f'From: {reversed_result['from'].date()} to: {reversed_result['to'].date()}')

first_price = norm_result['df'].Price.iloc[0]
last_price = norm_result['df'].Price.iloc[-1]
pure_margin = (last_price - first_price) / first_price
# st.write(f'First price: {first_price:.2f}')
# st.write(f'Last price: {last_price:.2f}')

st.title("Normal Strategy")
st.area_chart(norm_result['df'], x="Date", y=["Amount", "Value", ], stack=True)

st.title("Normal&Reversed Strategy Comparison")
st.line_chart(df_total, use_container_width=True, x="Date", y=["Total", "Reversed Total"])

st.title(f'¡¡¡Pure Margin: {pure_margin:.2%} !!!', help="Price change margin.")
st.line_chart(
    df[df.timestamp >= start_date][df.timestamp <= end_date], use_container_width=True,
    x="timestamp",
    y="close"
)

st.dataframe(norm_result['df'], use_container_width=True)

st.markdown('''
The cryptocurrency trading simulation program operates as follows:

1. **Initialization**: An investor starts with an initial sum (:blue-background[initial amount]) that they're willing to spend on cryptocurrency purchases.

2. **Price Tracking**: The program continuously tracks cryptocurrency prices. If the price of the cryptocurrency drops by a predefined percentage (:blue-background[Buy rate], for example, 5%), the program automatically executes a purchase.

3. **Investments**: The sum that the investor spends on a purchase is calculated as :blue-background[amount] * :blue-background[investment rate]. In other words, the investor uses a fixed share of their current capital for each purchase.

4. **Sale**: If the price of the cryptocurrency rises by a predetermined percentage (:blue-background[profit rate]), the program automatically sells all the cryptocurrency purchased in the last transaction.

5. **Save Rate**: A certain portion of the total sales revenue (:blue-background[save rate]) is withheld from the sum received from the sale. The remainder becomes available again for investing (purchases).

6. **Reorientation**: After each sale, the program still tracks prices relative to the previous purchase price. If all deals were closed (i.e. all purchased assets were sold), the program tracks prices relative to the current market price.

7. **Simulation Limit**: The trading simulation is limited to 1000 days or less. After this period, the simulation will end, and the final investment and profit values will be calculated.

8. **Inverted Data Testing**: The simulation also tests its functionality on inverted data. This implies that if the profitability of the strategy is only due to a rising price, it will show a loss in a falling market, indicating the need for parameter adjustments.

In summary, this program strives to maximize the investor's profit by automatically buying when prices drop and selling when prices rise. A key aspect of the strategy is the use of fixed percentage rates to determine points of purchase and sale, and the amounts for purchase and sale. The simulation period is limited to ensure the feasibility and manageability of the trading strategy. Importantly, the strategy is also tested on inverted data to ensure its robustness against different market conditions.
''')
