import streamlit as st
import tkinter
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

'''
## IC3 Training Survey Insights App

This very simple webapp allows you to select and visualize insights got 
from the students' responses. About 250 people have responded. 
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
st.write(new_df)

if st.checkbox('Show dataframe'):
    st.write(df)
# print(pd.DataFrame(df))

# ########## REACH OUT
# Emailaddress as the index
reachout_split_df = pd.DataFrame(df.BestReach.str.split(',').tolist(), index=df.Emailaddress).stack()
# Make Emailaddress as a column
reachout_split_df = reachout_split_df.reset_index([0, 'Emailaddress'])
# set the column names we want
reachout_split_df.columns = ['Emailaddress', 'BestReach']
reachout_split_df.to_csv(r'resp/reahout.csv')

# Reach out Data
reachout_df = pd.read_csv("resp/reachout.csv")
st.write(reachout_df)
st.write(reachout_df.groupby(['BestReach']).mean())

reachout_df.groupby('BestReach')['Emailaddress'].nunique().plot(kind='bar')
st.write(plt.title('Graph showing Student Selected Reach Outs'))
st.write(plt.xticks(np.arange(5), ('Email', 'WhatsApp','SMS', 'Zoom', 'Google Meet')))
(plt.show())
 

#   ############# Mechanism
# Emailaddress as the index
mech_split_df = pd.DataFrame(df.PreferredMechanism.str.split(',').tolist(), index=df.Emailaddress).stack()
# Make Emailaddress as a column
mech_split_df = mech_split_df.reset_index([0, 'Emailaddress'])
# set the column names we want
mech_split_df.columns = ['Emailaddress', 'PreferredMechanism']
# mech_split_df.to_csv(r'resp/PreferredMechanism.csv')

# Mechanism out Data
mech_df = pd.read_csv("resp/PreferredMechanism.csv")
st.write(mech_df)
st.write(mech_df.groupby(['PreferredMechanism']).mean())

mech_df.groupby('PreferredMechanism')['Emailaddress'].nunique().plot(kind='bar')
st.write(plt.title('Graph showing Student Selected Preferred Mechanism'))
# Both Online and Face to Face 1
#  Online on Campus 2
#  Online at Home 3
# Face to Face on Campus 4
#  Face to Face by location 5

st.write(plt.xticks(np.arange(5), ('Both Online and Face to Face', 'Online on Campus','Online at Home', 'Face to Face on Campus', 'Face to Face by location')))
(plt.show())

mechanism_split_df = pd.DataFrame(df.PreferredMechanism.str.split(',').tolist(), index=df.Emailaddress).stack()
# Make Emailaddress as a column
mechanism_split_df = mechanism_split_df.reset_index([0, 'Emailaddress'])
# set the column names we want
mechanism_split_df.columns = ['Emailaddress', 'PreferredMechanism']
st.write(mechanism_split_df)
# mechanism_split_df.groupby('PreferredMechanism')['Emailaddress'].nunique().plot(kind='bar')
# st.write(plt.show())

