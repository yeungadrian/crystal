import pandas as pd
import numpy as np
import requests
import altair as alt
import streamlit as st


def show_backtest(fundList,env):

    start_date = st.sidebar.date_input("Start Date")
    end_date = st.sidebar.date_input("End Date")

    initialAmount = st.sidebar.number_input("Initial Amount", min_value=0.0)

    fundsChosen = st.sidebar.multiselect(
        "Fund picker", fundList, default=['AAPL'])

    if len(fundsChosen) > 0:
        Allocation = []
        for y in range(0, len(fundsChosen)):
            temporaryAllocation = st.sidebar.number_input(
                fundsChosen[y], min_value=0.0, max_value=1.0)
            Allocation.append(temporaryAllocation)

    benchmark = st.sidebar.selectbox("Benchmark", fundList)


    startDate = start_date.strftime("%Y-%m-%d")
    endDate = end_date.strftime("%Y-%m-%d")

    rebalance = st.sidebar.checkbox("Rebalance Portfolio")
    frequency = ['Monthly', 'Quarterly', 'Yearly']
    # rebalanceFrequency should be optional with a default
    rebalanceFrequency = st.sidebar.selectbox("Rebalance Frequency", frequency)

    backtestRequest = {}

    backtestRequest['allocation_weights'] = Allocation
    backtestRequest['initial_amount'] = initialAmount
    backtestRequest['start_date'] = startDate
    backtestRequest['end_date'] = endDate
    backtestRequest['codelist'] = fundsChosen
    backtestRequest['benchmark'] = benchmark
    backtestRequest['rebalance'] = rebalance
    backtestRequest['rebalance_frequency'] = rebalanceFrequency

    @st.cache(allow_output_mutation=True)
    def backtest(env):
        url = f"{env}/backtest/"
        response = requests.post(url=url, json=backtestRequest)
        backtestData = response.json()
        backtestData = pd.DataFrame(backtestData['backtest'])
        backtestData['date'] = pd.to_datetime(backtestData['date'])
        backtestMetrics = response.json()['metrics']
        
        return { 
            'backtestData': backtestData, 
            'backtestMetrics': backtestMetrics
        }

    backtestData = backtest(env)['backtestData']
    backtestMetrics = backtest(env)['backtestMetrics']
    if 'annual returns' in backtestMetrics:
        backtestMetrics.pop('annual returns')

    chartoutput = alt.Chart(backtestData).mark_line().encode(
        x='date',
        y='output'
    ).properties(width=700)

    chartbenchmark = alt.Chart(backtestData).mark_line(color = 'black').encode(
        x='date',
        y='benchmark'
    ).properties(width=700)

    st.write('Portfolio Value')
    st.write(chartoutput+ chartbenchmark)

    chartDrawdown = alt.Chart(backtestData).mark_line(color = 'red').encode(
        x='date',
        y='drawdown_pct'
    ).properties(width=700)

    displayMetrics = pd.DataFrame.from_dict(backtestMetrics, orient = 'index').transpose()
    st.write('Portfolio Metrics')
    st.write(displayMetrics)

    st.write('Drawdowns')
    st.write(chartDrawdown)
