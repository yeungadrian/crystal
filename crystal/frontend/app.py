import streamlit as st
import requests
from pages.home import *
from pages.backtest import *
from pages.factorRegression import *
from pages.assetAnalysis import *
from pages.efficientFrontier import *

with open('env.txt', 'r') as file:
    env = file.read()

def getfunds(env):
    Request = f'{env}/stocks/'
    print(Request)
    Response = requests.get(Request).json()
    fundList = []
    for x in range(0, len(Response)):
        fundList.append(Response[x]['Code'])
    return (fundList)

fundList = getfunds(env)

st.sidebar.title('Aurora')

appOptions = ["Home", "BackTest", "Factor Analysis", "Asset Analysis", "Efficient Frontier"]

currentPage = st.sidebar.radio("Go to", appOptions)

if currentPage == "Home":
    st.title('Aurora')
    show_homepage()
if currentPage == "BackTest":
    st.title('Backtest Portfolio')
    show_backtest(fundList,env)
if currentPage == "Factor Regression":
    st.title('Factor Regression')
    show_factorRegression(fundList,env)
if currentPage == "Asset Analysis":
    st.title('Asset Analysis')
    show_assetAnalysis(fundList,env)
if currentPage == "Efficient Frontier":
    st.title('Efficient Frontier')
    show_efficientFrontier(fundList,env)
