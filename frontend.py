from supabase import create_client
import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime, timedelta

API_URL = 'https://tsaepqgxuguuoobkpivv.supabase.co'
API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRzYWVwcWd4dWd1dW9vYmtwaXZ2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2NzU3NTgyNDMsImV4cCI6MTk5MTMzNDI0M30.vvY4PjW68WDYgKjrS3c2IXqP0IiXV1cAj7eGpgNkDLw'
supabase = create_client(API_URL, API_KEY)

supabaseList = supabase.table('Water Level').select('*').execute().data

# time range variables updation to put in x axis range parameters
placeholder = datetime.now()
today = placeholder + \
        timedelta(minutes = 30)
present_date = placeholder.strftime("%Y-%m-%d %X")
twodaysago = today - \
        timedelta(days = 2)
back_date = twodaysago.strftime("%Y-%m-%d %X")

df = pd.DataFrame()

for row in supabaseList:
    row["created_at"] = row["created_at"].split(".")[0]
    row["time"] = row["created_at"].split("T")[1]
    row["date"] = row["created_at"].split("T")[0]
    row["DateTime"] = row["created_at"]
    df = df.append(row, ignore_index=True)

orignal_title = '<h1 style="font-family:Helvetica; color:Black; font-size: 45px; text-align: center">Tridev Water Monitoring System</p>'
st.markdown(orignal_title, unsafe_allow_html=True)
st.text("")

custom_range = [back_date, present_date]
fig = px.area(df, x="DateTime", y="water_level", title='',markers=False)
fig.update_layout(
    title={
        'text': "Water level in %",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
fig.update_layout(yaxis_range = [0,120])
fig.update_layout(xaxis_range = custom_range)

#Add Horizontal line in plotly chart for pump trigger level
fig.add_hline(y=80, line_width=3, line_color="black",
              annotation_text="Pump Start Level",
              annotation_position="top left",
              annotation_font_size=15,
              annotation_font_color="black"
              )

st.plotly_chart(fig,use_container_width=True)

