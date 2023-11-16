
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html
import plotly.graph_objects as go
from plotly.validators.scatter.marker import SymbolValidator
x = [1,1,1]
y = [2,1,2]

x2 = [2, 1.2,]
y2 = [1, 1 ]

# Création du scatter plot
figW = px.scatter(x=x, y=y,animation_frame=[1,2,3])
figW.update_traces(marker_size=15)





figW2 = px.scatter(x=x2, y=y2,animation_frame=[1,2])



fig3 = go.Figure(
    data=figW.data + figW2.data,
    frames=[
        go.Frame(data=fr1.data + fr2.data, name=fr1.name)
        for fr1, fr2 in zip(figW.frames, figW2.frames)
    ],
    layout=figW.layout,
)


app = Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig3),
dcc.Graph(figure=figW),dcc.Graph(figure=figW2),

])

app.run_server(debug=True, use_reloader=False)  # Turn off reloader if inside Jupyter