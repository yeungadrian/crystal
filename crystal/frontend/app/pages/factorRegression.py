import streamlit as st
import requests
import pandas as pd
import altair as alt


def show_factorRegression(fundList):

    fundChosen = st.sidebar.multiselect("Fund", options=fundList)

    if len(fundChosen) > 0:
        Allocation = []
        for y in range(0, len(fundChosen)):
            temporaryAllocation = st.sidebar.number_input(
                fundChosen[y], min_value=0.0, max_value=1.0)
            Allocation.append(temporaryAllocation)

    start_date = st.sidebar.date_input("Start Date")
    end_date = st.sidebar.date_input("End Date")

    startDate = start_date.strftime("%Y-%m-%d")
    endDate = end_date.strftime("%Y-%m-%d")

    factorList = ["MktMinRF", "SMB", "HML", "RMW", "CMA", "MOM"]

    factors = st.sidebar.multiselect("Regression Factors", factorList, default=[
                                     "MktMinRF", "SMB", "HML"])

    factorRegressionInput = {}

    factorRegressionInput['benchmark'] = "ABT"
    factorRegressionInput['start_date'] = startDate
    factorRegressionInput['end_date'] = endDate
    factorRegressionInput['regressionFactors'] = factors

    def factorRegression(factorRegressionInput):
        url = "http://api:8000/factorRegression/"
        response = requests.post(url=url, json=factorRegressionInput)
        factorRegressionData = response.json()
        return factorRegressionData

    outputRegression = {}
    summaryRegression = {}

    optimizeFactorData = {}
    optimizeFactorData['portfolio'] = []
    # Run regression
    for y in range(0, len(fundChosen)):
        fundToRegress = []
        fundToRegress.append(fundChosen[y])
        factorRegressionInput['codeList'] = fundToRegress
        factorRegressionData = factorRegression(factorRegressionInput)
        coefficientColumns = ["coeff", "pvals", "conf_lower", "conf_higher"]
        outputRegression[fundChosen[y]] = pd.DataFrame(
            factorRegressionData)[coefficientColumns]
        if y == 0:
            for l in range(0, len(factors)):
                summaryRegression[factors[l]] = [
                    factorRegressionData["coeff"][factors[l]]]
        else:
            for l in range(0, len(factors)):
                summaryRegression[factors[l]].append(
                    factorRegressionData["coeff"][factors[l]])
        optimizeFactorData['portfolio'].append(
            {fundChosen[y]: factorRegressionData["coeff"]})
        optimizeFactorData['portfolio'][y][fundChosen[y]
                                           ]['initialweight'] = Allocation[y]

    optimizeFactorData["optimization"] = {}
    sliders = {}
    for y in factors:
        sliders[y] = st.slider(y, min_value=min(
            summaryRegression[y]), max_value=max(summaryRegression[y]), step=0.01)
        optimizeFactorData["optimization"][y] = sliders[y]

    def optimizeFactor(optimizeFactorInput):
        url = "http://api:8000/optimizeFactor/"
        response = requests.post(url=url, json=optimizeFactorInput)
        optimizeFactorData = response.json()
        return optimizeFactorData

    optimizedPortfolio = optimizeFactor(optimizeFactorData)

    source = pd.DataFrame({
        'Fund': fundChosen,
        'Proportion': optimizedPortfolio
    })

    chartPie = alt.Chart(source).mark_bar().encode(
        x='Fund',
        y='Proportion'
    ).properties(width=700)

    st.write("Optimized Portfolio")

    st.write(chartPie)

    st.write('Individual Stock Factor Regression')

    for y in range(0, len(outputRegression.keys())):
        st.write(fundChosen[y])
        st.write(outputRegression[fundChosen[y]])
