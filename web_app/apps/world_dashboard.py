import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from web_app.app import app
import pandas as pd
from web_app.apps.helpers.helper_functions import get_tweets, get_polarity

df = pd.read_csv("/mnt/data/Events/CODE19/smart-disease-prediction-dashboard/")

COLUMNS = ['ARPU', 'Internet Usage', 'SMS Usage', 'Voice Usage']

COLORS = {
    'background': '#1e1e2a',
    'figure-background': '#28283c',
    'text': '#77d1d6',
}

TWEET = '''Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam ex magna, aliquet in magna in, 
        faucibus vestibulum enim. Suspendisse ut commodo augue. Proin vel facilisis sem. Quisque eget 
        mauris eu velit dictum auctor. Fusce lacinia nisl at ultrices aliquam. Nulla urna risus.'''

customer_id = 1
MONTHS = ['August', 'September', 'October', 'November', 'December', 'January']

SEGMENTS = list(df['Customer Segment'].unique())


def generate_scatter_plot(xaxis_column_name, yaxis_column_name,
                          xaxis_type, yaxis_type):
    # traces = []
    # for i in df['Customer Segment'].unique():
    #     df_by_segment = df[df['Customer Segment'] == i]
    #     traces.append(dict(
    #         x=df_by_segment[xaxis_column_name].unique(),
    #         y=df_by_segment[yaxis_column_name].unique(),
    #         mode='markers',
    #         opacity=0.7,
    #         marker={
    #             'size': 5,
    #             # 'line': {'width': 0.5, 'color': 'white'}
    #         },
    #         name=i
    #     ))
    return {
        # 'data': traces,
        'data': [
            {
                'x': df[xaxis_column_name].unique(),
                'y': df[yaxis_column_name].unique(),
                # 'x': df[xaxis_column_name],
                # 'y': df[yaxis_column_name],
                'mode': 'markers',
                'marker': {
                    'color': COLORS['text'],
                    'size': 5,
                },
            },
        ],
        'layout': {
            'title': 'Customer Segments Scatter Plot',
            'showlegend': False,
            'colorscale': 'balance',
            'legend': {
                'x': 0,
                'y': 1.0
            },
            'plot_bgcolor': COLORS['figure-background'],
            'paper_bgcolor': COLORS['figure-background'],
            'font': {
                'color': COLORS['text']
            },
            'transition': {
                'duration': 1500
            },
            'xaxis': {
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log',
            },
            'yaxis': {
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
        }
    }


def generate_bar_graph():
    segment_dict = dict(df['Customer Segment'].value_counts())
    widths = [0.5] * len(list(segment_dict.values()))
    return {
        'data': [
            {
                'x': list(segment_dict.values()),
                'y': list(segment_dict.keys()),
                'name': 'Internet Usage',
                'type': 'bar',
                'orientation': 'h',
                'width': widths,
                'marker': {
                    'color': '#ff9d76',
                }
            },
        ],
        'layout': {
            'title': 'Distribution of Users',
            'showlegend': False,
            'colorscale': 'balance',
            # 'legend': {
            #     'x': 0,
            #     'y': 1.0
            # },
            'plot_bgcolor': COLORS['figure-background'],
            'paper_bgcolor': COLORS['figure-background'],
            'font': {
                'color': COLORS['text']
            },
            'transition': {
                'duration': 1500
            },
            'xaxis': {
                'title': 'Number of Customers',
            },
            'yaxis': {
                'title': 'Customer Segments',
            },
        }
    }


def generate_pie_chart():
    return {
        'data': [
            {
                'values': get_polarity(),
                'type': 'pie',
                'labels': ['Negative', 'Positive', 'Neutral'],
                'hoverinfo': 'label+percent',
                'marker': {
                    'colors': ['#ff9d76', '#00adb5']
                },
            },
        ],
        'layout': {
            'plot_bgcolor': COLORS['background'],
            'paper_bgcolor': COLORS['background'],
            'font': {
                'color': COLORS['text']
            },
            'showlegend': False,
        }
    }


layout = html.Div([
    html.Div([
        html.Div([
            html.H3(
                html.Strong(
                    '''
                    ANALYTICS DASHBOARD
                    ''', id='customdash'),
            ),
        ], className='one-half column'),

        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='crossfilter-xaxis-column',
                    options=[{'label': i, 'value': i} for i in COLUMNS],
                    value='ARPU'
                ),
                dcc.RadioItems(
                    id='crossfilter-xaxis-type',
                    options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                    value='Linear',
                    labelStyle={'display': 'inline-block'}
                )
            ], className='one-half column', id='xaxis'),
            html.Div([
                dcc.Dropdown(
                    id='crossfilter-yaxis-column',
                    options=[{'label': i, 'value': i} for i in COLUMNS],
                    value='Internet Usage'
                ),
                dcc.RadioItems(
                    id='crossfilter-yaxis-type',
                    options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                    value='Linear',
                    labelStyle={'display': 'inline-block'}
                )
            ], className='one-half column', id='yaxis')
        ], className='one-half column container')
    ], className='container'),

    html.Div([
        html.Div([
            dcc.Graph(
                id='overall-scatter-plot',
                style={'width': '100%'},
                figure=generate_scatter_plot('ARPU', 'Internet Usage', 'Linear', 'Linear')
            )
        ], className='one-half column', style={'width': '48%'}),

        html.Div([
            dcc.Graph(
                id='overall-bar-graph',
                figure=generate_bar_graph()
            ),
        ], className='one-half column'),

    ], className='container'),

    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.Strong('LIVE TWEETS', id='tweet-title', className='titles', style={'float': 'left'}),
                    html.Button([
                        'REFRESH'
                    ], id='refresh-button', className='two columns'),
                ]),
                html.Div([
                    get_tweets()
                ], id='tweet-container')
            ], className='eight columns', id='tweet-display'),
            html.Div([
                html.Strong('TWEET POLARITY', className='titles'),
                html.Div([
                    dcc.Graph(
                        id='polarity-pie-chart',
                        figure=generate_pie_chart()
                    )
                ])
            ], className='four columns', id='tweet-polarity-display')
        ], className='container'),
    ], id='last-div'),

    html.Div([
        html.Button([
            dcc.Link('PREDICTION DASHBOARD', href='/apps/customer_dashboard')
        ], id='page2-link', className='three columns'),
    ], className='container', id='page2-link-container')

])


@app.callback(
    Output('overall-scatter-plot', 'figure'),
    [Input('crossfilter-xaxis-column', 'value'),
     Input('crossfilter-yaxis-column', 'value'),
     Input('crossfilter-xaxis-type', 'value'),
     Input('crossfilter-yaxis-type', 'value')],
)
def update_scatter_plot(xaxis_column, yaxis_column, xaxis_type, yaxis_type):
    return generate_scatter_plot(xaxis_column, yaxis_column, xaxis_type, yaxis_type)


@app.callback(
    Output('tweet-container', 'children'),
    [Input('refresh-button', 'n_clicks')],
    # [State('customer-id', 'value')]
)
def service_usage_graph(n_clicks):
    return get_tweets()
