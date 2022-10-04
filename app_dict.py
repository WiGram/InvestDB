input_dict = {
    'tickers': {'choices': {
        'GOOGL': 'Google',
        'MSFT': 'Microsoft',
        'TSLA': 'Tesla'
    }},
}


ui_dict = {
    'line_plot': {'id': 'line_plot'},
    'select_ticker': {
        'id': 'sticker',
        'label': 'Select',
        **input_dict['tickers']
    },
    'input_sdt': {'id': 'sdt', 'label': 'Date input', 'value': '2020-01-01'},
    'input_edt': {'id': 'edt', 'label': 'Date input', 'value': '2022-01-01'},
    'input_date_range': {
        'id': 'dt_rng',
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
