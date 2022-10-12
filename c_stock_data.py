import pandas as pd
import yfinance as yf


class YFinData:
    def __init__(
        self, yfin_data=None, 
        tickers=None, start_date=None, end_date=None,
        file_path=None
    ):

        self.yfin_data = yfin_data
        self.tickers = tickers
        self.start_date = start_date
        self.end_date = end_date
        self.file_path = file_path
        self.stock_df = None
        self.returns_df = None
    
    def set_tickers(self, tickers):
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
    
    def set_start_date(self, start_date):
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
    
    def set_end_date(self, end_date):
        """
        Params
        ------
        end_date: datetime.date object

        Comment
        -------
        Set end_date if this wasn't set when initialising the object
        """
        self.end_dtae = end_date
        return None
    
    def __helper_transform_yahoo_df__(self, yfin_data=None):
        if yfin_data is None:
            yfin_data = self.yfin_data
        
        stock_df = yfin_data \
                .stack() \
                .reset_index() \
                .rename(columns={'level_1': 'Ticker'})
        
        # Replace spaces in column names with underscores
        stock_df.columns = stock_df \
            .columns \
            .str \
            .replace(' ', '_')
        
        # Assign dataframe to object
        return stock_df
    
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
        if self.yfin_data is not None:
            # Pivot tickers columns into single column
            self.stock_df = self.__helper_transform_yahoo_df__()
            print('Prices dataframe now available, see self.stock_df.')
            return None
        
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
            print('File found - using stored data')
            stock_df = pd.read_parquet(path=self.file_path, engine='pyarrow')
            start_date_data = stock_df.Date.min().date()
            end_date_data = stock_df.Date.max().date()
            df_tickers = ' '.join(stock_df.Ticker.unique().tolist())

        except FileNotFoundError:
            print('File not found - data being dowloaded')
            TICKERS = ' '.join(self.tickers)
            new_stock_df = yf.download(TICKERS, self.start_date, self.end_date)
            self.stock_df = new_stock_df
            return 'Data was downloaded'

        except Exception as e:
            print('Unexpected error: ', e)
            return e
        
        added_tickers = self.__helper_added_tickers__(stock_df)
        start_date_req = self.__helper_start_date__(stock_df)
        end_date_req = self.__helper_end_date__(stock_df)

        if len(added_tickers) > 3:
            new_ticker_data = yf.download(
                added_tickers, start_date_req, end_date_req
            )
            append_df = self.__helper_transform_yahoo_df__(new_ticker_data)
            stock_df = pd.concat([stock_df, append_df], ignore_index=True)
        
        if start_date_req < start_date_data:
            print('Should download earlier data for existing tickers')
            earlier_stock_data = yf.download(df_tickers, start_date_req, start_date_data)
            earlier_ticker_data = self.__helper_transform_yahoo_df__(earlier_stock_data)
            stock_df = pd.concat([stock_df, earlier_ticker_data], ignore_index=True)
        else:
            print('Starts as early as possible')
        
        if end_date_data < end_date_req:
            print('Should download earlier data for existing tickers')
            later_stock_data = yf.download(df_tickers, end_date_data, end_date_req)
            later_ticker_data = self.__helper_transform_yahoo_df__(later_stock_data)
            stock_df = pd.concat([stock_df, later_ticker_data], ignore_index=True)
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

        MSNG_TICKERS = set(self.tickers).difference(DF_TICKERS)
        ADDED_TICKERS = ' '.join(MSNG_TICKERS)

        print('Tickers to be added: ', ADDED_TICKERS)

        return ADDED_TICKERS
    
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
        START_DATE_DATA = stock_df.Date.min().date()
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
        END_DATE_DATA = stock_df.Date.max().date()
        END_DATE_REQ = max(self.end_date, END_DATE_DATA)
        return END_DATE_REQ

