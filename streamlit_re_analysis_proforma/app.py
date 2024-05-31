import streamlit as st
import pandas as pd
import numpy as np
import numpy_financial as npf
import matplotlib.pyplot as plt

# Input values from the user
st.title("Real Estate Investment Analysis")

initial_market_value = st.number_input("Initial Market Value", value=300000)
purchase_price = st.number_input("Purchase Price", value=280000)
estimated_closing_costs = st.number_input("Estimated Closing Costs", value=5000)
downpayment_percentage = st.number_input("Downpayment Percentage (%)", value=20)
estimated_monthly_gross_rent = st.number_input("Estimated Monthly Gross Rent", value=2000)
property_taxes = st.number_input("Property Taxes", value=3000)
insurance_costs = st.number_input("Insurance Costs", value=1200)
loan_term = st.number_input("Loan Term (years)", value=30)
interest_rate = st.number_input("Interest Rate (%)", value=3.5)
appreciation_rate = st.number_input("Appreciation Rate (%)", value=2)
vacancy_rate = st.number_input("Vacancy Rate (%)", value=5)
management_fees = st.number_input("Management Fees (%)", value=10)
maintenance_percentage = st.number_input("Maintenance Percentage (%)", value=1)
rental_income_increase = st.number_input("Rental Income Increase (%)", value=2)

# Calculations
downpayment_dollars = (downpayment_percentage / 100) * purchase_price
initial_cash_invested = downpayment_dollars + estimated_closing_costs
annual_gross_rent = estimated_monthly_gross_rent * 12
vacancy_losses = (vacancy_rate / 100) * annual_gross_rent
property_taxes_dollars = property_taxes
insurance_costs_dollars = insurance_costs
management_fees_dollars = (management_fees / 100) * annual_gross_rent
maintenance_fees_dollars = (maintenance_percentage / 100) * initial_market_value
total_operating_expenses = vacancy_losses + property_taxes_dollars + insurance_costs_dollars + management_fees_dollars + maintenance_fees_dollars

# Mortgage Calculation
loan_amount = purchase_price - downpayment_dollars
monthly_interest_rate = (interest_rate / 100) / 12
num_payments = loan_term * 12
monthly_mortgage_payment = npf.pmt(monthly_interest_rate, num_payments, -loan_amount)
annual_mortgage_payment = monthly_mortgage_payment * 12

# Cash Flow Calculation
cash_flow = annual_gross_rent - total_operating_expenses - annual_mortgage_payment

# Gross Equity Income Calculation
annual_appreciation = (appreciation_rate / 100) * initial_market_value
gross_equity_income = annual_appreciation + (annual_mortgage_payment - loan_amount * monthly_interest_rate * 12)

# GEI with Tax Savings (simplified)
tax_savings = annual_mortgage_payment * 0.3  # Assuming 30% tax bracket
gei_with_tax_savings = gross_equity_income + tax_savings

# Display Results
st.header("Investment Analysis Results")
st.write(f"Downpayment in Dollars: ${downpayment_dollars:,.2f}")
st.write(f"Initial Cash Invested: ${initial_cash_invested:,.2f}")
st.write(f"Annual Gross Rent: ${annual_gross_rent:,.2f}")
st.write(f"Vacancy Losses: ${vacancy_losses:,.2f}")
st.write(f"Property Taxes: ${property_taxes_dollars:,.2f}")
st.write(f"Insurance Costs: ${insurance_costs_dollars:,.2f}")
st.write(f"Management Fees: ${management_fees_dollars:,.2f}")
st.write(f"Maintenance Fees: ${maintenance_fees_dollars:,.2f}")
st.write(f"Total Operating Expenses: ${total_operating_expenses:,.2f}")
st.write(f"Annual Mortgage Payment: ${annual_mortgage_payment:,.2f}")
st.write(f"Cash Flow: ${cash_flow:,.2f}")
st.write(f"Gross Equity Income: ${gross_equity_income:,.2f}")
st.write(f"GEI with Tax Savings: ${gei_with_tax_savings:,.2f}")

# 30-Year Projections
years = np.arange(1, 31)
cash_flows = []
equity_accumulation = []
current_rent = estimated_monthly_gross_rent * 12
current_market_value = initial_market_value

for year in years:
    current_rent *= (1 + rental_income_increase / 100)
    annual_gross_rent = current_rent
    vacancy_losses = (vacancy_rate / 100) * annual_gross_rent
    management_fees_dollars = (management_fees / 100) * annual_gross_rent
    total_operating_expenses = vacancy_losses + property_taxes_dollars + insurance_costs_dollars + management_fees_dollars + maintenance_fees_dollars
    cash_flow = annual_gross_rent - total_operating_expenses - annual_mortgage_payment
    cash_flows.append(cash_flow)

    current_market_value *= (1 + appreciation_rate / 100)
    annual_appreciation = current_market_value * (appreciation_rate / 100)
    equity_accumulation.append(annual_appreciation + (annual_mortgage_payment - loan_amount * monthly_interest_rate * 12))

# Plotting
st.header("30-Year Cash Flow and Equity Projections")
fig, ax = plt.subplots()
ax.plot(years, cash_flows, label='Annual Cash Flow')
ax.plot(years, equity_accumulation, label='Equity Accumulation')
ax.set_xlabel('Year')
ax.set_ylabel('Amount ($)')
ax.legend()
st.pyplot(fig)

st.header("30-Year Annual Cash Flow Projections")
fig, ax = plt.subplots()
ax.plot(years, cash_flows, label='Annual Cash Flow')
ax.set_xlabel('Year')
ax.set_ylabel('Cash Flow ($)')
ax.legend()
st.pyplot(fig)

st.header("30-Year Equity Accumulation Projections")
fig, ax = plt.subplots()
ax.plot(years, equity_accumulation, label='Equity Accumulation')
ax.set_xlabel('Year')
ax.set_ylabel('Equity Accumulation ($)')
ax.legend()
st.pyplot(fig)
