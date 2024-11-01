import streamlit as st
import math
import pandas as pd

# Page title
st.title("📝 Mortgage Repayment Calculator")
st.divider()

# Input section
st.write("### Loan Term")
col1, col2, col3 = st.columns(3)

loan_value = col1.number_input(
    "Loan Value ($)", min_value=100000, value=300000, step=500)
interest_rate = col2.number_input(
    "Interest (%)", min_value=1.0, value=2.5, step=0.05)
loan_term = col3.number_input(
    "Term (Years)", min_value=5, value=25, max_value=35)

st.markdown(
    f"You are borrowing :blue[${loan_value:,.0f}] at an interest rate of :blue[{interest_rate:.2f}%] for a term of :blue[{loan_term}] years."
)

st.divider()

# Calculations
monthly_interest_rate = (interest_rate / 100) / 12
number_of_payments = loan_term * 12
monthly_payment = (
    loan_value
    * (monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments)
    / ((1 + monthly_interest_rate) ** number_of_payments - 1)
)
total_payments = monthly_payment * number_of_payments
total_interest = total_payments - loan_value

# Repayment schedule calculation
schedule = []
remaining_balance = loan_value
total_interest_24 = 0

for i in range(1, number_of_payments + 1):
    interest_payment = remaining_balance * monthly_interest_rate
    principal_payment = monthly_payment - interest_payment
    remaining_balance -= principal_payment
    penalty = remaining_balance * 0.015
    year = math.ceil(i / 12)

    # Add to schedule
    schedule.append([year, i, monthly_payment, principal_payment,
                    interest_payment, remaining_balance, penalty])

    # Sum interest for the first 24 payments
    if i <= 24:
        total_interest_24 += interest_payment

# Display repayment metrics
st.write("### Repayment")
col1, col2 = st.columns([1, 2])

# Create DataFrame
df = pd.DataFrame(
    schedule,
    columns=["Year", "Month", "Payment ($)", "Principal ($)",
             "Interest ($)", "Remaining Balance ($)", "Penalty ($)"]
)

col1.metric(label="Monthly Payment", value=f"${monthly_payment:,.0f}")
col1.metric(label="Total Payment", value=f"${total_payments:,.0f}")
col1.metric(label="Interest (Lifetime)", value=f"${total_interest:,.0f}")
col1.metric(label="Interest (24 Months)", value=f"${total_interest_24:,.0f}")

# Yearly outstanding balance line chart
payments_df = df[["Year", "Remaining Balance ($)"]].groupby("Year").min()
col2.line_chart(data=payments_df, x_label="Year",
                y_label="Outstanding Balance", height=400)

st.divider()

# Monthly payment breakdown bar chart
st.write("### Monthly Payment Breakdown")
monthly_payment_df = df[["Year", "Principal ($)", "Interest ($)"]].groupby(
    "Year").min()
st.bar_chart(monthly_payment_df, x_label="Year",
             y_label="Breakdown", height=400)

# Round values in the DataFrame
df["Payment ($)"] = df["Payment ($)"].round(0)
df["Principal ($)"] = df["Principal ($)"].round(0)
df["Interest ($)"] = df["Interest ($)"].round(0)
df["Remaining Balance ($)"] = df["Remaining Balance ($)"].round(0)
df["Penalty ($)"] = df["Penalty ($)"].round(0)

# Display repayment schedule
st.dataframe(df, use_container_width=True, hide_index=True, height=200)
