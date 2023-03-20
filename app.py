import openai
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
from streamlit import cache

# Set your OpenAI API key
openai.api_key = "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"

def generate_stock_insights(stock_name, engine):
    prompt = f"Provide an analysis and insights for the stock {stock_name}"
    response = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )
    stock_insights = response.choices[0].text.strip()
    return stock_insights

def fetch_stock_data(ticker):
    return yf.download(ticker, start="2020-01-01", end="2023-01-01")

def calculate_moving_averages(data, short_window=50, long_window=200):
    data["short_mavg"] = data["Close"].rolling(window=short_window, min_periods=1).mean()
    data["long_mavg"] = data["Close"].rolling(window=long_window, min_periods=1).mean()
    return data

def generate_trading_signals(data):
    data["signal"] = 0
    data.loc[data["short_mavg"] > data["long_mavg"], "signal"] = 1
    data["positions"] = data["signal"].diff()
    return data

def plot_candlestick_chart(data, ticker):
    fig = go.Figure(data=[go.Candlestick(x=data.index,
                                         open=data['Open'],
                                         high=data['High'],
                                         low=data['Low'],
                                         close=data['Close'],
                                         increasing_line_color='green',
                                         decreasing_line_color='red',
                                         hovertext=data.index.strftime('%Y-%m-%d'),
                                         name=ticker)])
    fig.update_layout(
        title=f"{ticker} Daily Candlestick Chart",
        xaxis_rangeslider_visible=False,
        xaxis_title="Date",
        yaxis_title="Price",
        hovermode="x",
        template="plotly_dark",
        margin=dict(l=30, r=20, t=50, b=50),
    )
    return fig


def plot_mavg_signals(data, ticker):
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=data.index, y=data["Close"], mode="lines", name="Close"))
    fig.add_trace(go.Scatter(x=data.index, y=data["short_mavg"], mode="lines", name="Short MA"))
    fig.add_trace(go.Scatter(x=data.index, y=data["long_mavg"], mode="lines", name="Long MA"))

    fig.add_shape(type="rect",
                  x0=data[data.positions == 1].index,
                  x1=data[data.positions == -1].index,
                  y0=0,
                  y1=1,
                  yref="paper",
                  xref="x",
                  opacity=0.3,
                  fillcolor="green",
                  line=dict(width=0))

    fig.update_layout(title=f"{ticker} Moving Averages and Trading Signals", xaxis_rangeslider_visible=False)
    return fig

# Streamlit app
st.title("GPT-3 Stock Analysis, Insights, and Visualization")
ticker = st.text_input("Enter a stock ticker (e.g., AAPL, TSLA, AMZN):")

if ticker:
    stock_data = fetch_stock_data(ticker)
    stock_data = calculate_moving_averages(stock_data)
    stock_data = generate_trading_signals(stock_data)

    st.plotly_chart(plot_candlestick_chart(stock_data, ticker), use_container_width=True)


def generate_summary(text, engine):
    prompt = f"Please provide a summary of the following text:\n\n{text}"
    response = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )
    summary = response.choices[0].text.strip()
    return summary

# Streamlit app
st.title("GPT-3 Text Summarization")

input_text = st.text_area("Enter the text you want to summarize:")
engine = st.selectbox("Select GPT-3 Engine:", ["davinci", "davinci-codex", "curie", "babbage", "ada"])

if input_text:
    summary = generate_summary(input_text, engine)
    st.header("Summary")
    st.write(summary)

def generate_code(description, engine):
    prompt = f"Write a Python code snippet for the following task:\n\n{description}"
    response = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    code = response.choices[0].text.strip()
    return code

# Streamlit app
st.title("GPT-3 Code Generation")

code_description = st.text_area("Enter a description of the code you want to generate:")
engine = st.selectbox("Select GPT-3 Engine:", ["davinci-codex", "davinci", "curie", "babbage", "ada"])

if code_description:
    generated_code = generate_code(code_description, engine)
    st.header("Generated Code")
    st.code(generated_code, language="python")

def generate_response(conversation_history, message, engine):
    prompt = f"{conversation_history}\nUser: {message}\nAI:"
    response = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5,
    )
    reply = response.choices[0].text.strip()
    return reply

@cache(allow_output_mutation=True)
def get_history():
    return []

def append_to_history(history, user_message, ai_response):
    history.append({"role": "User", "message": user_message})
    history.append({"role": "AI", "message": ai_response})
    return history

# Streamlit app
st.title("GPT-3 Conversational AI")

history = get_history()

user_message = st.text_input("Enter your message:")
engine = st.selectbox("Select GPT-3 Engine:", ["davinci", "curie", "babbage", "ada"])
submit_button = st.button("Submit")

if submit_button:
    ai_response = generate_response("\n".join([f"{item['role']}: {item['message']}" for item in history]), user_message, engine)
    history = append_to_history(history, user_message, ai_response)

st.header("Conversation")
for item in history:
    if item["role"] == "User":
        st.markdown(f"> **{item['role']}:** {item['message']}")
    else:
        st.markdown(f"> _{item['role']}:_ {item['message']}")
