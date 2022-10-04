from shiny import ui
from app_dict import ui_dict
# need Jinja2 installed (pip it) for displaying data frames

app_ui = ui.page_fluid(

    # Panel Side Bar
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_date_range(**ui_dict['input_date_range']),
            
            ui.input_action_button(id='yf_get', label='Get data'),

            ui.input_date(**ui_dict['input_sdt']),
            ui.input_date(**ui_dict['input_edt']),

            ui.input_select(**ui_dict['select_ticker']),
            ui.input_action_button("show", "Show plot!"),
        ),

        ui.panel_main(
            ui.output_plot('line_plot')
        ),
    )
)
