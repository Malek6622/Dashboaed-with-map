import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly 
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_bootstrap_components.themes
import dash_table as dt
import requests
import sys
import plotly.express as px
import base64
import flask

server = flask.Flask(__name__)

mapbox_access_token = open(".mapbox_token").read()


@server.route('/')
def index():
    return ''

app = dash.Dash(
    __name__,
    server=server,
    routes_pathname_prefix='/dash/'
)

image_filename = 'assets/logo.jpg'
logo = base64.b64encode(open(image_filename, 'rb').read())

image_filename = 'assets/image.png'
image = base64.b64encode(open(image_filename, 'rb').read())

BS = "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
a = [
{
    'href': 'https://use.fontawesome.com/releases/v5.8.1/css/all.css',
    'rel': 'stylesheet',
    'integrity': 'sha384-50oBUHEmvpQ+1lW4y57PTFmhCaXp0ML5d60M1M7uH2+nqUivzIebhndOJK28anvf',
    'crossorigin': 'anonymous'
}
]
app = dash.Dash(external_stylesheets=[BS,a])
#app = dash.Dash('project', external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True
app.title = 'project'

#the path of AllPermutationsExamples.csv
df1 = pd.read_csv("C:/Users/1692/Desktop/DashApp/AllPermutationsExamples.csv", delimiter=';', skiprows=0, low_memory=False)
#the path of ApprovedListingsGPS.csv
df2 = pd.read_csv("C:/Users/1692/Desktop/DashApp/ApprovedListingsGPS.csv", delimiter=';', skiprows=0, low_memory=False)
#splitting the column into 8 columns
df2[["Address", "City", "Zipcode","ListedPrice", "Lat", "Long"]]= df2["Address,City,Zipcode,Listed Price,Lat,Long"].str.split(",", 7, expand=True)
#deleting the first column
df2 = df2.drop(["Address,City,Zipcode,Listed Price,Lat,Long"], axis=1)
#splitting the column into 8 columns
df1[['Address','Purchase Price', 'Down Payment %', 'Mortgage Rate', 'Rent as % of Purchase Price', 'Rent', 'Cashflow assuming Calculated Expenses & Mortgage' , 'Cap Rate']]=df1["Address,Purchase Price,Down Payment %,Mortgage Rate,Rent as % of Purchase Price,Rent,Cashflow assuming Calculated Expenses & Mortgage ,Cap Rate"].str.split(",", 9, expand=True)
#deleting the first column
df1 = df1.drop(["Address,Purchase Price,Down Payment %,Mortgage Rate,Rent as % of Purchase Price,Rent,Cashflow assuming Calculated Expenses & Mortgage ,Cap Rate"],axis=1)
#generating the map
df2['ListedPrice']=pd.to_numeric(df2.ListedPrice)
fig = px.scatter_mapbox(
      df2, lat=pd.to_numeric(df2.Lat), 
      lon=pd.to_numeric(df2.Long), 
      color='ListedPrice', 
      color_continuous_scale=px.colors.diverging.BrBG,
      size_max=15, 
      zoom=10, 
      size=pd.to_numeric(df2.ListedPrice)
      )
fig.update_layout(
      mapbox_style='carto-positron',
      height=550, )
#the layout of the map
app.layout = html.Div([

      dbc.Row(
      html.Div([
      dbc.Col(
      html.Div(children=[
      html.Div(children=[
      #the logo displayed on the left
      html.Img(src='data:image/png;base64,{}'.format(logo.decode()))],style={'width': '8%','height': '10%','display': 'inline-block', 'float':'left','paddingLeft':0,'paddingRight':0},className='one column'),
      html.Div(children=[
      #the logo displayed on the right
      html.Img(src='data:image/png;base64,{}'.format(logo.decode()))],style={'width': '9%','height': '10%','display': 'inline-block', 'float':'right','paddingLeft':'2%','paddingRight':0},className='one column'),
      ])),
      dbc.Row(
      html.Div(children=[
      html.Div(children=[
      html.Div(children=[
      #Top of page
      html.H1("Top of Page")],style={'width':'100%','height':80,'display': 'inline-block', 'text-align':'center','float':'left','backgroundColor':'#DEB887','color':'#FFFFFF','marginLeft':0,'marginRight':0},className='ten columns'),
      ],style={'width':'100%','display': 'inline-block', 'float':'left','marginLeft':0,'marginRight':0},className='row' ),
      #The buttons
      dbc.ButtonGroup(children =[
      html.A(dbc.Button("Help/How to use link", id='btn-nclicks-1', n_clicks=0, size='md'),href='https://github.com/czbiohub/singlecell-dash/issues/new'),
      html.A(dbc.Button("Link Box of some kind ", id='btn-nclicks-2', n_clicks=0, size='md'),href='https://github.com/czbiohub/singlecell-dash/issues/new'),
      dbc.Button("ApprovedListingsGPS", id='btn-nclicks-3', n_clicks=0, size='md'),
      dbc.Button("AllPermutationsExamples", id='btn-nclicks-4', n_clicks=0, size='md'),
      ],style={'width':'101%','paddingLeft':0,'paddingRight':15, 'float':'right'},className='row'),
      ],style={'width':'100%','display': 'inline-block','marginLeft':0,'marginRight':0})),      
      ],style={'width': '100%', 'marginRight':0, 'marginRight': 0 ,'max-width':50000},className='container')),
      #Displaying the map
      html.Div(children=[
      dcc.Graph(id ='mapbox', figure=fig),
      ]),
      #Displaying the tables
      html.Div(id='tab'),

      dbc.Row(
      html.Div(children=[
      #Your conacts
      dbc.Col(
      html.Div(children=[
      html.Div(children=[
      html.H1("Contact")
      ],style={'text-align':'left','color':'#FFFFFF','width':'90%'},className='ten columns'),
      html.Div(children=[
      html.H6("Name: -------")
      ],style={'text-align':'left','color':'#FFFFFF','width':'90%'},className='ten columns'),
      html.Div(children=[
      html.H6("e-mail: something@gmail.com")
      ],style={'text-align':'left','color':'#FFFFFF','width':'90%'},className='ten columns'),
      html.Div(children=[
      html.H6("Phone Number: 848787441")
      ],style={'text-align':'left','color':'#FFFFFF','width':'90%'},className='ten columns'),
      html.Div(children=[
      html.H6("Address: --------")
      ],style={'text-align':'left','color':'#FFFFFF','width':'90%'},className='ten columns')
      ],style={'display': 'inline-block', 'float':'left','width':'90%'})),
      #Your personal image
      dbc.Col(
      html.Div(children=[
      html.Img(src='data:image/png;base64,{}'.format(image.decode()))
      ],style={'width': '10%','height': '10%','display': 'inline-block', 'float':'right','paddingLeft':0,'paddingRight':0},className='two column')),
      
      ],style={'width':'100%','height':180,'max-width':50000,'backgroundColor':'#DEB887'},className='container')),
      

      ])
 
@app.callback(Output('tab', 'children'),
              [Input('btn-nclicks-3', 'n_clicks'),
               Input('btn-nclicks-4', 'n_clicks'),
               Input('mapbox', 'clickData')
              ])
def displayClick(btn1, btn2,n):
  changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
  ctx = dash.callback_context
  if 'btn-nclicks-3' in changed_id:
    tab2 = df2.drop(['Lat','Long'],axis=1)
    data2 = tab2.to_dict('rows')
    columns2 =  [{"name": i, "id": i,} for i in (tab2.columns)]
    return html.Div(children=[ 
    dt.DataTable(data=data2, columns=columns2,page_size=10,
    style_cell={'textAlign': 'left','padding': '10px','marginLeft':'50xp','font_family': 'Sans-Serif',
    'font_size': '15px'}
    , style_as_list_view=True,
    filter_action='native',
    style_header={
    'backgroundColor': '#DEB887',
    'font_family': 'Sans-Serif',
    'font_size': '15px',
    'color':'#FFFFFF',
    'fontWeight': 'bold'},
    style_data_conditional=[
    {
    'if': {'row_index': 'odd'},
    'backgroundColor': 'rgb(248, 248, 248)'
    }
    ])],style={'width':'90%','marginRight':'5%','marginLeft':'5%','marginBottom':80}),

  elif 'btn-nclicks-4' in changed_id:
    data1 = df1.to_dict('rows')
    columns1 =  [{"name": i, "id": i,} for i in (df1.columns)]
    return html.Div(children=[ 
    dt.DataTable(data=data1, columns=columns1,page_size=10,
    style_cell={'textAlign': 'left','padding': '10px','marginLeft':'50xp','font_family': 'Sans-Serif',
    'font_size': '15px'}
    , style_as_list_view=True,
    filter_action='native',
    style_header={
    'backgroundColor': '#DEB887',
    'font_family': 'Sans-Serif',
    'font_size': '15px',
    'color':'#FFFFFF',
    'fontWeight': 'bold'},
    style_data_conditional=[
    {
    'if': {'row_index': 'odd'},
    'backgroundColor': 'rgb(248, 248, 248)'
    }
    ])],style={'width':'90%','marginRight':'5%','marginLeft':'5%','marginBottom':80}),

  elif n != None:
    a = pd.to_numeric(n.get('points')[0].get('lat'))
    df = df2[pd.to_numeric(df2['Lat'])==pd.to_numeric(a)]
    df0 = pd.merge(df, df1, on='Address')
    df0 = df0.drop(["City",'Zipcode','ListedPrice','Lat','Long'],axis=1)
    data = df.to_dict('rows')
    columns =  [{"name": i, "id": i,} for i in (df.columns)]
    data0 = df0.to_dict('rows')
    columns0 =  [{"name": i, "id": i,} for i in (df0.columns)]
    return( 
    html.Div(children=[ 
    dt.DataTable(data=data0, columns=columns0,page_size=10,
      style_cell={'textAlign': 'left','padding': '10px','marginLeft':'50xp','font_family': 'Sans-Serif',
      'font_size': '15px'}
      , style_as_list_view=True,
      filter_action='native',
      style_header={
      'backgroundColor': '#DEB887',
      'font_family': 'Sans-Serif',
      'font_size': '15px',
      'color':'#FFFFFF',
      'fontWeight': 'bold'},
      style_data_conditional=[
      {
      'if': {'row_index': 'odd'},
      'backgroundColor': 'rgb(248, 248, 248)'
      }
      ])],style={'width':'90%','marginRight':'5%','marginLeft':'5%','marginBottom':80},className='Row'),
)
  else :
    tab2 = df2.drop(['Lat','Long'],axis=1)
    data2 = tab2.to_dict('rows')
    columns2 =  [{"name": i, "id": i,} for i in (tab2.columns)]
    return html.Div(children=[ 
    dt.DataTable(data=data2, columns=columns2,page_size=10,
      style_cell={'textAlign': 'left','padding': '10px','marginLeft':'50xp','font_family': 'Sans-Serif',
      'font_size': '15px'}
      , style_as_list_view=True,
      filter_action='native',
      style_header={
      'backgroundColor': '#DEB887',
      'font_family': 'Sans-Serif',
      'font_size': '15px',
      'color':'#FFFFFF',
      'fontWeight': 'bold'},
      style_data_conditional=[
      {
      'if': {'row_index': 'odd'},
      'backgroundColor': 'rgb(248, 248, 248)'
      }
      ])],style={'width':'90%','marginRight':'5%','marginLeft':'5%','marginBottom':80},className='Row'),
    

if __name__ == '__main__':
    app.run_server(debug=True)
