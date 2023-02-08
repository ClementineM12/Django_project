import dash
import plotly.graph_objs as go

# import dash_bootstrap_components as dbc
from dash import dcc, html, no_update, dash_table
from dash.dependencies import Input, Output, State
from django_plotly_dash import DjangoDash
import dash_bootstrap_components as dbc

import pandas as pd
import numpy as np
import scipy

# import io
# import datetime
# import base64
import plotly.express as px
import plotly.figure_factory as ff

df = pd.read_csv('./documents/updated_file.csv')
app = DjangoDash('Dash1', add_bootstrap_links=False)  
app.css.append_css({ "external_url" : "/static/custom.css" })

def get_categorical_columns(df):
    """
    Returns a list of column names that contain categorical values in a Pandas DataFrame.
    """
    categorical_columns = []
    for column in df.columns[:-1]:
        if df[column].dtype in [pd.Categorical, "category"]:
            categorical_columns.append(column)
    return categorical_columns

def get_numerical_columns(df):
    """
    Returns a list of column names that contain numerical values in a Pandas DataFrame.
    """
    numerical_columns = []
    for column in df.columns:
        if df[column].dtype in [float, int, np.float64, np.int64]:
            numerical_columns.append(column)
    return numerical_columns

vars_cat = get_categorical_columns(df)
vars_cont = get_numerical_columns(df)



# Pie plot
bar_colors = ['#439A97', '#CBEDD5']

df['count'] = df.index
pie = df.groupby(df.columns[-2]).count()['count'] / len(df)

fig_pie = px.pie(pie.reset_index(),
                 values='count',
                 names=df.columns[-2],
                 hole=0.3,
                 color_discrete_sequence=bar_colors)

fig_pie.update_layout(width=320,
                      height=250,
                      margin=dict(l=30, r=10, t=10, b=10),
                      paper_bgcolor='rgba(0,0,0,0)',
                      )

# Barplot
cat_pick = vars_cat[0]
bar_df = df.groupby([df.columns[-2], cat_pick]).count()['count'].reset_index()

bar_colors = ['#439A97', '#CBEDD5']
fig_bar = px.bar(bar_df,
                 x=cat_pick,
                 y="count",
                 color=df.columns[-2],
                 barmode='group',
                 color_continuous_scale=bar_colors
                 )

fig_bar.update_layout(width=500,
                      height=340,
                      margin=dict(l=40, r=20, t=20, b=30),
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',
                      legend_title=None,
                      yaxis_title=None,
                      xaxis_title=None,
                      showlegend=False,
                      legend=dict(
                          orientation="h",
                          yanchor="bottom",
                          y=1.02,
                          xanchor="right",
                          x=1
                          )
                      )
fig_bar.update_coloraxes(showscale=False)

# Distribution Chart
cont_pick = vars_cont[0]
def get_target_values(df, target_column, cont_pick):
    result = {}
    unique_targets = df[target_column].unique()
    for i, target in enumerate(unique_targets):
        if isinstance(target, int):
            if ' ' in target:
                result[f'{target.replace(" ", "_")}'] = df[df[target_column] == target][cont_pick].values.tolist()
        else:
            result[f'{target}'] = df[df[target_column] == target][cont_pick].values.tolist()
    return result

dictionary = get_target_values(df, df.columns[-2], cont_pick)

fig_dist = ff.create_distplot(hist_data=list(dictionary.values()),
                              group_labels=list(dictionary.keys()),
                              show_hist=False,
                              colors=bar_colors)

fig_dist.update_layout(width=500,
                       height=340,
                       margin=dict(t=20, b=20, l=40, r=20),
                       paper_bgcolor='rgba(0,0,0,0)',
                       plot_bgcolor='rgba(0,0,0,0)',
                       legend=dict(
                           orientation="h",
                           yanchor="bottom",
                           y=1.02,
                           xanchor="right",
                           x=1
                           )
                       )

# Heatmap

if df.columns[-2] in vars_cont:
    vars_cont.remove(df.columns[-2])
corr_pick = vars_cont

df_corr = df[corr_pick].corr()
x = list(df_corr.columns)
y = list(df_corr.index)
z = df_corr.values

colorscale = [[0, '#DAE2B6'], [0.5, '#439A97'], [1, '#F0E9D2']]

fig_corr = ff.create_annotated_heatmap(
    z,
    x=x,
    y=y,
    annotation_text=np.around(z, decimals=2),
    hoverinfo='z',
    colorscale=colorscale,
)
fig_corr.update_layout(width=1040,
                       height=300,
                       margin=dict(l=40, r=20, t=20, b=20),
                       paper_bgcolor='rgba(0,0,0,0)'
                       )


sidebar = html.Div(
    [
        # dbc.Row(
        #     [
        #         html.H5('Settings',
        #                 style={'margin-top': '12px', 'margin-left': '24px'})
        #         ],
        #     style={"height": "5%", 'margin': '3px'},
        #     className='settings'
        #     ),
        dbc.Row(
            [
                html.Div([
                    html.P('Categorical Variable',
                           style={'margin-top': '8px', 'margin-bottom': '5px'},
                           className='paragraph'),
                    dcc.Dropdown(id='my-cat-picker', multi=False, value=vars_cat[0],
                                 options=[{'label': x, 'value': x}
                                          for x in vars_cat],
                                 style={'width': '320px'}
                                 ),
                    html.P('Continuous Variable',
                           style={'margin-top': '16px', 'margin-bottom': '5px'},
                           className='paragraph'),
                    dcc.Dropdown(id='my-cont-picker', multi=False, value=vars_cont[0],
                                 options=[{'label': x, 'value': x}
                                          for x in vars_cont],
                                 style={'width': '320px', 'fontColor':'#678983'}
                                 ),
                    html.P('Continuous Variables for Correlation Matrix',
                           style={'margin-top': '16px', 'margin-bottom': '5px'},
                           className='paragraph'),
                    dcc.Dropdown(id='my-corr-picker', multi=True,
                                 value=vars_cont + [df.columns[-2]],
                                 options=[{'label': x, 'value': x}
                                          for x in vars_cont + [df.columns[-2]]],
                                 style={'width': '320px'}
                                 ),
                    html.Button(id='my-button', n_clicks=0, children='apply',
                                style={'margin-top': '16px', 'margin-bottom': '16px',
                                'margin-left':'100px'},
                                className='apply-button'),
                    html.Hr()
                    ]
                    )
                ],
            style={'height': '55%', 'margin': '3px'}),
        dbc.Row(
            [
                html.P('', className='font-titles'),
                dcc.Graph(figure=fig_pie)
                ],
            style={"height": "10%", 'flex-direction': 'column', 'margin-bottom': '10px',
            'text-align':'center'}
            )
        ], style={'margin-right':'8px', 'margin-right':'8px'}
    )

content = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div([
                            html.P(id='bar-title',
                                   children='Distribution of Categorical Variable',
                                   className='font-titles'),
                            dcc.Graph(id="bar-chart",
                                      figure=fig_bar,
                                      className='bg-light')])
                        ], className='col',
                        style={'padding-right': '20px'}),
                dbc.Col(
                    [
                        html.Div([
                            html.P(id='dist-title',
                                   children='Distribution of Continuous Variable',
                                   className='font-titles'),
                            dcc.Graph(id="dist-chart",
                                      figure=fig_dist,
                                      className='bg-light')])
                        ], className='col')
                ],
            style={'height': '50%',
                   'margin-top': '1.3px', 'margin-left': '8px',
                   'margin-bottom': '8px', 'margin-right': '8px'}),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div([
                            html.P('Correlation Matrix Heatmap',
                                   className='font-titles'),
                            dcc.Graph(id='corr-chart',
                                      figure=fig_corr,
                                      className='bg-light')])
                        ])
            ],
            style={"height": "50%", 'margin': '8px'}
            )
        ]
    )

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(sidebar, className='sidebar'),
                dbc.Col(content, width=9)
                ],
            ),
        ],
    style={'background-color': 'transparent', 'width': '100%', 'height': '100%'},
    fluid=True,
    )

# Apply calbacks  
@app.callback(Output('bar-chart', 'figure'),
              Output('bar-title', 'children'),
              Input('my-button', 'n_clicks'),
              State('my-cat-picker', 'value'))
def update_bar(n_clicks, cat_pick):
    bar_df = df.groupby([df.columns[-2], cat_pick]).count()['count'].reset_index()

    fig_bar = px.bar(bar_df,
                     x=cat_pick,
                     y="count",
                     color=df.columns[-2],
                     barmode='group',
                     color_continuous_scale=bar_colors,
                     )

    fig_bar.update_layout(width=500,
                          height=340,
                          margin=dict(l=40, r=20, t=20, b=30),
                          paper_bgcolor='rgba(0,0,0,0)',
                          plot_bgcolor='rgba(0,0,0,0)',
                          legend_title=None,
                          yaxis_title=None,
                          xaxis_title=None,
                          showlegend=False,
                          legend=dict(
                              orientation="h",
                              yanchor="bottom",
                              y=1.02,
                              xanchor="right",
                              x=1
                              )
                          )
    fig_bar.update_coloraxes(showscale=False)
    title_bar = 'Distribution of Categorical Variable: ' + cat_pick

    return fig_bar, title_bar


@app.callback(Output('dist-chart', 'figure'),
              Output('dist-title', 'children'),
              Input('my-button', 'n_clicks'),
              State('my-cont-picker', 'value'))
def update_dist(n_clicks, cont_pick):
    dictionary = get_target_values(df, df.columns[-2], cont_pick)

    fig_dist = ff.create_distplot(hist_data=list(dictionary.values()),
                                  group_labels=list(dictionary.keys()),
                                  show_hist=False,
                                  colors=bar_colors)

    fig_dist.update_layout(width=500,
                           height=340,
                           margin=dict(t=20, b=20, l=40, r=20),
                           paper_bgcolor='rgba(0,0,0,0)',
                           plot_bgcolor='rgba(0,0,0,0)',
                           legend=dict(
                               orientation="h",
                               yanchor="bottom",
                               y=1.02,
                               xanchor="right",
                               x=1
                               )
                           )

    title_dist = 'Distribution of Continuous Variable: ' + cont_pick

    return fig_dist, title_dist


@app.callback(Output('corr-chart', 'figure'),
              Input('my-button', 'n_clicks'),
              State('my-corr-picker', 'value'))
def update_corr(n_clicks, corr_pick):
    df_corr = df[corr_pick].corr()
    x = list(df_corr.columns)
    y = list(df_corr.index)
    z = df_corr.values

    fig_corr = ff.create_annotated_heatmap(
        z,
        x=x,
        y=y,
        annotation_text=np.around(z, decimals=2),
        hoverinfo='z',
        colorscale=colorscale
    )

    fig_corr.update_layout(width=1040,
                           height=300,
                           margin=dict(l=40, r=20, t=20, b=20),
                           paper_bgcolor='rgba(0,0,0,0)'
                           )

    return fig_corr


# if __name__ == "__main__":
#     app.run_server(debug=True, port=1234)