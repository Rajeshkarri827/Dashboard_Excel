import pandas as pd
import plotly.express as px
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
import os


def get_data():
    excel_path = os.path.join('Project', 'sampledata.xlsx')
    df = pd.read_excel(excel_path)
    return df


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Enhanced Excel Dashboard"

app.layout = dbc.Container([
   
    html.H1("Enhanced Excel Data Visualization Dashboard",
            className='text-center my-4 sticky-title'),
    
  
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(html.A("Overview", href="#overview", className="nav-link")),
            dbc.NavItem(html.A("Details", href="#details", className="nav-link"))
        ],
        brand="Dashboard Navigation",
        color="primary",
        dark=True,
        className="mb-4 sticky-navbar",
        fluid=True
    ),
    
  
    dcc.Interval(id='interval-component', interval=60000, n_intervals=0),
    
    
    dbc.Row([
        dbc.Col([
            html.Label("Select Category:"),
            dcc.Dropdown(
                id='category-dropdown',
                options=[{'label': cat, 'value': cat} for cat in get_data()['Category'].unique()],
                multi=True,
                placeholder="Select categories"
            )
        ], width=6)
    ], className="mb-4"),
    
    
    html.H2("Overview", id="overview", className="text-center my-4"),
    dbc.Row(id='overview-section'),
    
    
    html.H2("Details", id="details", className="text-center my-4"),
    dbc.Row(id='details-section')
], fluid=True)

@app.callback(
    [Output('overview-section', 'children'),
     Output('details-section', 'children')],
    [Input('category-dropdown', 'value'),
     Input('interval-component', 'n_intervals')]
)
def update_dashboard(selected_categories, n_intervals):
    df = get_data()
    if selected_categories:
        df_filtered = df[df['Category'].isin(selected_categories)]
    else:
        df_filtered = df

   
    total_sales = df_filtered['Sales'].sum()
    avg_profit = df_filtered['Profit'].mean()
    total_records = len(df_filtered)
    summary_cards = dbc.Row([
        dbc.Col(dbc.Card(
            dbc.CardBody([
                html.H4("Total Sales", className="card-title"),
                html.P(f"${total_sales:,.2f}", className="card-text")
            ]), color="primary", inverse=True), width=4),
        dbc.Col(dbc.Card(
            dbc.CardBody([
                html.H4("Average Profit", className="card-title"),
                html.P(f"${avg_profit:,.2f}", className="card-text")
            ]), color="success", inverse=True), width=4),
        dbc.Col(dbc.Card(
            dbc.CardBody([
                html.H4("Total Records", className="card-title"),
                html.P(f"{total_records}", className="card-text")
            ]), color="info", inverse=True), width=4)
    ], className="mb-4")

    
    sales_by_category = df_filtered.groupby('Category', as_index=False)['Sales'].sum()
    fig_bar = px.bar(sales_by_category, x='Category', y='Sales',
                     title='Total Sales by Category', color='Category',
                     labels={'Sales': 'Total Sales'}, hover_data={'Sales': ':.2f'})
    
    overview_content = [
        summary_cards,
        dbc.Row([dbc.Col(dcc.Graph(figure=fig_bar), width=12)])
    ]


    sales_by_month = df_filtered.groupby('Month', as_index=False)['Sales'].sum()
    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    sales_by_month['Month'] = pd.Categorical(sales_by_month['Month'], categories=month_order, ordered=True)
    sales_by_month = sales_by_month.sort_values('Month')
    fig_line = px.line(sales_by_month, x='Month', y='Sales',
                       title='Monthly Sales Trend', markers=True, labels={'Sales': 'Total Sales'})
    
   
    fig_scatter = px.scatter(df_filtered, x='Sales', y='Profit', title='Sales vs. Profit',
                             color='Category', hover_data=['Month'],
                             labels={'Sales': 'Sales ($)', 'Profit': 'Profit ($)'})
    
  
    fig_pie = px.pie(sales_by_month, names='Month', values='Sales',
                     title='Sales Distribution by Month', color_discrete_sequence=px.colors.qualitative.Pastel)
    
   
    corr = df_filtered[['Sales', 'Profit']].corr()
    fig_heatmap = px.imshow(corr, text_auto=True, title='Correlation Heatmap')
    
    
    fig_boxplot = px.box(df_filtered, x='Category', y='Profit', title='Profit Distribution by Category')

    details_content = dbc.Row([
        dbc.Col(dcc.Graph(figure=fig_line), md=6),
        dbc.Col(dcc.Graph(figure=fig_scatter), md=6),
        dbc.Col(dcc.Graph(figure=fig_pie), md=6),
        dbc.Col(dcc.Graph(figure=fig_heatmap), md=6),
        dbc.Col(dcc.Graph(figure=fig_boxplot), md=12)
    ])

    return overview_content, details_content

if __name__ == '__main__':
    import os 
    port = int(os.getenv("PORT", 8050))
    app.run(debug=False, host='0.0.0.0', port=port)
