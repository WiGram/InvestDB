import pandas as pd


def ui_dict():
    try:
        df_allocations = pd.read_excel('Data/allocations.xlsx')
        TICKERS = df_allocations['Ticker'].to_list()
        COMPANIES = df_allocations['Company'].to_list()
        choices_dict = dict(zip(TICKERS, COMPANIES))
    except:
        choices_dict = {
            'GOOGL': 'Google',
            'MSFT': 'Microsoft',
            'TSLA': 'Tesla',
            'NFLX': 'Netflix'
        }

    ui_dict = {
        'line_plot': {'id': 'line_plot'},
        'select_ticker': {
            'id': 'sticker',
            'label': 'Select',
            'choices': choices_dict,
        },
        'i_start_dt': {
            'id': 'i_start_dt',
            'label': 'Date input',
            'value': '2020-01-01'
        },
        'i_end_dt': {
            'id': 'i_end_dt',
            'label': 'Date input',
            'value': '2022-01-01'
        },
        'i_date_range': {
            'id': 'i_date_range',
            'label': 'Choose stock range',
            'start': "2010-01-01",
            'end': "2022-12-31",
            'min': "2010-01-01",
            'max': "2022-12-31",
            'format': "yyyy-mm-dd",
            'language': 'en-GB',
            'separator': " - "
        }
    }
    return ui_dict
