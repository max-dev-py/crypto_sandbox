import streamlit as st
import pandas as pd

from dummy_robot.price_fetcher import get_ccxt_df
from dummy_robot.strategy_tester import analyze_robot_trading
from dummy_robot.cinco import CincoRobot

st.set_page_config(page_title='Crypto-looser strategy simulator!',
                   # page_icon=None,
                   layout="wide",
                   initial_sidebar_state="auto",
                   menu_items=None
                   )


@st.cache_data  # 👈 Add the caching decorator
def load_data(symbol):
    df = get_ccxt_df(symbol=symbol)
    return df


with st.sidebar:
    st.header("Assumptions:")
    st.text_input("Ticker", key="ticker", value="BTC/USDT", help='Crypto ticker')
    st.number_input("Initial amount", key="amount", value=10000, help='Money amount')
    st.number_input("Buy rate", key="buy_rate", value=0.95, help='Buy rate')
    st.number_input("Profit rate", key="profit_rate", value=1.05, help='Profit rate')
    st.number_input("Save rate", key="save_rate", value=0.0005, format='%.5f',
                    help='Which part of crypto-currency will not be sold.')
    st.number_input("Investment rate", key="amount_rate", value=0.05, help='Which part of amount will be invested.')

df = load_data(
    symbol=st.session_state.ticker
)

norm_result = analyze_robot_trading(df,
                                    CincoRobot,
                                    amount=float(st.session_state.amount),
                                    buy_rate=float(st.session_state.buy_rate),
                                    profit_rate=float(st.session_state.profit_rate),
                                    save_rate=float(st.session_state.save_rate),
                                    amount_rate=float(st.session_state.amount_rate),
                                    )

reversed_result = analyze_robot_trading(df.sort_index(ascending=False).copy(),
                                        CincoRobot,
                                        amount=float(st.session_state.amount),
                                        buy_rate=float(st.session_state.buy_rate),
                                        profit_rate=float(st.session_state.profit_rate),
                                        save_rate=float(st.session_state.save_rate),
                                        amount_rate=float(st.session_state.amount_rate),
                                        )

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
cols[0].write(f'Quantity: {norm_result["quantity"]:.2f} price {norm_result['price']:,.2f}')
cols[1].write(f'Quantity: {reversed_result["quantity"]:.2f} price {reversed_result['price']:,.2f}')
cols[0].write(f'Min amount: {norm_result["min_amount"]:.2f} Max amount {norm_result['max_amount']:,.2f}')
cols[1].write(f'Min amount: {reversed_result["min_amount"]:.2f} Max amount {reversed_result['max_amount']:,.2f}')
cols[0].write(f'Min total: {norm_result["min_total"]:.2f} Max total {norm_result['max_total']:,.2f}')
cols[1].write(f'Min total: {reversed_result["min_total"]:.2f} Max total {reversed_result['max_total']:,.2f}')
cols[0].write(f'Deals: {norm_result['deals_count']}')
cols[1].write(f'Deals: {reversed_result['deals_count']}')
cols[0].write(f'From: {norm_result['from'].date()} to: {norm_result['to'].date()}')
cols[1].write(f'From: {reversed_result['from'].date()} to: {reversed_result['to'].date()}')

first_price = norm_result['df'].Price.iloc[0]
last_price = norm_result['df'].Price.iloc[-1]
pure_margin = (last_price - first_price) / first_price
st.title(f'¡¡¡Pure Margin: {pure_margin:.2%} !!!', help="Price change margin.")
# st.write(f'First price: {first_price:.2f}')
# st.write(f'Last price: {last_price:.2f}')

# norm_result['df']

st.title("Normal Strategy")
st.line_chart(norm_result['df'], x="Date", y=["Amount", "Value", "Total"])
st.dataframe(norm_result['df'], use_container_width=True)
