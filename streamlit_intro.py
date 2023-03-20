import streamlit as st
import pandas as pd
import altair as alt

st.write('Hello Titania')

st.title("Titania World")
# st.markdown("This is markdown")
# st.header("this is header")
# st.subheader("This is subheader")
# st.caption("this is a caption")
# st.code("x2021")
# st.latex(r''' a+a r^+a r^2+1 ''')

# st.checkbox('yes')
# st.button('Click')
# st.radio('Pick your gender',['Male','Female'])
# st.selectbox('Pick your gender',['Male','Female'])
# st.multiselect('choose a planet',['Jupiter', 'Mars', 'neptune'])
# st.select_slider('Pick a mark', ['Bad', 'Good', 'Excellent'])
# st.slider('Pick a number', 0,50)

# your_num = st.number_input('Pick a number', 0,10)
# st.text_input('Email address')
# st.date_input('Travelling date')
# st.time_input('School time')
# st.text_area('Description')
# st.file_uploader('Upload a photo')
# st.color_picker('Choose your favorite color')

# st.write(your_num)


st.image("/Users/apple/Desktop/Visual Analytics/Logo.png")

# Create a function to read the uploaded file as a DataFrame
def read_file(file):
    df = pd.read_csv(file)
    return df

# Display file upload widget
file = st.file_uploader("Upload file", type=["csv"])

# Check if file is uploaded and display the DataFrame
if file is not None:
    df = read_file(file)
    st.dataframe(df)

# Load the Cab_Data file
cab_data = pd.read_csv("Cab_Data.csv")

# Convert the 'Date of Travel' column to numeric format
cab_data['Date of Travel'] = pd.to_numeric(cab_data['Date of Travel'], errors='coerce')

# Define a function to convert numeric date to datetime object
def date_transform(date_num):
    return pd.to_datetime('1899-12-30') + pd.to_timedelta(date_num, unit='D')

# Apply the date_transform function to the 'Date of Travel' column
cab_data['Date of Travel'] = cab_data['Date of Travel'].apply(date_transform)

# Convert the "Date of Travel" column to datetime format
# cab_data["Date of Travel"] = pd.to_datetime(cab_data["Date of Travel"], format="%m/%d/%Y")

# Create a new column with the day of the week
cab_data["Day of Week"] = cab_data["Date of Travel"].dt.day_name()

# Group the data by day of the week and count the number of rides
rides_by_day = cab_data.groupby("Day of Week")["Transaction ID"].count().reset_index()
rides_by_day.columns = ["Day of Week", "Number of Rides"]

# Create a bar chart
bar_chart = alt.Chart(rides_by_day).mark_bar().encode(
    x="Day of Week",
    y="Number of Rides",
    tooltip=["Day of Week", "Number of Rides"]
).properties(
    width=600,
    height=400,
    title="Number of Rides per Day of the Week"
)

# Display the bar chart
st.altair_chart(bar_chart)

st.image("/Users/apple/Desktop/Visual Analytics/norm.jpg")
st.audio("/Users/apple/Desktop/Visual Analytics/fight_song.mp3")