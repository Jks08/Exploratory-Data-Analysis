import plotly
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.express as px
from dash import Dash, dcc, html
import pandas as pd
from dash.dependencies import Input, Output 
import dash
import numpy as np
import plotly.tools as tls
import plotly.figure_factory as ff

# df = pd.read_csv("/Users/jishnusrivastava/Documents/Exploratory-Data-Analysis/IBM_HR.csv")
df = pd.read_csv("https://raw.githubusercontent.com/Jks08/Exploratory-Data-Analysis/main/IBM_HR.csv")
df = df.drop(['Over18','EmployeeCount','StandardHours'],axis=1)
df.Attrition.replace(to_replace = dict(Yes = 1, No = 0), inplace = True)
df.describe()
df.tail()

data = [go.Bar(x=df['Age'],y=df['TotalWorkingYears'])]
layout = go.Layout(xaxis=dict(title='Age'),yaxis=dict(title='Total Working Years'))
fig = go.Figure(data,layout=layout)
fig.show()

fig1 = make_subplots(rows=2,cols=2, specs=[[{"type": "bar"}, {"type": "pie"}],[{'type':'histogram'},{'type':'bar'}]],subplot_titles=("Age vs Total Working Hours", "Education pie chart", "Daily Rate vs Years Since Promotion", "Total Working Hours vs Hourly Rate"))

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

# fig1.show()

tempFig = px.line_3d(df,x='Age',y='TotalWorkingYears',z='MonthlyIncome', color = 'JobSatisfaction',title='Age vs Total Working Hours vs Monthly Income',template='plotly_dark')

# tempFig = px.pie(df, values='Age', names='EducationField', title='Daily Rate vs Education Field', width=800,height=800)
# tempFig.show()

# options = [{'label':i,'value':i} for i in df.select_dtypes(include=['int64']).columns]
# options
attrition = df[(df['Attrition'] != 0)]
no_attrition = df[(df['Attrition'] == 0)]

trace = go.Bar(x = (len(attrition), len(no_attrition)), y = ['Yes Attrition', 'No Attition'], orientation = 'h', marker=dict(color=['MediumTurquoise', 'tomato']))
                    
# go.Figure(data = [trace]).show()


def plot_distribution(var_select, bin_size): 
    corr = df['Attrition'].corr(df[var_select])
    corr = np.round(corr,3)
    tmp1 = attrition[var_select]
    tmp2 = no_attrition[var_select]
    hist_data = [tmp1, tmp2]
    
    group_labels = ['Yes Attrition', 'No Attrition']
    colors = ['MediumTurquoise', 'tomato']

    fig = ff.create_distplot(hist_data, group_labels, colors = colors, show_hist = True, 
                             curve_type='kde', bin_size = bin_size)
    
    fig['layout'].update(title = var_select+' '+'(corr target ='+ str(corr)+')',autosize=False,width=1000,height=500)
    return fig

def barplot(var_select, x_no_numeric) :
    tmp1 = df[(df['Attrition'] != 0)]
    tmp2 = df[(df['Attrition'] == 0)]
    tmp3 = pd.DataFrame(pd.crosstab(df[var_select],df['Attrition']), )
    tmp3['Attr%'] = tmp3[1] / (tmp3[1] + tmp3[0]) * 100
    if x_no_numeric == True  : 
        tmp3 = tmp3.sort_values(1, ascending = False)

    color=['MediumTurquoise', 'tomato']
    trace1 = go.Bar(
        x=tmp1[var_select].value_counts().keys().tolist(),
        y=tmp1[var_select].value_counts().values.tolist(),
        name='Yes Attrition',opacity = 1.0, marker=dict(
        color='red',
        line=dict(color='#000000',width=1)))

    
    trace2 = go.Bar(
        x=tmp2[var_select].value_counts().keys().tolist(),
        y=tmp2[var_select].value_counts().values.tolist(),
        name='No Attrition', opacity = 1.0, marker=dict(
        color='blue',
        line=dict(color='#000000',width=1)))
    
    trace3 =  go.Scatter(   
        x=tmp3.index,
        y=tmp3['Attr%'],
        yaxis = 'y2',
        name='% Attrition', opacity = 0.6, marker=dict(
        color='black',
        line=dict(color='#000000',width=0.5
        )))

    layout = dict(title =  str(var_select),xaxis=dict(), yaxis=dict(title= 'Count'), yaxis2=dict(range= [-0, 75], overlaying= 'y', anchor= 'x', 
                          side= 'right',
                          zeroline=False,
                          showgrid= False, 
                          title= '% Attrition'))

    fig = go.Figure(data=[trace1, trace2, trace3], layout=layout)
    fig.update_layout(autosize=False,width=1000,height=500)
    fig.show()

figMulti = make_subplots(rows=1,cols=2,subplot_titles=('Age','DailyRate'))
for trace in plot_distribution('Age', False).select_traces():
    figMulti.add_trace(trace,row=1,col=1)
for trace in plot_distribution('DailyRate', 100).select_traces():
    figMulti.add_trace(trace,row=1,col=2)

figMulti1 = make_subplots(rows=1,cols=2,subplot_titles=('DistanceFromHome','HourlyRate'))
for trace in plot_distribution('DistanceFromHome', False).select_traces():
    figMulti1.add_trace(trace,row=1,col=1)
for trace in plot_distribution('HourlyRate', False).select_traces():
    figMulti1.add_trace(trace,row=1,col=2)

figMulti2 = make_subplots(rows=1,cols=2,subplot_titles=('MonthlyIncome','MonthlyRate'))
for trace in plot_distribution('MonthlyIncome', 100).select_traces():
    figMulti2.add_trace(trace,row=1,col=1)
for trace in plot_distribution('MonthlyRate', 100).select_traces():
    figMulti2.add_trace(trace,row=1,col=2)

figMulti3 = make_subplots(rows=1,cols=2,subplot_titles=('NumCompaniesWorked','PercentSalaryHike'))
for trace in plot_distribution('NumCompaniesWorked', False).select_traces():
    figMulti3.add_trace(trace,row=1,col=1)
for trace in plot_distribution('PercentSalaryHike', False).select_traces():
    figMulti3.add_trace(trace,row=1,col=2)

figMulti4 = make_subplots(rows=1,cols=2,subplot_titles=('TotalWorkingYears','TrainingTimesLastYear'))
for trace in plot_distribution('TotalWorkingYears', False).select_traces():
    figMulti4.add_trace(trace,row=1,col=1)
for trace in plot_distribution('TrainingTimesLastYear', False).select_traces():
    figMulti4.add_trace(trace,row=1,col=2)

figMulti5 = make_subplots(rows=1,cols=2,subplot_titles=('YearsAtCompany','YearsInCurrentRole'))
for trace in plot_distribution('YearsAtCompany', False).select_traces():
    figMulti5.add_trace(trace,row=1,col=1)
for trace in plot_distribution('YearsInCurrentRole', False).select_traces():
    figMulti5.add_trace(trace,row=1,col=2)

figMulti6 = make_subplots(rows=1,cols=2,subplot_titles=('YearsSinceLastPromotion','YearsWithCurrManager'))
for trace in plot_distribution('YearsSinceLastPromotion', False).select_traces():
    figMulti6.add_trace(trace,row=1,col=1)
for trace in plot_distribution('YearsWithCurrManager', False).select_traces():
    figMulti6.add_trace(trace,row=1,col=2)

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
        html.P(children='Some Subplots',style={'textAlign':'center','color':'Red'}),
        dcc.Graph(id='graph3',figure=fig1)
    ]),
    html.Div([
        html.P(children='Attrition vs Age and Daily rate',style={'textAlign':'left','color':'Blue'}),
        dcc.Graph(figure=figMulti)
    ]),
    html.Div([
        html.P(children='Attrition vs Distance from Home and Hourly Rate',style={'textAlign':'left','color':'Blue'}),
        dcc.Graph(figure=figMulti1)
    ]),
    html.Div([
        html.P(children='Attrition vs Monthly Income and Monthly Rate',style={'textAlign':'left','color':'Blue'}),
        dcc.Graph(figure=figMulti2)
    ]),
    html.Div([
        html.P(children='Attrition vs Num Companies Worked and Percent Salary Hike',style={'textAlign':'left','color':'Blue'}),
        dcc.Graph(figure=figMulti3)
    ]),
    html.Div([
        html.P(children='Attrition vs Total Working Years and Training Times Last Year',style={'textAlign':'left','color':'Blue'}),
        dcc.Graph(figure=figMulti4)
    ]),
    html.Div([
        html.P(children='Attrition vs Years At Company and Years In Current Role',style={'textAlign':'left','color':'Blue'}),
        dcc.Graph(figure=figMulti5)
    ]),
    html.Div([
        html.P(children='Attrition vs Years Since Last Promotion and Years With Current Manager',style={'textAlign':'left','color':'Blue'}),
        dcc.Graph(figure=figMulti6)
    ]),
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
        html.H1(children="Conclusion",style={'textAlign':'left','color':'#00C68B', 'fontSize':50,'fontFamily':'Times New Roman'}),
        html.P(children="🟡 We conclude that Attrition has a higher percentage when employees are younger than compared to older. Also, as Job Satisfaction increases, Attrition becomes lesser.", style={'textAlign':'left','color':'Black', 'fontSize':15,'fontFamily':'Times New Roman'}),
    ]),
    html.Div([
        html.H1(children='By - JKS ', style={'textAlign':'center','color':'Black', 'fontSize':50,'fontFamily':'Courier New'})
    ]),
    html.Div([
        html.A('Github of JKS', href='http://github.com/Jks08', target='http://github.com/Jks08', style={'textAlign':'center','color':'Black', 'fontSize':20,'fontFamily':'Courier New'})
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
    df1 = pd.read_csv("https://raw.githubusercontent.com/Jks08/Exploratory-Data-Analysis/main/IBM_HR.csv")
    print(dropdown)
    fig = px.scatter_matrix(df1, dimensions=dropdown, color="Attrition", title=f"Attrition analysis using {dropdown}",template='plotly_dark')
    return fig

if __name__=='__main__':
    app.run_server()
