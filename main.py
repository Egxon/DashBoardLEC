from dash import *
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import connect_bd
import figure
import request
############################################################






##############################################################

# Initialisation de l'application Dash
app = Dash(external_stylesheets=[dbc.themes.SLATE], suppress_callback_exceptions=False)
cur = connect_bd.getBD()
conn = connect_bd.getConBD()


# Get All Datas et DF
name = request.getName()
team = request.getTeam()
Stats = request.getStats()
KP = request.getKP()
Position_courante = request.getCurrentPosOfAction()
Match_courant = request.getMatchAndCurrent()
name_tmp = request.getNameTmp()
match = request.getMatch()

totalG = Stats[(Stats['matchUrn'] == "esports:match:b3590072-d7dd-4d8c-b307-b671b3760075") & (Stats['current'] == "1")]
pie = px.pie(KP, values='KP', names='name', title="KP", width=800)
player_data = Position_courante[Position_courante['namePlayer'] == "T1 Zeus"]
match_data = Match_courant[Match_courant['MatchId'] == "esports:match:b3590072-d7dd-4d8c-b307-b671b3760075"]

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

)
def update_BEG(player):
    return figure.getVideoCrossingEarly(player)


@app.callback(

    Output(component_id='graph-pos', component_property='figure'),
    Input(component_id='match-POS', component_property='value'),
    Input(component_id='series-POS', component_property='value'),

)
def update_POS(matchIdPos, currIdPos):
    return figure.getVideoCrossing(matchIdPos,currIdPos)



@app.callback(

    Output(component_id='series-POS', component_property='options'),
    Input(component_id='match-POS', component_property='value')
)
def update_menucurrPOS(value):
    opt = {}
    match_data = Match_courant[Match_courant['MatchId'] == value]
    for i in match_data['current']:
        opt[i] = i

    return opt


@app.callback(

    Output(component_id='player-KDA', component_property='options'),
    Input(component_id='match-KDA', component_property='value')
)
def update_menuPlayerKDA(value):
    # En fonction de la valeur sélectionnée dans le premier Dropdown,
    # vous pouvez définir les options du deuxième Dropdown ici.
    opt = {}
    Pdata = name[name['matchUrn'] == value]
    for i in Pdata['name']:
        print(i)
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
    match_data = Match_courant[Match_courant['MatchId'] == value]
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
    match_data = Match_courant[Match_courant['MatchId'] == value]
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
    teamKp = KP[(KP['matchUrn'] == matchId) & (KP['current'] == CurrentGame) & (KP['team'] == teamM)]
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
    match_data = Stats[(Stats['matchUrn'] == matchId) & (Stats['current'] == CurrentGame)]
    title = "Total gold of '%s' , series '%s' " % (matchD[matchId][0], CurrentGame)
    figure = px.histogram(match_data, x='name', y='totalGold', histfunc='max', color='totalGold', title=title)
    return figure


@callback(
    Output(component_id='nom', component_property='figure'),
    Input(component_id='player-KDA', component_property='value'),
    Input(component_id='match-KDA', component_property='value'),
    Input(component_id='series-KDA', component_property='value'),
    Input(component_id='choice', component_property='value')
)
def update_graph(joueurUG, matchUG, currentUG, choixUG):
    print(joueurUG, " - ", matchUG, " - ",currentUG , " - ", choixUG)
    return figure.getActionFromPlayer(joueurUG,matchUG,currentUG,choixUG)



@app.callback(

    Output(component_id='menuCurr', component_property='options'),
    Input(component_id='match', component_property='value')
)
def update_dropdown2(value):
    # En fonction de la valeur sélectionnée dans le premier Dropdown,
    # vous pouvez définir les options du deuxième Dropdown ici.

    opt = {}
    match_data = Match_courant[Match_courant['MatchId'] == value]
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
        print(i)
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
                                        children=[dcc.Graph(figure=figure.getActionFromPlayer(), id="nom")]),
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
                                                         id='player-KDA',
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
                                        children=[dcc.Graph(id="graph-pos", figure=figure.getVideoCrossing()),
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
                                        children=[dcc.Graph(id="graph-BEG", figure=figure.getVideoCrossingEarly()),
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
