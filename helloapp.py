import streamlit as st
import tkinter
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np


x = st.slider('x')
st.write(x, 'squared is', x * x)

df = pd.read_csv("resp/data-responses.csv")
# df = st.cache(pd.read_csv)("resp/data-responses.csv")

# Emailaddress as the index
reachout_split_df = pd.DataFrame(df.BestReach.str.split(',').tolist(), index=df.Emailaddress).stack()
# Make Emailaddress as a column
reachout_split_df = reachout_split_df.reset_index([0, 'Emailaddress'])
# set the column names we want
reachout_split_df.columns = ['Emailaddress', 'BestReach']
st.write(reachout_split_df)
# Plotting Data
reachout_split_df.groupby('BestReach')['Emailaddress'].nunique().plot(kind='bar')
st.write(plt.show())

reachout_split_df.assign(dummy = 1).groupby(
  ['dummy','BestReach']
).size().to_frame().unstack().plot(kind='bar',stacked=True,legend=False)
plt.title('Best selected Reach Out Method')
# other it'll show up as 'dummy' 
plt.xlabel('BestReach')
current_handles, _ = plt.gca().get_legend_handles_labels()
reversed_handles = reversed(current_handles)
labels = reversed(reachout_split_df['BestReach'].unique())
plt.legend(reversed_handles,labels,loc='lower right')
plt.show()

mechanism_split_df = pd.DataFrame(df.PreferredMechanism.str.split(',').tolist(), index=df.Emailaddress).stack()
# Make Emailaddress as a column
mechanism_split_df = mechanism_split_df.reset_index([0, 'Emailaddress'])
# set the column names we want
mechanism_split_df.columns = ['Emailaddress', 'PreferredMechanism']
st.write(mechanism_split_df)

mechanism_split_df.groupby('PreferredMechanism')['Emailaddress'].nunique().plot(kind='bar')
st.write(plt.show())


reachgraph = go.Figure(
    data=[go.Bar(
        x = reachout_df.BestReachNames,
        y = reachout_df.BestReach,
        )],
    layout_title_text="A Figure Displayed with fig.show()"
)
reachgraph.update_layout(title='Graph showing Student Selected Reach Outs', autosize=False,
                  width=800, height=800,
                  margin=dict(l=40, r=40, b=40, t=40))
st.plotly_chart(reachgraph)

with open('resp/ugandadistricts.geojson') as f:
    data = json.load(f)
# content = response['features']['properties']['Subregion']
for feature in data['features']:
    print(feature['properties']['Subregion'])
    print(feature['geometry']['coordinates'])

suppress_deprecation_warning = st.config.get_option(
    "global.suppressDeprecationWarnings"
    )
if not suppress_deprecation_warning:
    import streamlit as st

    st.warning("""
        The `deck_gl_chart` widget is deprecated and will be removed on
        2020-05-01. To render a map, you should use `st.pydeck_chart` widget.
    """)
