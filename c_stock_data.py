import pandas as pd
import yfinance as yf
from datetime import date


class YFinData:
    def __init__(
        self,
        yfin_data: pd.DataFrame = None,
        tickers: list[str] = None,
        start_date: date = None,
        end_date: date = None,
        file_path: str = None
    ):

        self.yfin_data = yfin_data
        self.tickers = tickers
        self.start_date = start_date
        self.end_date = end_date
        self.file_path = file_path
        self.stock_df = None
        self.returns_df = None
    
    def set_tickers(self, tickers: list[str]):
        """
        Params
        ------
        tickers: str object of tickers separated by a single space

        Comment
        -------
        Set tickers if this wasn't set when initialising the object
        """
        self.tickers = tickers
        return None
    
    def set_start_date(self, start_date: date):
        """
        Params
        ------
        start_date: datetime.date object

        Comment
        -------
        Set start_date if this wasn't set when initialising the object
        """
        self.start_date = start_date
        return None
    
    def set_end_date(self, end_date: date):
        """
        Params
        ------
        end_date: datetime.date object

        Comment
        -------
        Set end_date if this wasn't set when initialising the object
        """
        self.end_date = end_date
        return None
    
    def __helper_set_ticker_as_column__(self, yfin_data, ticker=None):
        
        # Declare a ticker_str for use in the output dataframe
        ticker_str: str = None

        # If we provide list of tickers then automatically use the first one
        if ticker is not None:
            ticker_str = ticker[0]

        # If we need the tickers then take the first one
        elif len(self.tickers) == 1:
            ticker_str = self.tickers[0]
        
        if isinstance(yfin_data.columns, pd.MultiIndex):
            stock_df = yfin_data \
                .stack() \
                .reset_index() \
                .rename(columns={'level_1': 'Ticker'})
        elif ticker_str is not None:
            yfin_data = yfin_data.reset_index()
            yfin_data['Ticker'] = ticker_str
            cols = ['Date', 'Ticker', 'Adj Close', 'Close', 'High', 'Low', 'Open', 'Volume']
            stock_df = yfin_data[cols]
        else:
            print('Problem - please provide ticker')
            stock_df = None
        return stock_df
    
    def __helper_transform_yahoo_df__(
        self,
        yfin_data: pd.DataFrame = None,
        ticker: str = None
    ):
        """
        Params
        ------
        yfin_data: dataframe from yahoo finance api
        ticker: string containing one single ticker, used when only one ticker is added

        Comment
        -------
        Set end_date if this wasn't set when initialising the object
        """

        # Ensure we have a yahoo data frame
        if yfin_data is None:
            yfin_data = self.yfin_data        
        
        # Make sure Tickers are collected in a column
        stock_df = self.__helper_set_ticker_as_column__(yfin_data, ticker)
            
        # Replace spaces in column names with underscores
        stock_df.columns = stock_df \
            .columns \
            .str \
            .replace(' ', '_')
        
        # Enforce date type for Date column
        stock_df.Date = stock_df.Date.dt.date
        
        # Assign dataframe to object
        return stock_df
    
    def __helper_load_yfin_data__(self, ticker: str = None):
        if self.stock_df is not None:
            print('Using existing df')
        if self.yfin_data is not None:
            self.stock_df = self.__helper_transform_yahoo_df__(ticker)
            print('Prices dataframe now available, see self.stock_df')
        return None
    
    def populate_data(self):
        """
        Params
        ------
        None

        Comment
        -------
        Reformat the dataframe to support variable amount of tickers
        """

        # Check if yfindata is populated        
        self.__helper_load_yfin_data__()
        
        if self.tickers is None:
            print('Tickers are missing')
            return 'Tickers are missing'
        
        if self.start_date is None:
            print('start_date is missing')
            return 'start_date is missing'
        
        if self.end_date is None:
            print('end_date is missing')
            return 'end_date is missing'
        
        try:
            stock_df = pd.read_parquet(path=self.file_path, engine='pyarrow')
            print('File found - using stored data')
            start_date_data = stock_df.Date.min()
            end_date_data = stock_df.Date.max()
            df_tickers = ' '.join(stock_df.Ticker.unique().tolist())

        except FileNotFoundError:
            print('File not found - data being dowloaded')
            TICKERS = ' '.join(self.tickers)
            new_stock_df = yf.download(TICKERS, self.start_date, self.end_date)
            self.stock_df = self.__helper_transform_yahoo_df__(new_stock_df)
            return 'Data was downloaded'

        except Exception as e:
            print('Unexpected error: ', e)
            return e
        
        added_tickers = self.__helper_added_tickers__(stock_df)
        start_date_req = self.__helper_start_date__(stock_df)
        end_date_req = self.__helper_end_date__(stock_df)

        if len(added_tickers) > 0:
            added_tickers_str = ' '.join(added_tickers)
            new_ticker_data = yf.download(
                added_tickers_str, start_date_req, end_date_req
            )
            append_df = self.__helper_transform_yahoo_df__(new_ticker_data, added_tickers)
            stock_df = pd.concat([stock_df, append_df], ignore_index=True)
        
        if start_date_req < start_date_data:
            print('Should download earlier data for existing tickers')
            earlier_stock_data = yf.download(df_tickers, start_date_req, start_date_data - pd.offsets.BDay(1))
            pre_data = self.__helper_transform_yahoo_df__(earlier_stock_data)

            # Yahoo finance dates are fuzzy - make a deterministic cutoff
            pre_data = pre_data.loc[pre_data.Date < start_date_data, :]
            stock_df = pd.concat([stock_df, pre_data], ignore_index=True)
        else:
            print('Starts as early as possible')
        
        if end_date_data < end_date_req:
            print('Should download earlier data for existing tickers')
            later_stock_data = yf.download(df_tickers, end_date_data + pd.offsets.BDay(1), end_date_req)
            post_data = self.__helper_transform_yahoo_df__(later_stock_data)

            # Yahoo finance dates are fuzzy - make a deterministic cutoff
            post_data = post_data.loc[post_data.Date > end_date_data, :]
            stock_df = pd.concat([stock_df, post_data], ignore_index=True)
        else:
            print('Ends as late as possible')
        
        self.stock_df = stock_df

        return 'Import job done'
    
    def get_df(self):
        """
        Params
        ------
        None

        Comment
        -------
        Return dataframe if it exists
        """
        if self.stock_df is not None:
            return self.stock_df
        else:
            self.populate_data()
            return self.stock_df
    
    def get_ticker_prices(self):
        return None

    def get_returns(self):
        """
        Params
        ------
        None

        Comment
        -------
        Compute log returns from prices and assign to object instance
        """
        if self.stokc_df is None:
            self.mk_df(self)
        
        cols = self.stock_df

        self.returns_df = self.stock_df \
            .sort_values(by=['Ticker', 'Date']) \
            .set_index(['Ticker', 'Date']) \
            .diff() \
            .reset_index() \
            .loc[:, cols]
        print(
            'Attribute "returns_df" was assigned to this class instance, '\
            ' see self.returns_df.'
        )

    def __helper_added_tickers__(self, stock_df):
        """
        Params
        ------
        stock_df: pandas.Dataframe holding stock price information

        Comment
        -------
        We receive only the tickers we don't already have stored.
        This allows the download size to be reduced.
        """

        DF_TICKERS = stock_df.Ticker.unique().tolist()

        MSNG_TICKERS = list(set(self.tickers).difference(DF_TICKERS))
        ADDED_TICKERS = ' '.join(MSNG_TICKERS)

        print('Tickers to be added: ', ADDED_TICKERS)

        return MSNG_TICKERS
    
    def __helper_start_date__(self, stock_df):
        """
        Params
        ------
        stock_df: pandas.Dataframe holding stock price information

        Comment
        -------
        We make sure to expand the start date if the existing data
        starts earlier than our set start date.
        """
        START_DATE_DATA = stock_df.Date.min()
        START_DATE_REQ = min(self.start_date, START_DATE_DATA)
        return START_DATE_REQ
    
    def __helper_end_date__(self, stock_df):
        """
        Params
        ------
        stock_df: pandas.Dataframe holding stock price information

        Comment
        -------
        We make sure to expand the end date if the existing data
        ends later than our set end date.
        """
        END_DATE_DATA = stock_df.Date.max()
        END_DATE_REQ = max(self.end_date, END_DATE_DATA)
        return END_DATE_REQ
    
    def write_df(self):
        if self.file_path is None:
            print('Set file_path using set_file_path method and try again')
            return None
        
        if self.stock_df is not None:
            self.stock_df.to_parquet(self.file_path)
            print('Dataframe is saved to: ', self.file_path)
            return None
        
        print('Dataframe missing. Set parameters and call populate_data method')
        return None
