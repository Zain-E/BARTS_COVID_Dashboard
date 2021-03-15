
#================================================= IMPORT LIBRARIES ====================================================

import pandas as pd
import plotly.express as px
import boto3
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash
import base64
from dash.dependencies import Input,Output,State
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import io
import xlrd

#================================================= AWS S3 CONNECTION ===================================================

access_key_ID ='AKIAXSF52DIAIYVY3EOU'
secret_access_key ='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'
bucket_name = 'zainprojects'
upload_file_key = 'COVID_Analysis/Excel_Documents/'



s3 = boto3.client('s3', aws_access_key_id=access_key_ID, aws_secret_access_key=secret_access_key)


#Reads the files in the S3 repo so we can use as a df
#Table 1
obj = s3.get_object(Bucket=bucket_name, Key=f'{upload_file_key}Table1.xlsx')
data = obj['Body'].read()
table1 = pd.read_excel(io.BytesIO(data))

#Table 2C
obj = s3.get_object(Bucket=bucket_name, Key=f'{upload_file_key}Table2C.xlsx')
data = obj['Body'].read()
table2C = pd.read_excel(io.BytesIO(data))

#Table 3
obj = s3.get_object(Bucket=bucket_name, Key=f'{upload_file_key}Table3.xlsx')
data = obj['Body'].read()
table3 = pd.read_excel(io.BytesIO(data))

#Deprivation
obj = s3.get_object(Bucket=bucket_name, Key=f'{upload_file_key}Deprivation_Index.xlsx')
data = obj['Body'].read()
Deprivation_Index = pd.read_excel(io.BytesIO(data))

#Ethnicity
obj = s3.get_object(Bucket=bucket_name, Key=f'{upload_file_key}Ethnic_Proportion.xlsx')
data = obj['Body'].read()
Ethnicity = pd.read_excel(io.BytesIO(data))

#Location
obj = s3.get_object(Bucket=bucket_name, Key=f'{upload_file_key}Location.xlsx')
data = obj['Body'].read()
Location = pd.read_excel(io.BytesIO(data))

#Table
obj = s3.get_object(Bucket=bucket_name, Key=f'{upload_file_key}Table.xlsx')
data = obj['Body'].read()
Table = pd.read_excel(io.BytesIO(data))

#=============================================== DATA MANIPULATION =====================================================


#First tab Filter
region_list = table1['Area of usual residence name'].unique()
print(region_list)

#Shorten names of Boroughs

short_hand =   {'Barking and Dagenham': 'Barking',
                'Richmond upon Thames': 'Richmond',
                'Kensington and Chelsea':'Kensington',
                'Hammersmith and Fulham':'Hammersmith',
                'Inner London':'Inner London',
                'Camden':'Camden',
                'City of London':'City of London',
                'Hackney':'Hackney',
                'Haringey':'Haringey',
                'Islington':'Islington',
                'Lambeth':'Lambeth',
                'Lewisham':'Lewisham',
                'Newham':'Newham',
                'Southwark':'Southwark',
                'Tower Hamlets':'Tower Hamlets',
                'Wandsworth':'Wandsworth',
                'Westminster':'Westminster',
                'Outer London':'Outer London',
                'Barnet':'Barnet',
                'Bexley':'Bexley',
                'Brent':'Brent',
                'Bromley':'Bromley',
                'Croydon':'Croydon',
                'Ealing':'Ealing',
                'Enfield':'Enfield',
                'Greenwich':'Greenwich',
                'Harrow':'Harrow',
                'Havering':'Havering',
                'Hillingdon':'Hillingdon',
                'Hounslow':'Hounslow',
                'Merton':'Merton',
                'Redbridge':'Redbridge',
                'Sutton':'Sutton',
                'Waltham Forest':'Waltham Forest',
                }

#================================================ DASHBOARD LAYOUT =====================================================


app = dash.Dash(__name__, eager_loading=True, external_stylesheets=[dbc.themes.LUX])
server = app.server
image_filename = r'Barts_logo.png' # replace with your own image - must be png image type - use this website to convert :https://jpg2png.com/
encoded_image = base64.b64encode(open(image_filename, 'rb').read())
image_filename = r'GitHub.png' # replace with your own image - must be png image type - use this website to convert :https://jpg2png.com/
encoded_image_Git = base64.b64encode(open(image_filename, 'rb').read())
image_filename_ONS = r'ONS.png' # replace with your own image - must be png image type - use this website to convert :https://jpg2png.com/
encoded_image_ONS = base64.b64encode(open(image_filename_ONS, 'rb').read())

app.layout = html.Div([
                        dbc.Row([dbc.Col(html.H1('COVID-19 Activity Dashboard',className='dark'),style={'text-align': 'center','vertical-align':'middle'}),
                                dbc.Col(html.A(href='https://www.bartshealth.nhs.uk/', children=html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), width=100, height=60, style={'vertical-align':'middle'}),target="_blank"), width=1),
                                ]),

                        html.Hr(),

                       dcc.Tabs(id="tabs", value='region-tab', children=[

                                # TAB 1 - REGION
                                dcc.Tab(label='Region', value='region-tab', children=[html.Div([

                                    html.Hr(),

                                    dbc.Row([dbc.Col(dcc.Dropdown(id='region_dropdown',
                                                                  options=[
                                                                      {"label": region_list[0],
                                                                       "value": region_list[0]},
                                                                      {"label": region_list[1],
                                                                       "value": region_list[1]},
                                                                      {"label": region_list[2],
                                                                       "value": region_list[2]},
                                                                      {"label": region_list[3],
                                                                       "value": region_list[3]},
                                                                      {"label": region_list[4],
                                                                       "value": region_list[4]},
                                                                      {"label": region_list[5],
                                                                       "value": region_list[5]},
                                                                      {"label": region_list[6],
                                                                       "value": region_list[6]},
                                                                      {"label": region_list[7],
                                                                       "value": region_list[7]},
                                                                      {"label": region_list[8],
                                                                       "value": region_list[8]},

                                                                  ],
                                                                  multi=True,
                                                                  value=[region_list[0],
                                                                         region_list[1],
                                                                         region_list[2],
                                                                         region_list[3],
                                                                         region_list[4],
                                                                         region_list[5],
                                                                         region_list[6],
                                                                         region_list[7],
                                                                         region_list[8]
                                                                         ],
                                                                  style={'text-align': 'center'},
                                                                  clearable=False,
                                                                  placeholder='Please select region'
                                                                  ), width={'size': 10, 'offset': 1}),

                                             ]),

                                    html.Hr(),

                                    dbc.Row(
                                        dbc.Col(html.H2('Deaths by Region', style={'text-align': 'center'}))),

                                    html.Br(),

                                    dbc.Row([dbc.Col(dcc.Graph(id='Graph 0', figure={}), width={'size': 10, 'offset': 1})]),

                                    html.Hr(),

                                    html.Br(),
                                    html.Br(),
                                    html.Br(),
                                    html.Br(),
                                    html.Br(),
                                    html.Br(),

                                    dbc.Row(
                                        [dbc.Col(html.H2('Deaths by Gender', style={'text-align': 'center'}), width={'size': 5, 'offset': 1}),
                                         dbc.Col(html.H2('Deaths VS Population', style={'text-align': 'center'}), width={'size': 5, 'offset': -1})]),

                                    dbc.Row([dbc.Col(dcc.Graph(id='Graph 1', figure={}), width={'size': 5, 'offset': 1}),
                                             dbc.Col(dcc.Graph(id='Graph 2', figure={}), width={'size': 5, 'offset': -1})
                                             ]),

                                    html.Hr(),
                                    html.Br(),
                                    html.Br(),

                                    dbc.Row([dbc.Col(html.H1(id='Card',style={'text-align': 'center', 'fontColor':'red'}, className="card-text"),width={'size': 10, 'offset': 1})
                                             ]),

                                    html.Br(),

                                    dbc.Row(dbc.Col(html.H5(
                                        'COVID-19 has had a significant effect on the population.  it can be observed from the regional graph that london in particular has exceptionally high deaths in comparion to its population size.  This needs further investigation into exactly where these deaths are occuring',
                                        style={'text-align': 'center'}), width={'size': 10, 'offset': 1})),

                                    html.Br(),
                                    html.Hr(),

                                ])]),


                                # TAB 2 - BOROUGH
                                dcc.Tab(label='Borough', value='borough-tab', children=[
                                    html.Div([

                                    html.Hr(),

                                    html.Br(),

                                    dbc.Row(dbc.Col(html.H2('Deaths by Deprivation',style={'text-align': 'center'}))),

                                    html.Br(),

                                    dbc.Row(dbc.Col(dcc.Graph(id='Graph 4', figure={}),width={'size': 8, 'offset': 2})),

                                    html.Hr(),
                                    html.Br(),

                                    dbc.Row(dbc.Col(html.H5(
                                            'Deprivation rates are scored from 1(most deprived) to 10(least deprived)',
                                            style={'text-align': 'center'}), width={'size': 10, 'offset': 1})),

                                    html.Br(),
                                    html.Hr(),

                                    html.Br(),
                                    html.Br(),
                                    html.Br(),

                                    dbc.Row(dbc.Col(html.H2('Deprivation VS Death Rate', style={'text-align': 'center'}))),

                                    dbc.Row(dbc.Col(dcc.Graph(id='Graph 3', figure={}), width={'size': 10, 'offset': 1})),

                                    html.Hr(),
                                    html.Br(),

                                    dbc.Row(dbc.Col(html.H5('The graphs above show the number of deaths by Borough.  In addition to this it can be seen that there is a strong relationship between deprivation rate and number of deaths.',style={'text-align': 'center'}),width={'size': 10, 'offset': 1})),

                                    html.Br(),

                                    dbc.Row(dbc.Col(html.H5('What is the relationship between deprivation, boroughs in london and deaths due to COVID-19?',style={'text-align': 'center'}),width={'size': 10, 'offset': 1})),

                                    html.Br(),
                                    html.Hr(),

                                    html.Br(),

                                    dbc.Row([dbc.Col(dcc.Graph(id='Map', figure={}),width={'size': 10, 'offset': 1})]),

                                    html.Br(),
                                    html.Hr(),

                                ])]),

                                # TAB 3 - DEPRIVATION
                                dcc.Tab(label='Deprivation', value='dep-tab',children=[

                                    html.Hr(),

                                    dbc.Row(dbc.Col(html.H2('Overall VS Health Deprivation', style={'text-align': 'center'}),width={'size': 10, 'offset': 1})),
                                    html.Br(),

                                    dbc.Row(dbc.Col(dcc.Graph(id='Graph 5', figure={}), width={'size': 10, 'offset': 1})),

                                    html.Hr(),
                                    html.Br(),

                                    dbc.Row(dbc.Col(html.H5(
                                        'The Health deprivation score is particularly important - therefore it has been compared to the overall score to determine if there are any anomalies/relationships',
                                        style={'text-align': 'center'}), width={'size': 10, 'offset': 1})),

                                    html.Br(),
                                    html.Hr(),

                                    html.Br(),
                                    html.Br(),
                                    html.Br(),

                                    dbc.Row(dbc.Col(html.H2('Ethnicity by borough', style={'text-align': 'center'}),width={'size': 10, 'offset': 1})),

                                    html.Br(),

                                    dbc.Row(dbc.Col(dcc.Graph(id='Graph 6', figure={}), width={'size': 10, 'offset': 1})),

                                    html.Br(),
                                    html.Br(),
                                    html.Br(),

                                    dbc.Row(dbc.Col(html.H2('Borough details', style={'text-align': 'center'}),width={'size': 10, 'offset': 1})),

                                    dbc.Row(
                                        [dbc.Col(html.Div(id='Table'), width={'size': 10, 'offset': 1})
                                         ]),

                                    html.Br(),
                                    html.Hr(),
                                    html.Br(),

                                    dbc.Row(dbc.Col(html.H5(
                                        'The table above has compared the death rate, deprivation score and BAME % by borough.  It is clear that boroughs that tend towards a higher BAME population are generally more deprived - and as a result have higher COVID-19 deaths amongst its population',
                                        style={'text-align': 'center'}), width={'size': 10, 'offset': 1})),

                                    html.Br(),
                                    html.Hr(),

                                    html.Br(),
                                    html.Br(),

                                    dbc.Row([dbc.Col(dcc.Graph(id='Graph 7', figure={}), width={'size': 10, 'offset': 1})
                                                                             ]),

                                    html.Br(),
                                    html.Br(),

                                    # dbc.Row([
                                    #          dbc.Col(html.A(href='https://github.com/Zain-E/BARTS_COVID_Dashboard', children=html.Img(src='data:image/png;base64,{}'.format(encoded_image_Git.decode()), width=60, height=60, style={'vertical-align':'middle'}),target="_blank"), width={'size': 1, 'offset': -1}),
                                    #          dbc.Col(html.A(href='https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/deathsduetocovid19bylocalareaanddeprivation', children=html.Img(src='data:image/png;base64,{}'.format(encoded_image_ONS.decode()), width=60, height=60, style={'vertical-align':'middle'}),target="_blank"), width={'size': 1, 'offset': -2})
                                    #     ]),


                                ]),

                               # TAB 4 - RECOMMENDATIONS
                                dcc.Tab(label='Recommendations', value='rec-tab', children=[

                                   html.Hr(),

                                   dbc.Row(dbc.Col(html.H2('Recommendations', style={'text-align': 'center'}),
                                                   width={'size': 10, 'offset': 1})),
                                   html.Br(),
                                   html.Br(),

                                   dbc.Row(dbc.Col(html.H5(
                                       '• Use our internal data to validate the ONS figures',
                                       style={'text-align': 'left'}), width={'size': 10, 'offset': 1})),

                                   html.Br(),

                                   dbc.Row(dbc.Col(html.H5(
                                        '• Inform strategy for the medium to long term for BARTS in a "post-COVID" world',
                                        style={'text-align': 'left'}), width={'size': 10, 'offset': 1})),

                                   html.Br(),

                                   dbc.Row(dbc.Col(html.H5(
                                        '• Data can be used to justify which programmes need focussing for improved performance and clinical outcomes',
                                        style={'text-align': 'left'}), width={'size': 10, 'offset': 1})),

                                   html.Br(),

                                   dbc.Row(dbc.Col(html.H5(
                                       '• Encourage the finance/contract teams to use this dashboard to form a business case for competitive bids',
                                       style={'text-align': 'left'}), width={'size': 10, 'offset': 1})),

                                   html.Br(),
                                   html.Hr(),

                                   dbc.Row([
                                        dbc.Col(html.A(href='https://github.com/Zain-E/BARTS_COVID_Dashboard',
                                                       children=html.Img(src='data:image/png;base64,{}'.format(
                                                           encoded_image_Git.decode()), width=60, height=60,
                                                                         style={'vertical-align': 'middle'}),
                                                       target="_blank"), width={'size': 1, 'offset': -1}),
                                        dbc.Col(html.A(
                                            href='https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/deathsduetocovid19bylocalareaanddeprivation',
                                            children=html.Img(
                                                src='data:image/png;base64,{}'.format(encoded_image_ONS.decode()),
                                                width=60, height=60, style={'vertical-align': 'middle'}),
                                            target="_blank"), width={'size': 1, 'offset': -2})
                                   ]),

                                ]),
                        ])

])
#============================================= GRAPH 0 =================================================================

@app.callback([Output('Graph 0', 'figure'),
              Output('Card', 'children')],

              Input(component_id='region_dropdown', component_property='value')
              )

def render_content(region):

    df = table1.copy()
    df = df[df['Sex']=='People']
    df = df[df['Underlying cause of death']=='Due to COVID-19']
    df = df[df['Area of usual residence name'].isin(region)]
    dfg = df.groupby(['Month'], as_index=False)['Deaths'].sum()

    dfa = table1.copy()
    dfa = dfa[dfa['Sex']=='People']
    dfa = dfa[dfa['Underlying cause of death']=='Due to other causes']
    dfa = dfa[dfa['Area of usual residence name'].isin(region)]
    dfag = dfa.groupby(['Month'], as_index=False)['Deaths'].sum()

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=dfg["Month"], y=dfg["Deaths"], name='Death by COVID-19',
                   line=dict(color='royalblue', width=4)))

    fig.add_trace(go.Scatter(x=dfag['Month'], y=dfag["Deaths"], name='Due to other causes',
                              line=dict(color='firebrick', width=4, dash='dot')))

    #fig.update_xaxes(showgrid=True, ticklabelmode="period", dtick="M1", tickformat="%b\n%Y", title='')

    fig.update_xaxes(
        rangeslider_visible=False,
        rangeselector=dict(
            buttons=list([
                dict(count=10, label="10m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(step="all")
            ])
        )
    )

    fig.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)'
    # 'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })


    card = df['Deaths'].sum()
    #card_b = card.map('{:,.0f}'.format)
    card_c = f"{card:,} TOTAL DEATHS"


    return fig, card_c

#============================================= GRAPH 1 =================================================================

@app.callback(Output('Graph 1', 'figure'),

               Input(component_id='region_dropdown', component_property='value')

              )

def render_content(region):

    df = table1.copy()
    df = df[df['Sex'] != 'People']
    df = df[df['Underlying cause of death']=='Due to COVID-19']
    df = df[df['Area of usual residence name'].isin(region)]
    dfg = df.groupby(['Sex'], as_index=False)['Deaths'].sum()


    fig = px.pie(dfg, values='Deaths', names='Sex')

    fig.update_layout(showlegend=False)


    return fig

#============================================= GRAPH 2 =================================================================


@app.callback(Output('Graph 2', 'figure'),

               Input(component_id='region_dropdown', component_property='value')

              )

def render_content(region):

    df = table1.copy()
    df = df[df['Sex'] == 'People']
    df = df[df['Underlying cause of death']=='Due to COVID-19']
    df = df[df['Area of usual residence name'].isin(region)]
    dfg = df.groupby(['Area of usual residence name','Underlying cause of death'], as_index=False)['Deaths','Population'].sum()


    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Scatter(x=dfg["Area of usual residence name"], y=dfg["Population"],name='Pop', fill='tozeroy',
                             mode='none'  # override default markers+lines
                             ),secondary_y=False)

    fig.add_trace(go.Scatter(x=dfg["Area of usual residence name"], y=dfg["Deaths"],name='Deaths', fill='tonexty',
                             mode='none'),secondary_y=True)

    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)'
        # 'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    },legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ))


    return fig

#============================================= GRAPH 3 =================================================================


@app.callback(Output('Graph 3', 'figure'),

               Input(component_id='region_dropdown', component_property='value')

              )

def render_content(region):

    df = table2C.copy()
    df = df[df['Geography type'] == 'London Borough']
    df = df[df['Underlying cause of death']=='Due to COVID-19']
    df['Borough'] = df['Area of usual residence name'].map(short_hand)
    dfg = df.groupby(['Borough'], as_index=False)['Rate'].sum()
    dfg = dfg.sort_values(by=['Rate'],ascending=False)

    dfag = df.groupby(['Borough'], as_index=False)['Deprivation Score'].mean()


    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Bar(x=dfg["Borough"], y=dfg["Rate"], name='Death Rate (Deaths per 100K)'), secondary_y=False)

    fig.add_trace(go.Scatter(x=dfag["Borough"], y=dfag["Deprivation Score"], name='Deprivation', mode='markers'), secondary_y=True)

    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)'},bargap=0.1)
    fig.update_xaxes(tickangle=45,showgrid=True, dtick="M1", tickformat="%b\n%Y", title='')
    # fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(yaxis_title="Death Rate")
    fig.update_traces(marker_color='rgb(214, 39, 40)',marker=dict(size=12,
                              line=dict(width=2,
                                        color='DarkSlateGrey')),
                              selector=dict(mode='markers'))


    return fig

# #============================================= GRAPH 4 =================================================================


@app.callback(Output('Graph 4', 'figure'),

               Input(component_id='region_dropdown', component_property='value')

              )

def render_content(region):

    df = table3.copy()
    df = df[df['Sex'] != 'People']
    df = df[df['Underlying cause of death']=='Due to COVID-19']
    dfg = df.groupby(['Deprivation decile'], as_index=False)['Deaths'].sum()


    fig = px.bar(dfg, x="Deprivation decile", y="Deaths")
    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)'},bargap=0.5)
    #fig.update_xaxes(tickangle=0,showgrid=True, ticklabelmode="period", dtick="M1", title='')
    # fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(yaxis_title="Deaths")
    fig.update_traces(marker_color='rgb(214, 39, 40)')

    return fig

#============================================= GRAPH 5 =================================================================


@app.callback(Output('Graph 5', 'figure'),

               Input(component_id='region_dropdown', component_property='value')

              )

def render_content(region):

    df = Deprivation_Index.copy()
    df = df.sort_values(by=['Index of Multiple Deprivation score'],ascending=True)
    df['Borough'] = df['Local Authority District'].map(short_hand)


    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Bar(name='Overall Deprivation', x=df["Borough"], y=df["Index of Multiple Deprivation score"]),secondary_y=False)

    fig.add_trace(go.Scatter(x=df["Borough"], y=df["Health Deprivation score"],name='Health Deprivation',
                             mode='lines+markers'),secondary_y=False)

    fig.update_xaxes(tickangle=45, showgrid=True)

    fig.update_traces(marker_color='rgb(214, 39, 40)',marker=dict(size=12,
                              line=dict(width=2,
                                        color='DarkSlateGrey')),
                              selector=dict(mode='markers'))

    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)'
        # 'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    },legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ))

    return fig

#============================================= GRAPH 6 =================================================================


@app.callback(Output('Graph 6', 'figure'),

               Input(component_id='region_dropdown', component_property='value')

              )

def render_content(region):

    df = Ethnicity.copy()
    df1 = df[(df['Area'] != 'City of London') & (df['Area'] != 'Inner London')]
    #df1['Borough'] = df1['Area'].map(short_hand)
    df2 = df1.sort_values(by=['%','Ethnicity'],ascending=[False,True])


    fig = px.bar(df2, x="Area", y="%", color="Ethnicity")
    fig.update_xaxes(tickangle=45,title='')

    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)'
        # 'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })

    return fig

#=========================================== TABLE =====================================================================

import dash_table as dt

@app.callback(Output('Table', 'children'),
               #Output('Card Utilisation Table', 'children')],
              Input(component_id='region_dropdown', component_property='value')
              )
def render_content(region):

    df_dash = Table.copy()

    #Formatting
    df_dash['Death Rate per (100K)'] = df_dash['Death Rate per (100K)'].map('{:,.0f}'.format)#to get numbers in format correctly
    df_dash['BAME Population %'] = df_dash['BAME Population %'].map('{:,.0f}'.format)  # to get numbers in format correctly
    df_dash['Deprivation Score'] = df_dash['Deprivation Score'].map('{:.0f}'.format)  # to get numbers in format correctly

    return html.Div([

            html. Br(),

            dbc.Row(dbc.Col(dt.DataTable(data=df_dash.to_dict('rows'),
                         columns=[{"name": i, "id": i} for i in df_dash.columns],
                         sort_action='native',
                         page_size=33,
                         fixed_rows={'headers': True},
                         style_table={'height': 800},

                         style_header={
                                             'backgroundColor': 'rgb(188, 219, 245)',
                                             'fontWeight': 'bold',
                                             'textAlign': 'center',
                                             'color': 'black',
                                             'border': '1px solid black'
                                         },
                         style_cell={'font_family': 'Nunito Sans',
                                                    'border': '1px solid grey',
                                                    'minWidth': 95, 'maxWidth': 95, 'width': 95,
                                                    'whiteSpace': 'normal',
                                                    'textAlign': 'center',
                                                    'backgroundColor': 'rgb(233, 243, 252)'
                                                    },
                                         )))
        ])

#============================================= GRAPH 7 =================================================================


@app.callback(Output('Graph 7', 'figure'),

               Input(component_id='region_dropdown', component_property='value')

              )

def render_content(region):

    dfg = Table.copy()

    fig = px.scatter_3d(dfg, x='Death Rate per (100K)', y='BAME Population %', z='Deprivation Score',
                    color='Borough', symbol='Borough', width=1500, height=900)

    return fig

#============================================= GRAPH MAP ===============================================================


access_token = 'pk.eyJ1IjoiemFpbmVpc2EiLCJhIjoiY2tlZWg0MXJvMGcwZzJyb3k1OXh0Ym55aiJ9.0SJ_VBRVxyWd6SmbdUwmKQ'

@app.callback(Output('Map', 'figure'),

               Input(component_id='region_dropdown', component_property='value'))


def render_content(region):

        df = table2C.copy()
        df = df[df['Geography type'] == 'London Borough']
        df = df[df['Underlying cause of death'] == 'Due to COVID-19']
        dfg = df.groupby(['Area of usual residence name'], as_index=False)['Deaths'].sum()
        df_merged = dfg.merge(Location,on=['Area of usual residence name'],how='left')

        # REMEMBER the as_index function turns the aggregate output from a Series into a Dataframe - important as some graphs/figures need Dfs
        dfmap_group = df_merged.groupby(['Area of usual residence name', 'Lat', 'Long'], as_index=False)['Deaths'].sum()
        dfmap_group['Deaths for label'] = dfmap_group['Deaths'].map('{:,.0f}'.format)
        dfmap_group['Label'] = dfmap_group['Deaths for label'].astype(str) + ' deaths at ' + dfmap_group['Area of usual residence name']

        locations = [go.Scattermapbox(
            lon=dfmap_group['Long'],
            lat=dfmap_group['Lat'],
            mode='markers',
            unselected={'marker': {'opacity': 0.5}},
            selected={'marker': {'opacity': 1, 'size': 50}},
            hoverinfo='text',
            hovertext=dfmap_group['Label'],
            marker=dict(
                size=dfmap_group['Deaths'] / 0.8,
                color='red',
                sizemode='area'
            )
        )]

        return {
                    'data': locations,
                    'layout': go.Layout(
                        uirevision='foo',  # preserves state of figure/map after callback activated
                        clickmode='event+select',
                        margin=dict(l=0, r=0, t=0, b=0),
                        hovermode='closest',
                        hoverdistance=2,
                        #title=dict(text="COVID CASES MAPPED", font = dict(size=35)), #irrelevant with the margins given
                        mapbox=dict(
                            accesstoken=access_token,
                            bearing=25,
                            # style='dark', # Can enter to style the graph
                            center=dict(
                                lat=51.505958,
                                # 51.50853, # is technically the centre of London, but the other co-ordinates fit better
                                lon=-0.126770
                                # -0.12574 # is technically the centre of London, but the other co-ordinates fit better
                            ),
                            pitch=20,
                            zoom=9.5
                        ),
                    )
                }



#=======================================================================================================================
if __name__ == '__main__':
    app.run_server(debug=True)
