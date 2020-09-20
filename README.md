# Crystal
Investment analysis application

### What Crystal does
- Range of investment analysis on US stocks in the S&P 500
- Backtesting of how portfolios historically performed
- Factor Regression using French-Fama
- Efficient Frontier Construction

### Tech Stack
- Python
- FastAPI Backend https://fastapi.tiangolo.com
- Streamlit Frontend https://www.streamlit.io
- Local development with docker compose

### Installation
- Download repo
- Run docker-compose up
- Go to http://localhost:8501 for streamlit application
- Backend swagger page at http://localhost:8000

### Data Source:
- Kenneth R. French http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html
- AlphaVantage https://www.alphavantage.co

### Examples of the application
![Dashboard](images/backtest.png?raw=true)

![Breakdown](images/frontier.png?raw=true)

![Forecast](images/factorRegression.png?raw=true)