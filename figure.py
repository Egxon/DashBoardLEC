import graph_position
import request
import base64
import plotly.express as px

#Image de la manimap
image1_filename = 'images/Minimap.jpg'
polar_light = base64.b64encode(open(image1_filename, 'rb').read())

def getVideoCrossing(match = None, current = None):
    print("jsuui dans la fonc")
    if match==None and current == None:
        scatter2 = px.scatter(graph_position.getCurrentPos(), x='posx', y='posy', color="name", animation_frame="gameTime", range_x=[0, 15000],range_y=[0, 15000])
    else:
        scatter2 = px.scatter(graph_position.getCurrentPos(match,current), x='posx', y='posy', color="name",animation_frame="gameTime", range_x=[0, 15000], range_y=[0, 15000])

    print("jsuui dans la ")
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
            sizing="stretch",
            layer="below")])

    print("c cesé return ")
    return scatter2

def getVideoCrossingEarly(player = None):
    if player == None:
        fig = px.scatter(graph_position.getMoveEarly(), x='posx', y='posy', color='current', animation_frame="gameTime", range_x=[0, 15000],range_y=[0, 15000])
    else:
        fig = px.scatter(graph_position.getMoveEarly(player), x='posx', y='posy', color='current', animation_frame="gameTime", range_x=[0, 15000],
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


def getActionFromPlayer(joueurUG=None, matchUG=None, currentUG=None, choixUG=None):
    Position_courante = request.getCurrentPosOfAction()

    if (joueurUG == None and matchUG == None and currentUG == None and choixUG == None):
        player_dataAll = Position_courante[Position_courante['namePlayer'] == 'T1 Faker']
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

    else:
        print(choixUG)
        if (choixUG == "One Game") :

            player_dataOne = Position_courante[(Position_courante['namePlayer'] == joueurUG) & (Position_courante['matchUrn'] == matchUG) & (Position_courante['current'] == currentUG)]
            scatter = px.scatter(player_dataOne, x='posx', y='posy', color="name", range_x=[0, 15000], range_y=[0, 15000], title=joueurUG)
        else :
            print("je dois exit normalment")

            player_dataAll = Position_courante[(Position_courante['namePlayer'] == joueurUG) & (Position_courante['matchUrn'] == matchUG)]
            scatter = px.scatter(player_dataAll, x='posx', y='posy', color="name", range_x=[0, 15000], range_y=[0, 15000], title=joueurUG)
            print("TA MERE")

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


