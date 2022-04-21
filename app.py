from distutils.fancy_getopt import OptionDummy
import streamlit as st

from instockalert import geturl, getalert

st.set_page_config(page_icon='📦', page_title='Is my bike in stock?')

with open('bike_urls.txt') as bikes:
    bikes = bikes.readlines()
models = []
colors = []
for url in bikes:
    models.append(url.split('/')[8])
    colors.append(url.split('=')[1].replace('%2','-').strip('\n')) # Cleaning up color substring
# Our first option is for testing our code on known model that is in stock
models[0] = 'TEST  ' + models[0]
options = [a + ' - ' + b for a,b in zip(colors, models)]
bike = st.radio("Which bike's stock do you wish to check?", tuple(options))
opbike = options.index(bike)  


size = st.radio("Size", ('S','M','L','XL','2XL'))

try:
    alert, name = getalert(geturl(opbike,size))
except:
    st.markdown(f" #### Please make valid selection ")
    alert = False

if alert:
    st.markdown(f" #### Bike :bike: IS in stock! :beers: \
                   \nfollow the link to buy - \
                   \n{geturl(opbike,size)}")
else:
    st.markdown(f" #### Bike IS NOT in stock! :sob: ")
