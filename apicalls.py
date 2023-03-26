import requests
import json

def tickerincomestatement (ticker):
    # GET INCOME STATEMENT DATA
    stockincomestatement = requests.get(
        f'https://api.twelvedata.com/income_statement?symbol={ticker}&apikey=01ac55e20e6e49f6bcb340d2d8600558')
    # Transform API call response to string
    stockincomestatement_string = stockincomestatement.text

    # Makes the JSON response from API call look pretty in terminal
    incomestatement_dict = json.loads(stockincomestatement_string)
    pretty_incomestatement = json.dumps(incomestatement_dict, indent=4)
    # print(pretty_incomestatement)
    return incomestatement_dict

def tickerbalancesheet (ticker):
    # GET BALANCE SHEET DATA
    stockbalancesheet = requests.get(
        f'https://api.twelvedata.com/balance_sheet?symbol={ticker}&apikey=01ac55e20e6e49f6bcb340d2d8600558')
    # Transform API call response to string
    stockbalancesheet_string = stockbalancesheet.text

    # Makes the JSON response from API call look pretty in terminal
    balancesheet_dict = json.loads(stockbalancesheet_string)
    pretty_balancesheet = json.dumps(balancesheet_dict, indent=4)
    # print(pretty_balancesheet)
    return balancesheet_dict

def tickercashflow (ticker):
    # GET CASH FLOW DATA
    stockcashflow = requests.get(
        f'https://api.twelvedata.com/cash_flow?symbol={ticker}&apikey=01ac55e20e6e49f6bcb340d2d8600558')
    # Transform API call response to string
    stockcashflow_string = stockcashflow.text

    # Makes the JSON response from API call look pretty in terminal
    cashflow_dict = json.loads(stockcashflow_string)
    pretty_cashflow = json.dumps(cashflow_dict, indent=4)
    # print(pretty_cashflow)
    return cashflow_dict


def calculatingvalue (incomestatement_dict, balancesheet_dict, cashflow_dict):

    year_dict = {}
    revenue_dict = {}
    spendingincome_dict = {}
    depreciation_dict = {}
    accruedexpenses_dict = {}
    provisionsforrisksandcharges_dict = {}
    addition_dict = {}
    operatingcashflow_dict = {}
    grosstotalinvestment_dict = {}
    revenuetoinvestmentrate_dict = {}

    for i in range(0, len(incomestatement_dict["income_statement"])):
        year_dict[f'year{i + 1}'] = incomestatement_dict["income_statement"][i]["fiscal_date"][:4]
        print('Year:', year_dict[f'year{i + 1}'])

        revenue_dict[f'revenue{i+1}'] = incomestatement_dict["income_statement"][i]["sales"]
        print("Revenue:", revenue_dict[f'revenue{i+1}'])


        spendingincome_dict[f'spendingincome{i+1}'] = incomestatement_dict["income_statement"][i]["operating_income"]
        print("Spending income:", spendingincome_dict[f'spendingincome{i+1}'])


        depreciation_dict[f'depreciation{i+1}'] = cashflow_dict["cash_flow"][i]["operating_activities"]["depreciation"]
        depreciation_dict[f'depreciation{i+1}'] = 0 if depreciation_dict[f'depreciation{i+1}'] is None else depreciation_dict[f'depreciation{i+1}']
        print("Depreciation:", depreciation_dict[f'depreciation{i+1}'])


        accruedexpenses_dict[f'accruedexpenses{i+1}'] = balancesheet_dict["balance_sheet"][i]["liabilities"]["current_liabilities"]["accrued_expenses"]
        accruedexpenses_dict[f'accruedexpenses{i+1}'] = 0 if accruedexpenses_dict[f'accruedexpenses{i+1}'] is None else accruedexpenses_dict[f'accruedexpenses{i+1}']
        print("accrued expenses:", accruedexpenses_dict[f'accruedexpenses{i+1}'])


        provisionsforrisksandcharges_dict[f'provisionsforrisksandcharges{i+1}'] = balancesheet_dict["balance_sheet"][i]["liabilities"]["non_current_liabilities"]["provision_for_risks_and_charges"]
        provisionsforrisksandcharges_dict[f'provisionsforrisksandcharges{i+1}'] = 0 if provisionsforrisksandcharges_dict[f'provisionsforrisksandcharges{i+1}'] is None else provisionsforrisksandcharges_dict[f'provisionsforrisksandcharges{i+1}']

        print("provisions for risks and charges:", provisionsforrisksandcharges_dict[f'provisionsforrisksandcharges{i+1}'])

        addition_dict[f'addition{i+1}'] = spendingincome_dict[f'spendingincome{i+1}'] + depreciation_dict[f'depreciation{i+1}'] + accruedexpenses_dict[f'accruedexpenses{i+1}'] + provisionsforrisksandcharges_dict[f'provisionsforrisksandcharges{i+1}']
        print(addition_dict[f'addition{i+1}'])

        theoreticaltaxrate = 0.3

        operatingcashflow_dict[f'operatingcashflow{i+1}'] = addition_dict[f'addition{i+1}'] * (1 - theoreticaltaxrate)
        print("Operating cash flow:", operatingcashflow_dict[f'operatingcashflow{i+1}'])

        grosstotalinvestment_dict[f'grosstotalinvestment{i+1}'] = depreciation_dict[f'depreciation{i+1}'] + accruedexpenses_dict[f'accruedexpenses{i+1}'] + provisionsforrisksandcharges_dict[f'provisionsforrisksandcharges{i+1}']
        print("Gross total investment:", grosstotalinvestment_dict[f'grosstotalinvestment{i+1}'])

        if grosstotalinvestment_dict[f'grosstotalinvestment{i+1}'] == 0:
            revenuetoinvestmentrate_dict[f'revenuetoinvestmentrate{i+1}'] = 0
        else:
            revenuetoinvestmentrate_dict[f'revenuetoinvestmentrate{i+1}'] = revenue_dict[f'revenue{i+1}'] / grosstotalinvestment_dict[f'grosstotalinvestment{i+1}']
        print('Revenue to investment rate:', revenuetoinvestmentrate_dict[f'revenuetoinvestmentrate{i+1}'])

    revenue_growth_yoy_dict = {}
    for i in range(1, len(year_dict)):
        revenue_growth_yoy_dict[f'revenue_growth_yoy{i+1}'] = revenue_dict[f'revenue{i}'] - revenue_dict[f'revenue{i + 1}']
        print('Revenue Growth YoY', revenue_growth_yoy_dict[f'revenue_growth_yoy{i+1}'])

    ratio_average = sum(revenuetoinvestmentrate_dict.values()) / len(revenuetoinvestmentrate_dict)
    print('Ratio Average:', ratio_average)