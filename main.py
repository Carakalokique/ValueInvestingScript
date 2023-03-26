import requests
import csv
import json

import apicalls
from apicalls import tickerincomestatement, tickerbalancesheet, tickercashflow, calculatingvalue


with open('nasdaq_screener_1678251144777.csv') as csvfile:
    liststocktickers = csv.reader(csvfile, delimiter=' ', quotechar='|')
    line_count = 0
    for row in liststocktickers:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            # Get the data from API calls from the function in apicalls.py
            tickerincomestatement(row[0])
            incomestatement_dict = apicalls.tickerincomestatement(row[0])
            tickerbalancesheet(row[0])
            balancesheet_dict = apicalls.tickerbalancesheet(row[0])
            tickercashflow(row[0])
            cashflow_dict = apicalls.tickercashflow(row[0])
            calculatingvalue(incomestatement_dict, balancesheet_dict, cashflow_dict)
            print(row[0])
            line_count += 1

    print(f'Processed {line_count} lines.')

