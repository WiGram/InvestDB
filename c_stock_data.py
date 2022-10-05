class StockData:
    def __init__(self, yfin_data):
        self.yfin_data = yfin_data
        self.stock_df = None
        self.returns_df = None
    
    def mk_df(self):
        stock_df = self.yfin_data.stack().reset_index().rename(columns={'level_1': 'Ticker'})
        stock_df.columns = stock_df.columns.str.replace(' ', '_')
        self.stock_df = stock_df
        print('Attribute "stock_df" was assigned to this class object, see self.stock_df.')
    
    def get_returns(self):
        if self.stokc_df is None:
            self.mk_df(self)
        
        cols = self.stock_df

        self.returns_df = self.stock_df \
            .sort_values(by=['Ticker', 'Date']) \
            .set_index(['Ticker', 'Date']) \
            .diff() \
            .reset_index() \
            [cols]
        print('Attribute "returns_df" was assigned to this class instance, see self.returns_df.')
