from shiny import render, reactive
from matplotlib import pyplot as plt
import c_stock_data as SD
import pandas as pd


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
        df_allocations = pd.read_excel('Data/allocations.xlsx')
        TICKERS = df_allocations['Ticker'].to_list()

        FILE_PATH = 'Data/stock_df.parquet'
        START_DATE = start_get_date()
        END_DATE = end_get_date()

        stock_data = SD.YFinData(
            tickers=TICKERS,
            start_date=START_DATE,
            end_date=END_DATE,
            file_path=FILE_PATH
        )
        
        return stock_data.get_df()
    
    @reactive.Calc
    @reactive.event(input.show)
    def start_date():
        return input.i_start_dt()
    
    @reactive.Calc
    @reactive.event(input.show)
    def end_date():
        return input.i_end_dt()
    
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

        df = stock_data()
        df = df.pivot(index='Date', columns='Ticker', values='Adj_Close')

        return df.loc[START_DATE:END_DATE, TICKER]
    
    @output
    @render.plot
    @reactive.event(input.show) 
    async def line_plot():
        return plt.plot(plot_data())
