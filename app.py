import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Instantiation of the app
app = dash.Dash(__name__)

# calculations(tuple/array, array of tuples/arrays)
# Inputing the dimensions and corners this function returns an array of rows of points
def calculations(dimensions, corners):

    # pulling the x's and y's of the corners as well as setting the row and column amounts
    columns = dimensions[1]
    rows = dimensions[0]
    x_in = []
    x_in.extend([corners[0][0], corners[1][0], corners[2][0], corners[3][0]])
    y_in = []
    y_in.extend([corners[0][1], corners[1][1], corners[2][1], corners[3][1]])

    #cfinding the minimum and maximum x and y of the corners 
    x_max = max(x_in)
    x_min = min(x_in)
    y_max = max(y_in)
    y_min = min(y_in)
    
    # calculating the jumps between the x and y values 
    x_jump = (x_max - x_min) / (columns-1)
    y_jump = (y_max - y_min) / (rows-1)

    x_out = []
    y_out = []

    # creating an array of all the new x values 
    # this is done by adding the jump value to the x's until I reach the x max value
    curr_x = x_min
    while len(x_out) < columns:
        x_out.append(curr_x)
        curr_x = curr_x + x_jump

    # creating an array of all the new y values 
    # this is done by adding the jump value to the y's until I reach the y max value
    curr_y = y_min
    while len(y_out) < rows:
        y_out.append(curr_y)
        curr_y = curr_y + y_jump
    
    # creation of rows and output array
    # I create points by looping through each x and y variation, then add them to rows
    # according to similar x values, the rows are then made into an output array. 
    row= []
    out = []
    for x in x_out:
        for y in y_out:
            row.append([x, y])
        out.append(row)
        row = []
    return out 

#This is the layer of HTML elements
app.layout = html.Div(children=[
    html.H1(children='Fetch Rewards Coding Assessment MLE ', style={'text-align': 'center'}),

    html.Div([
            html.Label(['Insert the following inputs:'],style={'font-weight': 'bold'}),
            html.Br(), html.Br(),
            html.Label(['Dimensions: '],style={'font-weight': 'bold'}),
            dcc.Input(id="dimensions", type="text", placeholder="(rows, columns)", debounce=True),
            html.Br(),
            html.Label(['Corners: '],style={'font-weight': 'bold'}),
            dcc.Input(id="corner1", type="text", placeholder="(x, y)", debounce=True),
            dcc.Input(id="corner2", type="text", placeholder="(x, y)", debounce=True),
            dcc.Input(id="corner3", type="text", placeholder="(x, y)", debounce=True),
            dcc.Input(id="corner4", type="text", placeholder="(x, y)", debounce=True),
            html.Button('Submit', id='button'),

            html.Div(dcc.Graph(id='out')),
        ])        
])

@app.callback(
    Output("out", "figure"),
    Input("dimensions", "value"),
    Input("corner1", "value"),
    Input("corner2", "value"),
    Input("corner3", "value"),
    Input("corner4", "value"),
    Input('button', 'n_clicks')
)
# update_plot(string, string, string, string, string)
# update_plot takes in strings of tuples/arrays (and button pressed) turns them into actual tuples and arrays
# if the tuples and arrays pass the error checking it runs through the calculation function
def update_plot(dimensions, corner1, corner2, corner3, corner4, n):
    #Making sure the function only runs when the button is pressed 
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if ('button' in changed_id) and (dimensions and corner1 and corner2 and corner3 and corner4) != None:
        # turns the dimension string into an int tuple 
        dim = tuple(map(int, dimensions.strip(')(').split(',')))
        columns = dim[1]
        rows = dim[0]
        # checks to make sure the dimensions work 
        if (rows and columns) < 2:
            print("Your dimensions will not work")
            fig = px.scatter(title = "Incomplete data or incorrect format")
            return fig
        # turns the corners into tuples then adds it to an array
        corners  = []
        c1 = tuple(map(int, corner1.strip(') (').split(',')))
        c2 = tuple(map(int, corner2.strip(') (').split(',')))
        c3 = tuple(map(int, corner3.strip(') (').split(',')))
        c4 = tuple(map(int, corner4.strip(') (').split(',')))
        corners.extend([c1, c2, c3, c4])
        # checks the dimensions are correct
        if len(dim) != 2:
            print("Your dimensions are not correct")
            fig = px.scatter(title = "Incomplete data or incorrect format")
            return fig
        # checks the corners are correct 
        if len(corners) != 4:
            print("Your corners are not correct ")
            fig = px.scatter(title = "Incomplete data or incorrect format")
            return fig
        
        # runs the calculation function to receive the array or rows and points for plotting
        coordinates = calculations(dim, corners)
        # creation of a dataframe for plotting using plotly 
        df = pd.DataFrame()
        for row in coordinates:
            df = df.append(row)
        df.columns = ['X', 'Y']
        fig = px.scatter(df, x='X', y='Y')
        fig.update_traces(marker=dict(size=15))
        return fig
    else:
        fig = px.scatter(title = "Incomplete data or incorrect format")
        return fig

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port = '8050')
