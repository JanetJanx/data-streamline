import streamlit as st
import pydeck as pdk
import tkinter
import matplotlib
matplotlib.use('Agg')
import multiprocessing
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import json
import plotly.graph_objects as go


import os
MAPBOX_API_KEY = os.environ["MAPBOX_API_KEY"]
'''
## IC3 Training Survey Insights App

This very simple webapp allows you to select and visualize insights got 
from the students' responses. About 300 students have responded! 
.
'''
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)    

local_css("style.css")
remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')

@st.cache(allow_output_mutation=True)
def load_df():
    df = pd.read_csv("resp/data-responses.csv")
    return df

df = load_df()

st.sidebar.title('Our Dashboard')
st.sidebar.write('Responses')
resp = df['Emailaddress'].count()
st.sidebar.button(str(resp))

# ########## Skill Rates
@st.cache(allow_output_mutation=True)
def load_skill_df():
    skill_df = df['Rate_Computer_Skills']
    return skill_df

skill_df = load_skill_df()
# st.write(skill_df)
counts = skill_df.value_counts(sort=True)
# colors = {'slightknowledge':'red', 'Moderate':'blue', 'VeryGood':'green', 'No Skills':'purple', 'Expert':'yellow'} 
# labels = list(colors.keys())
ax = skill_df.value_counts(sort=True).plot(kind='bar', color=('brown', 'darkblue', 'darkgreen', 'purple', 'red'), label='Inline label')
plt.title('Graph showing computer skill rate of students')
plt.xticks(fontsize =8)
ax.set_xlabel('Computer Skill Rate Levels')
ax.set_ylabel('Students')
rects = ax.patches
labels = counts[:5].to_list() 
for rect, label in zip(rects, labels):
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width() / 2, height + 1, label,
            ha='center', va='bottom')
st.pyplot()
st.sidebar.write('Most rated Computer Skill: ', skill_df.value_counts(sort=True)[:1][:1])
respe = counts[0]
st.sidebar.button(str(respe))
# ########## REACH OUT
# Emailaddress as the index
reachout_split_df = pd.DataFrame(df.BestReach.str.split(',').tolist(), index=df.Emailaddress).stack()
# Make Emailaddress as a column
reachout_split_df = reachout_split_df.reset_index([0, 'Emailaddress'])
# set the column names we want
reachout_split_df.columns = ['Emailaddress', 'BestReach']
reachout_split_df.to_csv(r'resp/reahout.csv')

# Reach out Data
@st.cache(allow_output_mutation=True)
def load_reachout_df():
    reachout_df = pd.read_csv("resp/reachout.csv")
    return reachout_df

reachout_df = load_reachout_df()
reach_names = reachout_df['BestReachNames']
# st.write(reach_names)
reach_df = reachout_df['BestReach']
reach_counts = reach_df.value_counts(sort=False)
ax_reach = reachout_df.groupby('BestReach')['Emailaddress'].nunique().plot(kind='bar', color=('brown', 'blue', 'green', 'purple', 'yellow'))
plt.title('Graph showing Selected ReachOut methods by the Students')
plt.xticks(np.arange(5), ('Email', 'WhatsApp','SMS', 'Zoom', 'Google Meet'), fontsize = 8)
ax_reach.set_xlabel('Communication Methods')
ax_reach.set_ylabel('Students')
rects_r = ax_reach.patches
labels_r = reach_counts[:5].to_list() 
for rect, label in zip(rects_r, labels_r):
    height = rect.get_height()
    ax_reach.text(rect.get_x() + rect.get_width() / 2, height + 1, label,
            ha='center', va='bottom')
st.pyplot()
st.sidebar.write('Prefered Reach out Method: ')
respes = max(reach_counts)
st.sidebar.text("WhatsApp")
st.sidebar.button(str(respes))

#   ############# Mechanism
# Emailaddress as the index
mech_split_df = pd.DataFrame(df.PreferredMechanism.str.split(',').tolist(), index=df.Emailaddress).stack()
# Make Emailaddress as a column
mech_split_df = mech_split_df.reset_index([0, 'Emailaddress'])
# set the column names we want
mech_split_df.columns = ['Emailaddress', 'PreferredMechanism']
mech_split_df.to_csv(r'resp/PreferredMechanis.csv')

# Mechanism out Data
@st.cache(allow_output_mutation=True)
def load_mech_df():
    mech_df = pd.read_csv("resp/PreferredMechanism.csv")
    return mech_df
mech_df = load_mech_df()
# st.write(mech_df)
@st.cache(allow_output_mutation=True)
def load_mec_df():
    mec_df = pd.read_csv("resp/PreferredMechanis.csv")
    return mec_df
mec_df = load_mec_df()

mechanism_df = mech_df['PreferredMechanism']
mechanis_df = mec_df['PreferredMechanism']
mech_counts = mechanism_df.value_counts(sort=False)
ax_mech = mech_df.groupby('PreferredMechanism')['Emailaddress'].nunique().plot(kind='bar', color=('blue', 'red', 'green', 'purple', 'yellow'))
plt.title('Graph showing Selected Preferred Mechanism by the Students')
# Both Online and Face to Face 1
#  Online on Campus 2
#  Online at Home 3
# Face to Face on Campus 4
#  Face to Face by location 5

plt.xticks(np.arange(5), ('Both Online and Face to Face', 'Online on Campus','Online at Home', 'Face to Face on Campus', 'Face to Face by location'), fontsize = 8)
ax_mech.set_xlabel('Delivery Mechanisms')
ax_mech.set_ylabel('Students')
rects_m = ax_mech.patches
labels_m = mech_counts[:5].to_list() 
for rect, label in zip(rects_m, labels_m):
    height = rect.get_height()
    ax_mech.text(rect.get_x() + rect.get_width() / 2, height + 1, label,
            ha='center', va='bottom')
st.pyplot()
st.sidebar.write('Preferred Delivery Mechanism: ', mechanis_df.value_counts(sort=True)[:1])
respese = max(mech_counts)
st.sidebar.button(str(respese))

option = st.sidebar.multiselect(
    'What is the best way to reach you?',
     df['BestReach'].unique())
     
# 'You selected: ', option

options = st.sidebar.multiselect(
 'What mechanism would you prefer?', df['PreferredMechanism'].unique())
 
# st.write('You selected:', options)
new_df = df[(df['BestReach'].isin(option)) & (df['PreferredMechanism'].isin(options))]
st.sidebar.write('Students who prefer ', option, 'and ', options)
st.sidebar.write(new_df)
if st.sidebar.checkbox('View Student Responses'):
    st.sidebar.subheader('Student Responses')
    st.sidebar.write(df)
# print(pd.DataFrame(df))

programs_df = df['Program of Study']
program_counts = programs_df.value_counts(sort=True)
ax_program = program_counts.nlargest(55).plot(kind='bar', color=('purple'))
plt.title('Graph showing the number of students by program of study ')
plt.xticks(fontsize =8)
ax_program.set_xlabel('Programs of Study')
ax_program.set_ylabel('Students')
rects_p = ax_program.patches
labels_p = program_counts[:55].to_list() 
for rect, label in zip(rects_p, labels_p):
    height = rect.get_height()
    ax_program.text(rect.get_x() + rect.get_width() / 2, height + 0.5, label,
            ha='center', va='bottom')
st.pyplot()
if st.sidebar.checkbox('View Student courses by Program'):
    st.sidebar.subheader('Student courses by Program')
    st.sidebar.write(programs_df.value_counts())

college_df = df['College']
college_counts = college_df.value_counts(sort=True)
ax_college = college_counts.plot(kind='bar', color=('purple', 'red', 'brown', 'green', 'blue', 'black', 'darkblue', 'darkgreen', 'yellow', 'pink'))
plt.title('Graph showing the number of students by college ')
plt.xticks(fontsize =8)
ax_college.set_xlabel('Colleges')
ax_college.set_ylabel('Students')
rects_c = ax_college.patches
labels_c = college_counts.to_list() 
for rect, label in zip(rects_c, labels_c):
    height = rect.get_height()
    ax_college.text(rect.get_x() + rect.get_width() / 2, height + 0.5, label,
            ha='center', va='bottom')
st.pyplot()
if st.sidebar.checkbox('View Student courses by College'):
    st.sidebar.subheader('Student courses by College')
    st.sidebar.write(college_df.value_counts())

# filter = st.slider('', 1, 31, 5)
# Location_Filter = df[df['District'] == filter]
location_df = df['District'].value_counts()
location_df.to_csv(r'resp/locatio.csv')

@st.cache(allow_output_mutation=True)
def load_loca_df():
    loca_df = pd.read_csv("resp/location.csv").dropna()
    return loca_df

loca_df = load_loca_df()
if st.sidebar.checkbox('View Student Locations'):
    st.sidebar.subheader('Student Locations')
    st.sidebar.write(loca_df)

locat_df = df['District']
loca_counts = locat_df.value_counts(sort=True)
ax_loca = df['District'].value_counts(sort=True).nlargest(50).plot(kind='bar')
plt.title('Graph showing the first 50 districts with the highest number of students')
plt.xticks(fontsize =8)
ax_loca.set_xlabel('Districts')
ax_loca.set_ylabel('Students')
rects_l = ax_loca.patches
labels_l = loca_counts[:50].to_list() 
for rect, label in zip(rects_l, labels_l):
    height = rect.get_height()
    ax_loca.text(rect.get_x() + rect.get_width() / 2, height + 0.5, label,
            ha='center', va='bottom')
st.pyplot()

# Map to show the physical locations of Crime for the selected day.
midpoint = (np.average(loca_df["lat"]), np.average(loca_df["lon"]))
loc_df = loca_df['Students'].dropna()
st.pydeck_chart(pdk.Deck(
     map_style='mapbox://styles/mapbox/light-v10',
     layers=[
         pdk.Layer(
            type='HexagonLayer',
            data=loca_df,
            radius=200,
            elevationScale=4,
            elevationRange=[0, 1000],
            pickable=True,
            extruded=True,
         ),
         pdk.Layer(
             type='ScatterplotLayer',
             data=loca_df,
             pickable=True,
             opacity=0.8,
            #  stroked=True,
             filled=True,
             radius_scale=1,
             radius_min_pixels=10,
             radius_max_pixels=600,
             line_width_min_pixels=1,                                                                                                               
             get_position='[lon, lat]',
             get_radius=loc_df,
             get_fill_color='[200, 30, 0, 160]',
             get_line_color=[255,0,0]
         ),
     ],
     initial_view_state=pdk.ViewState(
         latitude=midpoint[0],
         longitude=midpoint[1],
         zoom=6,
         pitch=20,
     ),
     tooltip={
         "text": "{District}: '{Students}'",
         "style": {
             "color": "white",
             "visibility": "visible"
             }
             },
     
))

# ########## Google locations
# Emailaddress as the index
google_split_df = pd.DataFrame(df.GeoAddress.str.split(',').tolist(), index=df.Emailaddress).stack()
# Make Emailaddress as a column
google_split_df = google_split_df.reset_index([0, 'Emailaddress'])
# set the column names we want
google_split_df.columns = ['Emailaddress', 'GeoAddress']
# google_split_df.to_csv(r'resp/googlelocation.csv')

# Google Location Data
@st.cache(allow_output_mutation=True)
def load_google_df():
    google_df = pd.read_csv("resp/googlelocation.csv")
    return google_df

google_df = load_google_df()
google_loc_df = google_df['District'].value_counts(sort=True)
# google_loc_df.to_csv(r'resp/googleloc.csv')

@st.cache(allow_output_mutation=True)
def load_google_loc_df():
    google_loc_df = pd.read_csv("resp/googleloc.csv")
    return google_loc_df

google_location_df = load_google_loc_df()
# Graph for Google Locations
google_locat_df = google_df['District'].value_counts(sort=True)
ax_google = google_locat_df.nlargest(20).plot(kind='bar', color=('green'))
plt.title('Graph showing the Google reported location for the students')
plt.xticks(fontsize =8)
ax_google.set_xlabel('Districts')
ax_google.set_ylabel('Students')
rects_g = ax_google.patches
labels_g = google_locat_df[:20].to_list() 
for rect, label in zip(rects_g, labels_g):
    height = rect.get_height()
    ax_google.text(rect.get_x() + rect.get_width() / 2, height + 0.2, label,
            ha='center', va='bottom')
st.pyplot()
# Map to show the physical locations of Crime for the selected day.
midpoint = (np.average(google_location_df["lat"]), np.average(google_location_df["lon"]))
std_loc_df = google_location_df['Students'].dropna()
st.pydeck_chart(pdk.Deck(
     map_style='mapbox://styles/mapbox/light-v10',
     layers=[
         pdk.Layer(
            type='HexagonLayer',
            data=google_location_df,
            radius=200,
            elevationScale=4,
            elevationRange=[0, 1000],
            pickable=True,
            extruded=True,
         ),
         pdk.Layer(
             type='ScatterplotLayer',
             data=google_location_df,
             pickable=True,
             opacity=0.8,
             filled=True,
             radius_scale=1,
             radius_min_pixels=10,
             radius_max_pixels=600,
             line_width_min_pixels=1,                                                                                                               
             get_position='[lon, lat]',
             get_radius=loc_df,
             get_fill_color='[100, 200, 0, 150]',
             get_line_color=[255,0,0]
         ),
     ],
     initial_view_state=pdk.ViewState(
         latitude=midpoint[0],
         longitude=midpoint[1],
         zoom=6,
         pitch=20,
     ),
     tooltip={
         "text": "{District}: '{Students}'",
         "style": {
             "color": "white",
             "visibility": "visible"
             }
             },
     
))