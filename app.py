from distutils.fancy_getopt import OptionDummy
import streamlit as st

from instockalert import geturl, getalert, checkstock

st.set_page_config(page_icon='📦', page_title='Is my bike in stock?')



bike = st.radio("Which bike's stock do you wish to check?", ('Endurace','Grizl','Test'))
opbike = ['Endurace','Grizl','Test'].index(bike) + 1 

if opbike == 1:
    type = st.radio("Name of the bike", ('Endurace-cf-sl-7-disc','BLUE endurace-8-disc','BLACK endurace-8-disc'))
    optype = ['Endurace-cf-sl-7-disc','BLUE endurace-8-disc','BLACK endurace-8-disc'].index(type) + 1
elif opbike == 2:
    type = st.radio("Name of the bike", ('grizl-cf-sl-6', 'grizl-7'))
    optype = ['grizl-cf-sl-6', 'grizl-7'].index(type) + 1
else:
    st.write('Please select XL or 2XL size for testing')
    optype = 42


size = st.radio("Size", ('S','M','L','XL','2XL'))

try:
    alert, name = getalert(geturl(opbike,optype,size))
except:
    st.markdown(f" #### Please make valid selection ")
    alert = False

if alert:
    st.markdown(f" #### Bike IS in stock! \
                   \nfollow the link to buy {geturl(opbike,optype,size)}")
else:
    st.markdown(f" #### Bike IS NOT in stock! ☹️ ")
