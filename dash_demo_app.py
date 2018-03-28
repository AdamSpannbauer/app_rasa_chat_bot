import glob

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

from rasa_nlu.model import Interpreter
from rasa_nlu.config import RasaNLUConfig

import utils.bot
from utils.downloader import download_charts

# read in most recent model build
model_dirs = sorted(glob.glob('./rasa_model/default/model_*/'))
model_path = model_dirs[-1]

# define config
args = {'pipeline': 'spacy_sklearn'}
config = RasaNLUConfig(cmdline_args=args)

# where `model_directory points to the folder the model is persisted in
interpreter = Interpreter.load(model_path, config)

# update chart data.. use back up data if error
try:
    app_data_path = 'data/app_chart_data.csv'
    download_charts(app_data_path)
except:
    print('using backup app data')
    app_data_path = 'data/backup_app_chart_data.csv'
# --------------------------------------------------

# init app and add stylesheet
app = dash.Dash()
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

# init a list of the sessions conversation history
conv_hist = []

# app ui
app.layout = html.Div([
    html.H3('Search App Charts Bot Demo', style={'text-align': 'center'}),
    html.Div([
        html.Div([
            html.Table([
                html.Tr([
                    # text input for user message
                    html.Td([dcc.Input(id='msg_input', value='hello', type='text')],
                            style={'valign': 'middle'}),
                    # message to send user message to bot backend
                    html.Td([html.Button('Send', id='send_button', type='submit')],
                            style={'valign': 'middle'})
                ])
            ])],
            style={'width': '325px', 'margin': '0 auto'}),
        html.Br(),
        html.Div(id='conversation')],
        id='screen',
        style={'width': '400px', 'margin': '0 auto'})
])


# trigger bot response to user inputted message on submit button click
@app.callback(
    Output(component_id='conversation', component_property='children'),
    [Input(component_id='send_button', component_property='n_clicks')],
    state=[State(component_id='msg_input', component_property='value')]
)
# function to add new user*bot interaction to conversation history
def update_conversation(click, text):
    global conv_hist

    # dont update on app load
    if click > 0:
        # call bot with user inputted text
        response, generic_response = utils.bot.respond(
            text,
            interpreter,
            app_data_path
        )
        # user message aligned left
        rcvd = [html.H5(text, style={'text-align': 'left'})]
        # bot response aligned right and italics
        rspd = [html.H5(html.I(r), style={'text-align': 'right'}) for r in response]
        if generic_response:
            generic_msg = 'i couldn\'t find any specifics in your message, here are some popular apps:'
            rspd = [html.H6(html.I(generic_msg))] + rspd
        # append interaction to conversation history
        conv_hist = rcvd + rspd + [html.Hr()] + conv_hist

        return conv_hist
    else:
        return ''


@app.callback(
    Output(component_id='msg_input', component_property='value'),
    [Input(component_id='conversation', component_property='children')]
)
def clear_input(_):
    return ''


# run app
if __name__ == '__main__':
    app.run_server()
