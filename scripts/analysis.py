import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

def display_transactions_count(transactions_df):
    with st.container(border=True):
        st.write(f"**Total Transactions:** {len(transactions_df)}")

# function that shows a line plot of daily expenses over time and daily income over time
def display_daily_expenses_and_income(transactions_df):
    with st.container(border=True):
        # Time range selection
        start_date = pd.to_datetime(transactions_df['Date']).min().date()
        end_date = pd.to_datetime(transactions_df['Date']).max().date()
        date_range = st.date_input(
            "Select date range",
            value=(start_date, end_date),
            min_value=start_date,
            max_value=end_date
        )

        # Filter transactions based on selected date range
        mask = (transactions_df['Date'] >= date_range[0]) & (transactions_df['Date'] <= date_range[1])
        filtered_df = transactions_df[mask]

        # Prepare data for plotting
        daily_expenses = filtered_df[filtered_df['Type'] == 'Expense'].groupby('Date')['Amount'].sum().reset_index()
        daily_income = filtered_df[filtered_df['Type'] == 'Income'].groupby('Date')['Amount'].sum().reset_index()

        # Create interactive line plot using Plotly
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots

        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_trace(
            go.Scatter(x=daily_expenses['Date'], y=daily_expenses['Amount'], name="Expenses", line=dict(color="red")),
            secondary_y=False,
        )

        fig.add_trace(
            go.Bar(x=daily_income['Date'], y=daily_income['Amount'], name="Income", marker_color="green"),
            secondary_y=True,
        )

        fig.update_layout(
            title_text="Daily Expenses and Income Over Time",
            xaxis_title="Date",
            yaxis_title="Amount (Expenses)",
            yaxis2_title="Amount (Income)",
        )

        st.plotly_chart(fig, use_container_width=True)

        st.write(f"**Total Expenses:** {daily_expenses['Amount'].sum():.2f} PLN")
        st.write(f"**Total Income:** {daily_income['Amount'].sum():.2f} PLN")

