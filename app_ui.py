from shiny import ui
import app_dict as ad
# need Jinja2 installed (pip it) for displaying data frames

ui_dict = ad.ui_dict()

app_ui = ui.page_fluid(

    # Panel Side Bar
    ui.layout_sidebar(
        # ui.page_navbar(title='Navbar', id='nav_bar'),

        ui.panel_sidebar(
            ui.input_date_range(**ui_dict['i_date_range']),
            
            ui.input_action_button(id='yf_get', label='Get data'),

            ui.input_date(**ui_dict['i_start_dt']),
            ui.input_date(**ui_dict['i_end_dt']),

            ui.input_select(**ui_dict['select_ticker']),
            ui.input_action_button("show", "Show plot!"),
        ),

        ui.panel_main(
            ui.output_plot('line_plot')
        ),
    )
)
