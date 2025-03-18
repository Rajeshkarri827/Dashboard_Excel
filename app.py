# import pandas as pd
# import plotly.express as px
# import dash
# import dash_bootstrap_components as dbc
# from dash import dcc, html, Input, Output
# import os

# # Function to read data from the Excel file
# def get_data():
#     # Ensure the file exists before reading
#     excel_path = os.path.join('Project', 'sampledata.xlsx')
#     df = pd.read_excel(excel_path)
#     return df

# # Initialize Dash app with Bootstrap stylesheet
# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
# app.title = "Enhanced Excel Dashboard"

# app.layout = dbc.Container([
#     html.H1("Enhanced Excel Data Visualization Dashboard", className='text-center my-4'),
    
#     # Interval for real-time update simulation (every 60 seconds)
#     dcc.Interval(id='interval-component', interval=60000, n_intervals=0),
    
#     # Dropdown for category filtering (applies to both tabs)
#     dbc.Row([
#         dbc.Col([
#             html.Label("Select Category:"),
#             dcc.Dropdown(
#                 id='category-dropdown',
#                 options=[{'label': cat, 'value': cat} for cat in get_data()['Category'].unique()],
#                 multi=True,
#                 placeholder="Select categories"
#             )
#         ], width=6)
#     ], className="mb-4"),
    
#     # Tabs for navigation: Overview & Details
#     dbc.Tabs(id='tabs', active_tab='tab-overview', children=[
#         dbc.Tab(label="Overview", tab_id="tab-overview"),
#         dbc.Tab(label="Details", tab_id="tab-details"),
#     ]),
    
#     # Content area for the active tab
#     html.Div(id='tab-content', className='mt-4')
# ], fluid=True)

# # Callback to update tab content based on selected category and time interval
# @app.callback(
#     Output('tab-content', 'children'),
#     [Input('tabs', 'active_tab'),
#      Input('category-dropdown', 'value'),
#      Input('interval-component', 'n_intervals')]
# )
# def render_tab_content(active_tab, selected_categories, n_intervals):
#     df = get_data()
#     if selected_categories:
#         df_filtered = df[df['Category'].isin(selected_categories)]
#     else:
#         df_filtered = df

#     # --- Summary Metrics for Overview ---
#     total_sales = df_filtered['Sales'].sum()
#     avg_profit = df_filtered['Profit'].mean()
#     total_records = len(df_filtered)
#     summary_cards = dbc.Row([
#         dbc.Col(dbc.Card(
#             dbc.CardBody([
#                 html.H4("Total Sales", className="card-title"),
#                 html.P(f"${total_sales:,.2f}", className="card-text")
#             ]), color="primary", inverse=True), width=4),
#         dbc.Col(dbc.Card(
#             dbc.CardBody([
#                 html.H4("Average Profit", className="card-title"),
#                 html.P(f"${avg_profit:,.2f}", className="card-text")
#             ]), color="success", inverse=True), width=4),
#         dbc.Col(dbc.Card(
#             dbc.CardBody([
#                 html.H4("Total Records", className="card-title"),
#                 html.P(f"{total_records}", className="card-text")
#             ]), color="info", inverse=True), width=4)
#     ], className="mb-4")

#     # --- Visualizations ---
    
#     # Bar Chart: Total Sales by Category
#     sales_by_category = df_filtered.groupby('Category', as_index=False)['Sales'].sum()
#     fig_bar = px.bar(sales_by_category, x='Category', y='Sales',
#                      title='Total Sales by Category', color='Category',
#                      labels={'Sales': 'Total Sales'}, hover_data={'Sales': ':.2f'})
    
#     # Line Chart: Monthly Sales Trend
#     sales_by_month = df_filtered.groupby('Month', as_index=False)['Sales'].sum()
#     month_order = ['January', 'February', 'March', 'April', 'May', 'June',
#                    'July', 'August', 'September', 'October', 'November', 'December']
#     sales_by_month['Month'] = pd.Categorical(sales_by_month['Month'], categories=month_order, ordered=True)
#     sales_by_month = sales_by_month.sort_values('Month')
#     fig_line = px.line(sales_by_month, x='Month', y='Sales',
#                        title='Monthly Sales Trend', markers=True, labels={'Sales': 'Total Sales'})
    
#     # Scatter Plot: Sales vs. Profit
#     fig_scatter = px.scatter(df_filtered, x='Sales', y='Profit', title='Sales vs. Profit',
#                              color='Category', hover_data=['Month'],
#                              labels={'Sales': 'Sales ($)', 'Profit': 'Profit ($)'})
    
#     # Pie Chart: Sales Distribution by Month
#     fig_pie = px.pie(sales_by_month, names='Month', values='Sales',
#                      title='Sales Distribution by Month', color_discrete_sequence=px.colors.qualitative.Pastel)
    
#     # Heatmap: Correlation between Sales and Profit
#     corr = df_filtered[['Sales', 'Profit']].corr()
#     fig_heatmap = px.imshow(corr, text_auto=True, title='Correlation Heatmap')
    
#     # Boxplot: Profit Distribution by Category
#     fig_boxplot = px.box(df_filtered, x='Category', y='Profit', title='Profit Distribution by Category')

#     # --- Tab Layouts ---
#     if active_tab == 'tab-overview':
#         content = html.Div([
#             summary_cards,
#             dbc.Row([
#                 dbc.Col(dcc.Graph(figure=fig_bar), width=12)
#             ])
#         ])
#     elif active_tab == 'tab-details':
#         content = dbc.Row([
#             dbc.Col(dcc.Graph(figure=fig_line), md=6),
#             dbc.Col(dcc.Graph(figure=fig_scatter), md=6),
#             dbc.Col(dcc.Graph(figure=fig_pie), md=6),
#             dbc.Col(dcc.Graph(figure=fig_heatmap), md=6),
#             dbc.Col(dcc.Graph(figure=fig_boxplot), md=12)
#         ])
#     else:
#         content = html.Div("No tab selected")
#     return content

# if __name__ == '__main__':
#     import os 
#     port = int(os.getenv("PORT", 8050))
#     # Host '0.0.0.0' makes the app accessible externally.
#     app.run(debug=False, host='0.0.0.0', port=port)

import pandas as pd
import plotly.express as px
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
import os

# Function to read data from the Excel file
def get_data():
    excel_path = os.path.join('Project', 'sampledata.xlsx')
    df = pd.read_excel(excel_path)
    return df

# Initialize Dash app with Bootstrap stylesheet
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Excel Dashboard"

app.layout = dbc.Container([
    html.H1("Excel Data Visualization Dashboard", className='text-center my-4'),
    
    # Navigation bar with anchor links for redirection
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(html.A("Overview", href="#overview", className="nav-link")),
            dbc.NavItem(html.A("Details", href="#details", className="nav-link"))
        ],
        brand="Dashboard Navigation",
        color="primary",
        dark=True,
        className="mb-4",
        fluid=True
    ),
    
    # Interval component for real-time updates (every 60 seconds)
    dcc.Interval(id='interval-component', interval=60000, n_intervals=0),
    
    # Dropdown for category filtering
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
    
    # Overview Section (with an anchor ID for redirection)
    html.H2("Overview", id="overview", className="text-center my-4"),
    dbc.Row(id='overview-section'),
    
    # Details Section (with an anchor ID for redirection)
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

    # --- Overview Section ---
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

    # Bar Chart: Total Sales by Category
    sales_by_category = df_filtered.groupby('Category', as_index=False)['Sales'].sum()
    fig_bar = px.bar(sales_by_category, x='Category', y='Sales',
                     title='Total Sales by Category', color='Category',
                     labels={'Sales': 'Total Sales'}, hover_data={'Sales': ':.2f'})
    
    overview_content = [
        summary_cards,
        dbc.Row([dbc.Col(dcc.Graph(figure=fig_bar), width=12)])
    ]

    # --- Details Section ---
    # Line Chart: Monthly Sales Trend
    sales_by_month = df_filtered.groupby('Month', as_index=False)['Sales'].sum()
    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    sales_by_month['Month'] = pd.Categorical(sales_by_month['Month'], categories=month_order, ordered=True)
    sales_by_month = sales_by_month.sort_values('Month')
    fig_line = px.line(sales_by_month, x='Month', y='Sales',
                       title='Monthly Sales Trend', markers=True, labels={'Sales': 'Total Sales'})
    
    # Scatter Plot: Sales vs. Profit
    fig_scatter = px.scatter(df_filtered, x='Sales', y='Profit', title='Sales vs. Profit',
                             color='Category', hover_data=['Month'],
                             labels={'Sales': 'Sales ($)', 'Profit': 'Profit ($)'})
    
    # Pie Chart: Sales Distribution by Month
    fig_pie = px.pie(sales_by_month, names='Month', values='Sales',
                     title='Sales Distribution by Month', color_discrete_sequence=px.colors.qualitative.Pastel)
    
    # Heatmap: Correlation between Sales and Profit
    corr = df_filtered[['Sales', 'Profit']].corr()
    fig_heatmap = px.imshow(corr, text_auto=True, title='Correlation Heatmap')
    
    # Boxplot: Profit Distribution by Category
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
