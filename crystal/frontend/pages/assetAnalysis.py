import streamlit as st
import requests
import pandas as pd
import altair as alt
import json

def show_assetAnalysis(fundList,env):

    fundChosen = st.sidebar.multiselect("Fund", options=fundList)

    start_date = st.sidebar.date_input("Start Date")
    end_date = st.sidebar.date_input("End Date")

    startDate = start_date.strftime("%Y-%m-%d")
    endDate = end_date.strftime("%Y-%m-%d")

    assetAnalysisInput = {
        'codelist': list(fundChosen),
        'start_date': startDate,
        'end_date': endDate
    }

    def correlationGet(assetAnalysisInput,env):
        url = f'{env}/assetAnalysis/correlation'
        response = requests.post(url=url, json=assetAnalysisInput)
        correlationData = response.json()
        return correlationData

    correlationMatrix = pd.DataFrame(
        correlationGet(assetAnalysisInput,env)['correlation'])

    def rollingGet(assetAnalysisInput,env):
        assetAnalysisInput['codelist'] = assetAnalysisInput['codelist'][0:2]
        url = f'{env}/assetAnalysis/rollingCorrelation'
        response = requests.post(url=url, json=assetAnalysisInput)
        rollingData = response.json()
        return rollingData
    
    rollingData = pd.DataFrame({'correlation': rollingGet(assetAnalysisInput,env)})
    rollingData = rollingData.reset_index(drop = False)
    rollingData['index'] = pd.to_datetime(rollingData['index'])
    
    chartCorrelation = alt.Chart(rollingData).mark_line().encode(
        x='index',
        y='correlation'
    ).properties(width=700)

    def cointegrationGet(assetAnalysisInput,env):
        url = f"{env}/assetAnalysis/cointegration"
        response = requests.post(url=url, json=assetAnalysisInput)
        cointegrationData = response.json()
        return cointegrationData

    cointegrationData = cointegrationGet(assetAnalysisInput,env)

    cointegrationDF = pd.DataFrame(cointegrationData)

    st.write('Correlation Matrix')
    st.write(correlationMatrix)

    st.write('Rolling Correlation')
    st.write(chartCorrelation)

    st.write('Cointegration')
    st.write(cointegrationDF)
