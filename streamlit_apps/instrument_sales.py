from utils import get_data_from_gsheets
import  gspread
import streamlit as st
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# sheet_name = config.sales_cash_gsheet_name
# 1. MAKE IT WIDE (This must be the very first Streamlit command)
st.set_page_config(layout="wide", page_title="Instrument Sales Report")

df = get_data_from_gsheets(
    sheet_name='sales_by_product_cash_summary_sheets',
    gc=gspread.service_account()
)

df['month'] = pd.to_datetime(df['month'])
df['year'] = df['month'].dt.year.astype(str)
df = df.sort_values('month')

# Create a display version of the dataframe for this chart
df_display = df.copy()

st.title("Instrument Sales Report")
st.divider()

st.header("Annual Instrument Sales ($)")
yearly_instr = df.groupby(['year', 'instrument'])['amount'].sum().reset_index()
yearly_totals = yearly_instr.groupby('year')['amount'].sum().reset_index()

yearly_service = df.groupby(['year', 'product_service'])['amount'].sum().reset_index()

fig = make_subplots(specs=[[{"secondary_y": True}]])

for instr in yearly_instr['instrument'].unique():
    instr_data = yearly_instr[yearly_instr['instrument'] == instr]
    fig.add_trace(
        go.Bar(
            x=instr_data['year'],
            y=instr_data['amount'],
            name=instr,
            hovertemplate=f'<b>{instr}</b>: ' + '$%{y:,.0f}<extra></extra>'
        ),
        secondary_y=False,
    )

# 4. Add the Secondary Lines (Product Service Trends)
colors = {'Consignment Sale': '#FFFFFF', 'Inventory Sales': '#FFD700'} # Custom colors for lines

for service in yearly_service['product_service'].unique():
    service_data = yearly_service[yearly_service['product_service'] == service]
    fig.add_trace(
        go.Scatter(
            x=service_data['year'],
            y=service_data['amount'],
            name=service,
            mode='lines+markers',
            line=dict(width=4, color=colors.get(service)),
            # Updated Hover: Shows "DV Owned: $50,000"
            hovertemplate=f'<b>{service} Total</b>: ' + '$%{y:,.0f}<extra></extra>'),
        secondary_y=True,
    )

# 5. UI and Layout Tweaks
fig.update_layout(
    title_text="Annual Sales ($) by Instrument",
    barmode='stack',
    hovermode="x unified",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    # Styling the hover label to be cleaner
    hoverlabel=dict(bgcolor="rgba(33, 33, 33, 0.8)", font_size=14, font_family="Arial")
)

# Set axis titles
fig.update_yaxes(title_text="Instrument Sales ($)", secondary_y=False)
fig.update_yaxes(title_text="Consignment vs DV ($)", secondary_y=True)

st.plotly_chart(fig)