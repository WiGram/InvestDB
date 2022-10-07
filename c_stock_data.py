class YFinData:
    def __init__(self, yfin_data=None, tickers=None, start_date=None, end_date=None):
        self.yfin_data = yfin_data
        self.tickers = tickers
        self.start_date = start_date
        self.end_date = end_date
        self.stock_df = None
        self.returns_df = None
    
    def make_df(self):
        stock_df = self.yfin_data \
            .stack() \
            .reset_index() \
            .rename(columns={'level_1': 'Ticker'})
        
        stock_df.columns = stock_df \
            .columns \
            .str \
            .replace(' ', '_')
        
        self.stock_df = stock_df
        print('Attribute "stock_df" was assigned to this class object, see self.stock_df.')
    
    def get_df(self):
        if self.stock_df is not None:
            return self.stock_df
        else:
            self.make_df(self)
            return self.stock_df
    
    def get_returns(self):
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
