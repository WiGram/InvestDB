from shiny import render, reactive
from matplotlib import pyplot as plt
import yfinance as yf


def server(input, output, session):

    # Have a choice of tickers
    # Make later min/max dates be dynamic with download dates
    
    @reactive.Calc
    @reactive.event(input.yf_get)
    def start_get_date():
        return input.dt_rng()[0]
    
    @reactive.Calc
    @reactive.event(input.yf_get)
    def end_get_date():
        return input.dt_rng()[1]

    @reactive.Calc
    @reactive.event(input.yf_get)
    def stock_data():
        START_DATE = start_get_date()
        END_DATE = end_get_date()
        return yf.download('GOOGL MSFT TSLA', START_DATE, END_DATE)
    
    @reactive.Calc
    @reactive.event(input.show)
    def start_date():
        return input.sdt()
    
    @reactive.Calc
    @reactive.event(input.show)
    def end_date():
        return input.edt()
    
    @reactive.Calc
    @reactive.event(input.show)
    def ticker():
        return input.sticker()
    
    @reactive.Calc
    @reactive.event(input.show)
    def plot_data():
        START_DATE = start_date()
        END_DATE = end_date()
        TICKER = ticker()

        # stock_data = yf.download('GOOGL MSFT TSLA', START_DATE, END_DATE)

        return stock_data()['Adj Close'].loc[START_DATE:END_DATE, TICKER]
    
    @output
    @render.plot
    @reactive.event(input.show) 
    async def line_plot():
        return plt.plot(plot_data())
