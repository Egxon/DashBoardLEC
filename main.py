import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash import *
import asyncio
from PIL import Image
import sqlite3
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt

from PIL import Image
import base64
import dash_bootstrap_components as dbc
from dash_bootstrap_components.themes import LUX
from dash_bootstrap_templates import load_figure_template
from packaging import markers

import plotly.graph_objects as go
import connect_bd
import graph_position
import request
############################################################






##############################################################

# Initialisation de l'application Dash
app = Dash(external_stylesheets=[dbc.themes.SLATE], suppress_callback_exceptions=True)
cur = connect_bd.getBD()
conn = connect_bd.getConBD()
image1_filename = 'images/Minimap.jpg'
polar_light = base64.b64encode(open(image1_filename, 'rb').read())
final_pos = graph_position.getGraphPos()
final_pos2 = graph_position.getGraphPosTMP()
Oner = graph_position.getOner()

# Get All Datas et DF
name = request.getName()
team = request.getTeam()
df = request.getDf()
df2 = request.getDf2()
df3 = request.getDf3()
df4 = request.getDf4()
name_tmp = request.getNameTmp()
match = request.getMatch()

totalG = df[(df['matchUrn'] == "esports:match:b3590072-d7dd-4d8c-b307-b671b3760075") & (df['current'] == "1")]
pie = px.pie(df2, values='KP', names='name', title="KP", width=800)
player_data = df3[df3['namePlayer'] == "T1 Zeus"]
match_data = df4[df4['MatchId'] == "esports:match:b3590072-d7dd-4d8c-b307-b671b3760075"]

choice = {"One Game": "One Game",
          "All Game": "All Game"}

opt = [
    {'label': 1, 'value': 1},
    {'label': 2, 'value': 2}
]

matchD = {}
matchN = {}

for i in match:
    matchD[i[2]] = [i[0] + " VS " + i[1]]

for i in match:
    matchN[i[0] + " VS " + i[1]] = [i[2]]

scatter2 = px.scatter(final_pos2, x='posx', y='posy', color="name", animation_frame="gameTime", range_x=[0, 15000],
                      range_y=[0, 15000])
scatter2.update_traces(marker_size=10)

scatter2.update_layout(
    autosize=True,
    width=1000,
    height=1000,
    images=[dict(
        source='data:image/jpg;base64,{}'.format(polar_light.decode()),
        xref="paper", yref="paper",
        x=0, y=1,  # position of the upper left corner of the image in subplot 1,1
        sizex=1, sizey=1,  # sizex, sizey are set by trial and error
        xanchor="left",
        yanchor="top",
        # height="800",

        sizing="stretch",
        layer="below")])

scatter = px.scatter(Oner, x='posx', y='posy', color="name", range_x=[0, 15000], range_y=[0, 15000])
scatter.update_traces(marker_size=20)

scatter.update_layout(
    autosize=True,
    width=1000,
    height=1000,
    images=[dict(
        source='data:image/jpg;base64,{}'.format(polar_light.decode()),
        xref="paper", yref="paper",
        x=0, y=1,  # position of the upper left corner of the image in subplot 1,1
        sizex=1, sizey=1,  # sizex, sizey are set by trial and error
        xanchor="left",
        yanchor="top",
        # height="800",

        sizing="stretch",
        layer="below")])

scatterOner = px.scatter(Oner, x='posx', y='posy', color="current", range_x=[0, 15000], range_y=[0, 15000])
scatterOner.update_traces(marker_size=10)

scatterOner.update_layout(
    autosize=True,
    width=1000,
    height=1000,
    images=[dict(
        source='data:image/jpg;base64,{}'.format(polar_light.decode()),
        xref="paper", yref="paper",
        x=0, y=1,  # position of the upper left corner of the image in subplot 1,1
        sizex=1, sizey=1,  # sizex, sizey are set by trial and error
        xanchor="left",
        yanchor="top",
        # height="800",

        sizing="stretch",
        layer="below")])

# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Définition du layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Match", href="/page-match")),
            dbc.NavItem(dbc.NavLink("Stat", href="/page-stat")),
            dbc.NavItem(dbc.NavLink("Graphique", href="/page-graphique")),
            dbc.NavItem(dbc.NavLink("Map", href="/page-map")),
        ],
        brand="Mon Dashboard",
        brand_href="/",
        color="primary",
        dark=True,
        expand="lg",
    ),
    dbc.Container(id='page-content', className='mt-4'),
])


@app.callback(

    Output(component_id='graph-BEG', component_property='figure'),
    Input(component_id='menu', component_property='value'),
    prevent_initial_call=True
)
def update_BEG(player):
    # En fonction de la valeur sélectionnée dans le premier Dropdown,
    # vous pouvez définir les options du deuxième Dropdown ici.
    # final_pos2 = final_pos[(final_pos['current'] == currIdPos) & (final_pos['matchUrn'] == matchIdPos )]
    pos = graph_position.getBegPlayer(player)
    fig = px.scatter(pos, x='posx', y='posy', color='current', animation_frame="gameTime",range_x=[0, 15000], range_y=[0, 15000])
    fig.update_traces(marker_size=10)

    fig.update_layout(
        autosize=True,
        width=1000,
        height=1000,
        images=[dict(
            source='data:image/jpg;base64,{}'.format(polar_light.decode()),
            xref="paper", yref="paper",
            x=0, y=1,  # position of the upper left corner of the image in subplot 1,1
            sizex=1, sizey=1,  # sizex, sizey are set by trial and error
            xanchor="left",
            yanchor="top",
            # height="800",

            sizing="stretch",
            layer="below")])

    return fig


@app.callback(

    Output(component_id='graph-pos', component_property='figure'),
    Input(component_id='match-POS', component_property='value'),
    Input(component_id='series-POS', component_property='value'),
    prevent_initial_call=True
)
def update_POS(matchIdPos, currIdPos):
    # En fonction de la valeur sélectionnée dans le premier Dropdown,
    # vous pouvez définir les options du deuxième Dropdown ici.
    # final_pos2 = final_pos[(final_pos['current'] == currIdPos) & (final_pos['matchUrn'] == matchIdPos )]
    pos = graph_position.getCurrent(currIdPos)
    fig = px.scatter(pos, x='posx', y='posy', color="name", animation_frame="gameTime", range_x=[0, 15000],
                     range_y=[0, 15000])
    fig.update_traces(marker_size=10)

    fig.update_layout(
        autosize=True,
        width=1000,
        height=1000,
        images=[dict(
            source='data:image/jpg;base64,{}'.format(polar_light.decode()),
            xref="paper", yref="paper",
            x=0, y=1,  # position of the upper left corner of the image in subplot 1,1
            sizex=1, sizey=1,  # sizex, sizey are set by trial and error
            xanchor="left",
            yanchor="top",
            # height="800",

            sizing="stretch",
            layer="below")])

    return fig


@app.callback(

    Output(component_id='series-POS', component_property='options'),
    Input(component_id='match-POS', component_property='value')
)
def update_menucurrPOS(value):
    # En fonction de la valeur sélectionnée dans le premier Dropdown,
    # vous pouvez définir les options du deuxième Dropdown ici.
    opt = {}
    match_data = df4[df4['MatchId'] == value]
    for i in match_data['current']:
        opt[i] = i

    return opt


@app.callback(

    Output(component_id='menu', component_property='options'),
    Input(component_id='match-KDA', component_property='value')
)
def update_menuPlayerKDA(value):
    # En fonction de la valeur sélectionnée dans le premier Dropdown,
    # vous pouvez définir les options du deuxième Dropdown ici.
    opt = {}

    Pdata = name[name['matchUrn'] == value]
    for i in Pdata['name']:
        opt[i] = i

    return opt


@app.callback(

    Output(component_id='series-KDA', component_property='options'),
    Input(component_id='match-KDA', component_property='value')
)
def update_menucurrkp(value):
    # En fonction de la valeur sélectionnée dans le premier Dropdown,
    # vous pouvez définir les options du deuxième Dropdown ici.
    opt = {}
    match_data = df4[df4['MatchId'] == value]
    for i in match_data['current']:
        opt[i] = i

    return opt


@app.callback(

    Output(component_id='team-KP', component_property='options'),
    Input(component_id='match-KP', component_property='value')
)
def update_menuteamKP(value):
    # En fonction de la valeur sélectionnée dans le premier Dropdown,
    # vous pouvez définir les options du deuxième Dropdown ici.

    opt = {}
    upd_teamKP = team[team['MatchId'] == value]

    opt[upd_teamKP['teamOne'].values[0]] = upd_teamKP['teamOne'].values[0]
    opt[upd_teamKP['teamTwo'].values[0]] = upd_teamKP['teamTwo'].values[0]

    return opt


@app.callback(

    Output(component_id='menuCurr-KP', component_property='options'),
    Input(component_id='match-KP', component_property='value')
)
def update_menucurrkp(value):
    # En fonction de la valeur sélectionnée dans le premier Dropdown,
    # vous pouvez définir les options du deuxième Dropdown ici.
    opt = {}
    match_data = df4[df4['MatchId'] == value]
    for i in match_data['current']:
        opt[i] = i

    return opt


@app.callback(

    Output(component_id='pie-KP', component_property='figure'),
    Input(component_id='match-KP', component_property='value'),
    Input(component_id='menuCurr-KP', component_property='value'),
    Input(component_id='team-KP', component_property='value')
)
def update_KP(matchId, CurrentGame, teamM):
    # En fonction de la valeur sélectionnée dans le premier Dropdown,
    # vous pouvez définir les options du deuxième Dropdown ici.

    title_ = "KP of '%s' players during '%s' series '%s' " % (teamM, matchD[matchId][0], CurrentGame)
    teamKp = df2[(df2['matchUrn'] == matchId) & (df2['current'] == CurrentGame) & (df2['team'] == teamM)]

    figure = px.pie(teamKp, values='KP', names='name', title=title_, width=800)
    return figure


@app.callback(

    Output(component_id='totalGold', component_property='figure'),
    Input(component_id='match', component_property='value'),
    Input(component_id='menuCurr', component_property='value')
)
def update_totalGold(matchId, CurrentGame):
    # En fonction de la valeur sélectionnée dans le premier Dropdown,
    # vous pouvez définir les options du deuxième Dropdown ici.
    match_data = df[(df['matchUrn'] == matchId) & (df['current'] == CurrentGame)]
    title = "Total gold of '%s' , series '%s' " % (matchD[matchId][0], CurrentGame)
    figure = px.histogram(match_data, x='name', y='totalGold', histfunc='max', color='totalGold', title=title)
    return figure


@callback(
    Output(component_id='nom', component_property='figure'),
    Input(component_id='menu', component_property='value'),
    Input(component_id='match-KDA', component_property='value'),
    Input(component_id='series-KDA', component_property='value'),
    Input(component_id='choice', component_property='value')
)
def update_graph(joueurUG, matchUG, currentUG, choixUG):
    player_dataAll = df3[df3['namePlayer'] == joueurUG]
    player_dataOne = df3[(df3['namePlayer'] == joueurUG) & (df3['matchUrn'] == matchUG) & (df3['current'] == currentUG)]

    # print(player_dataAll['namePlayer'])

    if (choixUG == "One Game"):

        scatter = px.scatter(player_dataOne, x='posx', y='posy', color="name", range_x=[0, 15000], range_y=[0, 15000])
    else:

        scatter = px.scatter(player_dataAll, x='posx', y='posy', color="name", range_x=[0, 15000], range_y=[0, 15000])

    scatter.update_traces(marker_size=20)

    scatter.update_layout(
        autosize=True,
        width=800,
        height=800,
        images=[dict(
            source='data:image/jpg;base64,{}'.format(polar_light.decode()),
            xref="paper", yref="paper",
            x=0, y=1,  # position of the upper left corner of the image in subplot 1,1
            sizex=1, sizey=1,  # sizex, sizey are set by trial and error
            xanchor="left",
            yanchor="top",
            # height="800",

            sizing="stretch",
            layer="below")])

    return scatter


@app.callback(

    Output(component_id='menuCurr', component_property='options'),
    Input(component_id='match', component_property='value')
)
def update_dropdown2(value):
    # En fonction de la valeur sélectionnée dans le premier Dropdown,
    # vous pouvez définir les options du deuxième Dropdown ici.

    opt = {}
    match_data = df4[df4['MatchId'] == value]
    for i in match_data['current']:
        opt[i] = i

    return opt


# Callback pour mettre à jour le contenu en fonction de l'URL
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-stat':
        return html.Div([
            html.H3('Les stats'),
            # Ajoutez ici le contenu de votre page "Stat"
        ])

    elif pathname == '/page-graphique':
        return html.Div([
            html.H3('Graphiques'),
            html.Div(className="bigG", children=[
                html.Div(className="bigG-block", children=[
                    html.Div(className="bigG-block-top", children=[

                        dcc.Graph(id="totalGold", figure=px.histogram(totalG, x='name', y='totalGold', histfunc='max',
                                                                      color='totalGold',
                                                                      title="Total gold of LNG vs T1 , series 1"))
                    ]),

                    html.Div(className="bigG-block-bot", children=[

                        dcc.Dropdown(
                            id='match',
                            options=matchD,
                            style={'width': "100%", 'color': "red", 'text-align': "center"},
                            value='esports:match:b3590072-d7dd-4d8c-b307-b671b3760075'),
                        dcc.Dropdown(
                            id='menuCurr',
                            options=opt,
                            style={'width': "100%", 'text-align': "center", 'color': "blue"},
                            value='1'),

                    ]),

                ]),

                html.Div(className="bigG-block", children=[

                    html.Div(className="bigG-block-top", children=[

                        html.Div(dcc.Graph(id="pie-KP", figure=pie))

                    ]),

                    html.Div(className="bigG-block-bot", children=[dcc.Dropdown(
                        id='match-KP',
                        options=matchD,
                        style={'width': "100%", 'display': "block", 'text-align': "center", 'color': "red"},
                        value="esports:match:b3590072-d7dd-4d8c-b307-b671b3760075"
                    ), dcc.Dropdown(
                        id='menuCurr-KP',
                        options={"e": "e"},
                        style={'width': "100%", 'display': "block", 'text-align': "center", 'color': "blue"},
                        value='1'
                    ), dcc.Dropdown(
                        id='team-KP',
                        options={"LNG": "LNG"},
                        style={'width': "100%", 'display': "block", 'text-align': "center", 'color': "blue"},
                        value='LNG'
                    )]),

                ])

            ])
            # Ajoutez ici le contenu de votre page "Graphique"
        ])
    elif pathname == '/page-map':
        return html.Div([
            html.H3('Carte'),
            html.Div(className="secondsection",
                     children=[html.Div(className="secondsection-a",
                                        children=[dcc.Graph(figure=scatter, id="nom")]),
                               html.Div(html.Div(className="secondsection-b",
                                                 children=[dcc.Dropdown(
                                                     id="match-KDA",
                                                     options=matchD,
                                                     style={'width': "100%", 'display': "block",
                                                            'text-align': "center", 'color': "red"},
                                                     value='esports:match:b3590072-d7dd-4d8c-b307-b671b3760075'
                                                 ),
                                                     dcc.Dropdown(
                                                         id='series-KDA',
                                                         options={"e": "e"},
                                                         style={'width': "100%", 'display': "block",
                                                                'text-align': "center", 'color': "red"},
                                                         value='1'),
                                                     dcc.Dropdown(
                                                         id='menu',
                                                         options=name_tmp,
                                                         style={'width': "100%", 'display': "block",
                                                                'text-align': "center", 'color': "red"},
                                                         value='T1 Zeus'),
                                                     dcc.Dropdown(
                                                         id='choice',
                                                         options=choice,
                                                         style={'width': "100%", 'display': "block",
                                                                'text-align': "center", 'color': "red"},
                                                         value='One Game'),

                                                 ])
                                        ), ]
                     ),

            html.Div(className="secondsection",
                     children=[html.Div(className="secondsection-a",
                                        children=[dcc.Graph(id="graph-pos", figure=scatter2),
                                                  html.Div(html.Div(className="secondsection-b",
                                                                    children=[
                                                                        dcc.Dropdown(
                                                                            id='match-POS',
                                                                            options=matchD,
                                                                            style={'width': "100%",
                                                                                   'display': "block",
                                                                                   'text-align': "center",
                                                                                   'color': "red"},
                                                                            value='esports:match:b3590072-d7dd-4d8c-b307-b671b3760075'
                                                                        ),
                                                                        dcc.Dropdown(
                                                                            id='series-POS',
                                                                            options={"e": "e"},
                                                                            style={'width': "100%",
                                                                                   'display': "block",
                                                                                   'text-align': "center",
                                                                                   'color': "red"},
                                                                            value='1'),
                                                                    ]))
                                                  ])
                               ]),

            html.Div(className="secondsection",
                     children=[html.Div(className="secondsection-a",
                                        children=[dcc.Graph(id="graph-BEG", figure=scatterOner),
                                                  html.Div(html.Div(className="secondsection-b",
                                                                    children=[
                                                                        dcc.Dropdown(
                                                                            id='match-POS',
                                                                            options=matchD,
                                                                            style={'width': "100%",
                                                                                   'display': "block",
                                                                                   'text-align': "center",
                                                                                   'color': "red"},
                                                                            value='esports:match:b3590072-d7dd-4d8c-b307-b671b3760075'
                                                                        ),
                                                                        dcc.Dropdown(
                                                                            id='menu',
                                                                            options=name_tmp,
                                                                            style={'width': "100%",
                                                                                   'display': "block",
                                                                                   'text-align': "center",
                                                                                   'color': "red"},
                                                                            value='T1 Zeus'),
                                                                    ]))
                                                  ])
                               ]),



        ])

    else:
        return html.Div([
            html.H3('Accueil'),
            # Ajoutez ici le contenu de votre page d'accueil par défaut
        ])


# Exécute l'applicationv
if __name__ == '__main__':
    load_figure_template('SLATE')
    app.run_server(debug=True)
