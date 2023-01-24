import plotly
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.express as px
from dash import Dash, dcc, html
import pandas as pd
from dash.dependencies import Input, Output 
import dash

# df = pd.read_csv("/Users/jishnusrivastava/Documents/Exploratory-Data-Analysis/IBM_HR.csv")
df = pd.read_csv("https://raw.githubusercontent.com/Jks08/Exploratory-Data-Analysis/main/IBM_HR.csv")
df.tail()

data = [go.Bar(x=df['Age'],y=df['TotalWorkingYears'])]
layout = go.Layout(xaxis=dict(title='Age'),yaxis=dict(title='Total Working Years'))
fig = go.Figure(data,layout=layout)
fig.show()

fig1 = make_subplots(rows=2,cols=2, specs=[[{"type": "bar"}, {"type": "pie"}],[{'type':'histogram'},{'type':'bar'}]],subplot_titles=("Plot 1", "Plot 2", "Plot 3", "Plot 4"))

fig1.add_trace(go.Bar(x=df['Age'],y=df['TotalWorkingYears']),row=1,col=1)
fig1.add_trace(go.Pie(labels = df['EducationField'],values=df['DailyRate']),row=1,col=2)
fig1.add_trace(go.Histogram(x=df['YearsSinceLastPromotion'],y=df['DailyRate']),row=2,col=1)
fig1.add_trace(go.Bar(x=df['HourlyRate'],y=df['TotalWorkingYears']),row=2,col=2)

fig1.update_xaxes(title_text="Age of Employee", row=1, col=1)
fig1.update_xaxes(title_text="Field of Education", row=1, col=2)
fig1.update_xaxes(title_text="Years since last promotion", showgrid=False, row=2, col=1)
fig1.update_xaxes(title_text="Hourly Rate", row=2, col=2)


fig1.update_yaxes(title_text="Total Working Hours", row=1, col=1)
fig1.update_yaxes(title_text="Daily Rate", row=1, col=2)
fig1.update_yaxes(title_text="Daily Rate", showgrid=False, row=2, col=1)
fig1.update_yaxes(title_text="Total Working Hours", row=2, col=2)

fig1.show()

tempFig = px.line_3d(df,x='Age',y='TotalWorkingYears',z='MonthlyIncome', color = 'JobSatisfaction',title='Age vs Total Working Hours vs Monthly Income',template='plotly_dark')

# tempFig = px.pie(df, values='Age', names='EducationField', title='Daily Rate vs Education Field', width=800,height=800)
# tempFig.show()

# options = [{'label':i,'value':i} for i in df.select_dtypes(include=['int64']).columns]
# options

app = dash.Dash()
app.title = 'Attrition Analysis - JKS'
server = app.server

app.layout = html.H1(children=[
    html.P(
        id="parent",
        children = [html.P(id="IBM_HR", children='IBM HR Attrition Analysis', style={'textAlign':'center','backgroundColor':'beige','color':'Blue'}),
        dcc.Dropdown(id="dropdown",
        options = [{'label':i,'value':i} for i in df.select_dtypes(include=['int64']).columns],
        value=['DailyRate','MonthlyIncome'],
        multi=True), 
        dcc.Graph(id="graph"),]),
    html.Div([
        html.P(children='Age vs Total Working Hours vs Monthly Income',style={'textAlign':'center','backgroundColor':'beige','color':'Green'}),
        dcc.Graph(id='graph2',figure=tempFig)
        ]
    ),
    html.Div([
        html.P(children='4 Subplots 🥱',style={'textAlign':'center','color':'Red'}),
        dcc.Graph(id='graph3',figure=fig1)
    ]
    ),
    html.Div([
        html.H1(children='Key Findings and Insights ',style={'textAlign':'left','color':'#00C68B', 'fontSize':50,'fontFamily':'Times New Roman'}),
        html.P(children="🟡 'Attrition' was at 66.67% for 19 year olds, but then the 'Attrition' rate drastically drops until employees hit the age of 58, whereafter 'Attrition' jumps up to 35.71%.",style={'textAlign':'left','color':'Black', 'fontSize':20,'fontFamily':'Times New Roman'}),
        html.P(children="🟡 When 'YearsAtCompany' was 0 the 'Attrition' rate was 36.36%, whereas when 'Years at Company' became 1, the attrition rate was 34.50%.", style={'textAlign':'left','color':'Black', 'fontSize':20,'fontFamily':'Times New Roman'}),
        html.P(children="🟡 For the 'MaritalStatus - Single' the attrition rate was 25.53%, and interestingly it was much lower for married people at 12.48% and even lower for divorced at 10.09%.", style={'textAlign':'left','color':'Black', 'fontSize':20,'fontFamily':'Times New Roman'}),
        html.P(children="🟡 The 'Attrition' rate was 25.00% for 'JobSatisfaction' of 1, but then it dropped to 16.67% for 'JobSatisfaction' of 2, and then it dropped even further to 12.50% for 'JobSatisfaction' of 3.", style={'textAlign':'left','color':'Black', 'fontSize':20,'fontFamily':'Times New Roman'}),
        html.P(children="🟡 'EducationField' of Human Resources has an 'Attrition' rate of 25.92%, whereas that of Medical was at 13.57%.", style={'textAlign':'left','color':'Black', 'fontSize':20,'fontFamily':'Times New Roman'}),
        html.P(children="🟡 When 'TotalWorkingYears' was 0 the attrition rate was 45.45%, when 1 the attrition rate was 49.38% and at 40 it was 100%, due to retirement.", style={'textAlign':'left','color':'Black', 'fontSize':20,'fontFamily':'Times New Roman'}),
    ]),
    html.Div([
        html.P(children='JKS ',style={'textAlign':'center','color':'Black', 'fontSize':50,'fontFamily':'Courier New'}),
    ])
], style={'backgroundColor':'White'})

@app.callback(Output("graph", "figure"), [Input("dropdown", "value")])

# def update_graph(dropdown):
#     fig = px.histogram(df, x=dropdown, color="Attrition", title=f"Attrition vs {dropdown}")
#     return fig

# def update_graph(dropdown):
#     print(dropdown)
#     fig = go.Figure([go.Scatter(x=df['Age'],y=df['{}'.format(dropdown)],line=dict(color='firebrick'), mode='lines+markers', name='{}'.format(dropdown))])
#     fig.update_layout(title=f"Attrition vs {dropdown}", xaxis_title="Age", yaxis_title="{}".format(dropdown))
#     return fig

# def update_graph(dropdown):
#     print(dropdown)
#     # fig = go.Figure([go.Bar(x=df['Age'],y=df['{}'.format(dropdown)])])
#     fig = px.line_3d(df,x=df['Age'],y=df['{}'.format(dropdown)],z=df['TotalWorkingYears'],color=df['JobSatisfaction'],title=f"Attrition vs {dropdown}")
#     return fig

# def update_graph(dropdown):
#     print(dropdown)
#     fig = px.bar(df, x=df['Age'], y=df['{}'.format(dropdown)], color=df['Attrition'], title=f"Attrition vs {dropdown}")
#     return fig

def update_graph(dropdown):
    print(dropdown)
    fig = px.scatter_matrix(df, dimensions=dropdown, color="Attrition", title=f"Attrition analysis using {dropdown}",template='plotly_dark')
    return fig

if __name__=='__main__':
    app.run_server()
