import streamlit as st
import requests
import pandas as pd
import altair as alt
import json


def show_efficientFrontier(fundList,env):
    fundChosen = st.sidebar.multiselect("Fund", options=fundList)

    start_date = st.sidebar.date_input("Start Date")
    end_date = st.sidebar.date_input("End Date")

    startDate = start_date.strftime("%Y-%m-%d")
    endDate = end_date.strftime("%Y-%m-%d")

    efficientFrontierInput = {
        'codelist': list(fundChosen),
        'start_date': startDate,
        'end_date': endDate
    }
    @st.cache
    def assetreturns(efficientFrontierInput,env):
        url = f"{env}/efficientFrontier/individualReturns"
        response = requests.post(url=url, json=efficientFrontierInput)
        frontierData = response.json()
        return frontierData

    assetDataDF = pd.DataFrame(assetreturns(efficientFrontierInput,env))
    assetDataDF['date'] = pd.to_datetime(assetDataDF['date'])

    assetPriceChart = alt.Chart(assetDataDF).mark_line().encode(
        x='date',
        y='price',
        color='symbol',
        strokeDash='symbol',
    ).properties(width=700)

    assetReturnsChart = alt.Chart(assetDataDF).mark_line().encode(
        x='date',
        y='returns',
        color='symbol',
        strokeDash='symbol',
    ).properties(width=700)

    simulatedFrontierInput = {
        'codelist': list(fundChosen),
        'start_date': startDate,
        'end_date': endDate,
        'num_portfolios': 4000
    }

    @st.cache
    def simulatedFrontier(simulatedFrontierInput,env):
        url = f"{env}/efficientFrontier/simulatedFrontier"
        response = requests.post(url=url, json=simulatedFrontierInput)
        simulatedData = response.json()
        return simulatedData

    simulatedDataDF = pd.DataFrame(simulatedFrontier(simulatedFrontierInput,env))

    simulatedChart = alt.Chart(simulatedDataDF).mark_circle(size=10,color = 'lightgrey',opacity=0.2).encode(
        x='Volatility',
        y='Return',
        tooltip=['Volatility', 'Return', 'Sharpe Ratio'] + fundChosen
    ).properties(width=700, height = 400).add_selection(
        alt.selection_interval(bind='scales')
    )
    
    def efficientFrontier(efficientFrontierInput,env):
        url = f"{env}/efficientFrontier/efficientFrontier"
        response = requests.post(url=url, json=efficientFrontierInput)
        frontierData = response.json()
        return frontierData

    frontierDataDF = pd.DataFrame(efficientFrontier(efficientFrontierInput,env))

    frontierChart = alt.Chart(frontierDataDF).mark_circle(size=15,color = 'green',opacity = 0.6).encode(
        x='Volatility',
        y='Return',
         tooltip=['Volatility', 'Return', 'Sharpe Ratio'] + fundChosen
    ).properties(width=700, height = 400).add_selection(
        alt.selection_interval(bind='scales')
    )

    def stockData(efficientFrontierInput,env):
        url = f"{env}/efficientFrontier/meanvariance"
        response = requests.post(url=url, json=efficientFrontierInput)
        stockData = response.json()
        return stockData

    plotStocksDF = pd.DataFrame(stockData(efficientFrontierInput,env))

    stockChart = alt.Chart(plotStocksDF).mark_circle(size=30).encode(
        x='Volatility',
        y='Return',
        color = 'Symbol',
        tooltip=['Symbol', 'Volatility', 'Return']
    ).properties(width=700, height = 400).add_selection(
        alt.selection_interval(bind='scales')
    )

    indexDataAltair = pd.DataFrame()
    for x in range(0,len(fundChosen)):
        tempAltair = frontierDataDF[[fundChosen[x],'Volatility']]
        tempAltair.columns = ['weight','Volatility']
        tempAltair['symbol'] = fundChosen[x]
        indexDataAltair = indexDataAltair.append(tempAltair)

    indexDataAltair = indexDataAltair.reset_index(drop=True)

    stackedChart = alt.Chart(indexDataAltair).mark_area(opacity=0.3).encode(
        x="Volatility",
        y=alt.Y("weight", stack="normalize"),
        color="symbol:N"
    ).properties(width=700)

    st.write('Efficient Frontier')
    st.write(simulatedChart+frontierChart+stockChart)

    st.write('Efficient Portfolios')
    st.write(frontierDataDF)

    st.write('Efficient Frontier Transition Map')
    st.write(stackedChart)

    st.write('Daily Prices')
    st.write(assetPriceChart)

    st.write('Daily Returns')
    st.write(assetReturnsChart)