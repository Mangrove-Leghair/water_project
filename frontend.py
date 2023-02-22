from supabase import create_client
import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


@st.cache_resource
def init_connection():
    # API credentials
    API_URL = 'https://tsaepqgxuguuoobkpivv.supabase.co'
    API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRzYWVwcWd4dWd1dW9vYmtwaXZ2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2NzU3NTgyNDMsImV4cCI6MTk5MTMzNDI0M30.vvY4PjW68WDYgKjrS3c2IXqP0IiXV1cAj7eGpgNkDLw'
    return create_client(API_URL, API_KEY)

supabase = init_connection()

# Fetching data from supabase database
# @st.cache_resource #Caching across all streamlit sessions
supabaseList = supabase.table('Water Level').select('*').execute().data

# time range variables updation to put in x axis range parameters
placeholder = datetime.now(tz=ZoneInfo('Asia/Kolkata'))
today = placeholder + \
        timedelta(hours=1)
present_date = today.strftime("%Y-%m-%d %X")
present_date_wo_time = today.strftime("%Y-%m-%d")
twodaysago = today - \
             timedelta(days=2)
back_date = twodaysago.strftime("%Y-%m-%d %X")

thirtydaysago = today - \
                timedelta(days=31)
thirtydate = thirtydaysago.strftime("%Y-%m-%d")

custom_range = [back_date, present_date]  # Setting time values for y axis to show the time period


@st.cache_data(ttl=30)
def datafr_creator():
    # initialize dataframe
    df = pd.DataFrame()

    for row in supabaseList:
        row["created_at"] = row["created_at"].split(".")[0]
        row["time"] = row["created_at"].split("T")[1]
        row["date"] = row["created_at"].split("T")[0]
        row["DateTime"] = row["created_at"]
        df = df.append(row, ignore_index=True)
    return df


# Here, it will call datafr_creator and use the cache if the
# dataframe has already been generated.df = datafr_creator()
df = datafr_creator()  # creating local list

# Display section
orignal_title = '<h1 style="font-family:Helvetica; color:Black; font-size: 45px; text-align: center">Tridev Water Monitoring System</p>'
st.markdown(orignal_title, unsafe_allow_html=True)
st.text("")
fig = px.area(df, x="DateTime", y="water_level", title='', markers=False)
fig.update_layout(
    title={
        'text': "Water level in %",
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
fig.update_layout(yaxis_range=[0, 120])
fig.update_layout(xaxis_range=custom_range)

# Add Horizontal line in plotly chart for pump trigger level
fig.add_hline(y=80, line_width=3, line_color="black",
              annotation_text="Pump Start Level",
              annotation_position="top left",
              annotation_font_size=15,
              annotation_font_color="black"
              )

# Final Chart print
st.plotly_chart(fig, use_container_width=True)

# Save Data of last 30 days as CSV
filename = datetime.now().strftime("%d_%m_%Y")
mask = (df['date'] > thirtydate) & (df['date'] <= present_date_wo_time)
df2 = df.loc[mask]


def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


csv = convert_df(df2)

st.download_button(
    label="Download CSV",
    data=csv,
    file_name=f'{filename}.csv',
    mime='text/csv',
    help="Data of Last 30 Days as .csv file",
)
