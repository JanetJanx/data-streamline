import streamlit as st
import tkinter
import matplotlib
matplotlib.use('TkAgg')
import multiprocessing
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

import plotly.graph_objects as go


'''
## IC3 Training Survey Insights App

This very simple webapp allows you to select and visualize insights got 
from the students' responses. About 300 students have responded! 
.
'''

df = pd.read_csv("resp/data-responses.csv")
# df = st.cache(pd.read_csv)("resp/data-responses.csv")

option = st.sidebar.multiselect(
    'What is the best way to reach you?',
     df['BestReach'].unique())
     
# 'You selected: ', option

options = st.sidebar.multiselect(
 'What mechanism would you prefer?', df['PreferredMechanism'].unique())
 
# st.write('You selected:', options)

new_df = df[(df['BestReach'].isin(option)) & (df['PreferredMechanism'].isin(options))]
st.sidebar.write(new_df)

if st.sidebar.checkbox('Show Student Responses'):
    st.sidebar.write(df)
# print(pd.DataFrame(df))

# ########## REACH OUT
# Emailaddress as the index
reachout_split_df = pd.DataFrame(df.BestReach.str.split(',').tolist(), index=df.Emailaddress).stack()
# Make Emailaddress as a column
reachout_split_df = reachout_split_df.reset_index([0, 'Emailaddress'])
# set the column names we want
reachout_split_df.columns = ['Emailaddress', 'BestReach']
# reachout_split_df.to_csv(r'resp/reahout.csv')

# Reach out Data
reachout_df = pd.read_csv("resp/reachout.csv")
# st.write(reachout_df)

reachout_df.groupby('BestReach')['Emailaddress'].nunique().plot(kind='bar', color=('red', 'blue', 'green', 'purple', 'yellow'))
plt.title('Graph showing Student Selected Reach Outs')
plt.xticks(np.arange(5), ('Email', 'WhatsApp','SMS', 'Zoom', 'Google Meet'), fontsize = 5)
st.pyplot()
 

#   ############# Mechanism
# Emailaddress as the index
mech_split_df = pd.DataFrame(df.PreferredMechanism.str.split(',').tolist(), index=df.Emailaddress).stack()
# Make Emailaddress as a column
mech_split_df = mech_split_df.reset_index([0, 'Emailaddress'])
# set the column names we want
mech_split_df.columns = ['Emailaddress', 'PreferredMechanism']
# mech_split_df.to_csv(r'resp/PreferredMechanis.csv')

# Mechanism out Data
mech_df = pd.read_csv("resp/PreferredMechanism.csv")
# st.write(mech_df)


mech_df.groupby('PreferredMechanism')['Emailaddress'].nunique().plot(kind='bar', color=('lightblue', 'pink', 'lightgreen', 'purple', 'yellow'))
plt.title('Graph showing Student Selected Preferred Mechanism')
# Both Online and Face to Face 1
#  Online on Campus 2
#  Online at Home 3
# Face to Face on Campus 4
#  Face to Face by location 5

plt.xticks(np.arange(5), ('Both Online and Face to Face', 'Online on Campus','Online at Home', 'Face to Face on Campus', 'Face to Face by location'), fontsize = 5)
st.pyplot()

st.subheader('Crime Location on Map - Select the day of a Month')
filter = st.slider('', 1, 31, 5)
Location_Filter = df[df['District'] == filter]

# Map to show the physical locations of Crime for the selected day.
midpoint = (np.average(Location_Filter["lat"]), np.average(Location_Filter["lon"]))

st.deck_gl_chart(
    viewport={
        "latitude": midpoint[0],
        "longitude": midpoint[1],
        "zoom": 11,
        "pitch": 40,
    },
    layers=[
        {
            "type": "HexagonLayer",
            "data": Crime_Filter,
            "radius": 80,
            "elevationScale": 4,
            "elevationRange": [0, 1000],
            "pickable": True,
            "extruded": True,
        }
    ],
)