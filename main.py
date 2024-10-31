import streamlit as st
import math
import pandas as pd

st.title("Mortgage Repayment Calculator")

st.write("### Input Data")

col1, col2, col3 = st.columns(3)

loan_value = col1.number_input(
    "Loan Value ($)",
    min_value=100000,
    step=500,
)
interest_rate = col2.number_input(
    "Interest (%)",
    min_value=1.0,
    step=0.05,
)
loan_term = col3.number_input(
    "Term (Years)",
    min_value=5,
    max_value=35
)

monthly_interest_rate = (interest_rate / 100) / 12
number_of_payments = loan_term * 12
monthly_payment = (
    loan_value
    * (monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments)
    / ((1 + monthly_interest_rate) ** number_of_payments - 1)
)

total_payments = monthly_payment * number_of_payments
total_interest = total_payments - loan_value

# Create a dataframe with the repayment schedule
schedule = []
remaining_balance = loan_value
total_interest_24 = 0

for i in range(1, number_of_payments + 1):
    interest_payment = remaining_balance * monthly_interest_rate
    principal_payment = monthly_payment - interest_payment
    remaining_balance -= principal_payment
    year = math.ceil(i/12)
    schedule.append(
        [
            i,
            monthly_payment,
            principal_payment,
            interest_payment,
            remaining_balance,
            year
        ]
    )

    # Sum interest for the first 24 payments
    if i <= 24:
        total_interest_24 += interest_payment


st.write("### Repayment")
col1, col2, col3, col4 = st.columns(4)
col1.metric(label="Monthly", value=f"${monthly_payment:,.2f}")
col2.metric(label="Total", value=f"${total_payments:,.0f}")
col3.metric(label="Interest", value=f"${total_interest:,.0f}")
col4.metric(label="Interest (24 Months)", value=f"${total_interest_24:,.0f}")

df = pd.DataFrame(
    schedule,
    columns=["Month", "Payment", "Principal",
             "Interest", "Remaining Balance", "Year"]
)

st.write("### Loan Balance")
payments_df = df[["Year", "Remaining Balance"]].groupby("Year").min()
st.line_chart(payments_df)

st.write("### Monthly Payment Breakdown")
monthly_payment_df = df[["Year", "Principal",
                         "Interest"]].groupby("Year").min()
st.bar_chart(monthly_payment_df)
