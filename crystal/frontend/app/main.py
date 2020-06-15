import streamlit as st
import requests
from pages.home import *
from pages.backtest import *
from pages.factorRegression import *
from pages.assetAnalysis import *
from pages.efficientFrontier import *

def getfunds():
    Request = 'http://api:8000/stocks/'
    Response = requests.get(Request).json()
    fundList = []
    for x in range(0, len(Response)):
        fundList.append(Response[x]['Code'])
    return (fundList)


fundList = getfunds()

st.sidebar.title('Aurora')

appOptions = ["Home", "BackTest", "Factor Regression", "Asset Analysis", "Efficient Frontier"]

currentPage = st.sidebar.radio("Go to", appOptions)

if currentPage == "Home":
    st.title('Aurora')
    show_homepage()
if currentPage == "BackTest":
    st.title('Backtest Portfolio')
    show_backtest(fundList)
if currentPage == "Factor Regression":
    st.title('Factor Regression')
    show_factorRegression(fundList)
if currentPage == "Asset Analysis":
    st.title('Asset Analysis')
    show_assetAnalysis(fundList)
if currentPage == "Efficient Frontier":
    st.title('Efficient Frontier')
    show_efficientFrontier(fundList)
