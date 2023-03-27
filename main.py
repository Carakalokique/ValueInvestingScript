import openpyxl
import requests
import csv
import json
import openpyxl

import apicalls
from apicalls import tickerincomestatement, tickerbalancesheet, tickercashflow, tickerstatistics, tickerprice, calculatingvalue



with open('TSX_tickers_test.csv') as csvfile:
    liststocktickers = csv.reader(csvfile, delimiter=' ', quotechar='|')
    line_count = 0

    # Create a new workbook
    workbook = openpyxl.Workbook()

    # Select the active worksheet
    worksheet = workbook.active


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
            tickerstatistics(row[0])
            ticker_statistics_dict = apicalls.tickerstatistics(row[0])
            tickerprice(row[0])
            ticker_realtime_price_dict = apicalls.tickerprice(row[0])
            calculatingvalue(incomestatement_dict, balancesheet_dict, cashflow_dict, ticker_statistics_dict, ticker_realtime_price_dict)
            print(row[0])
            line_count += 1

            # Write ticker to a cell
            worksheet[f'A{row}'] = row[0]
            # Write price to a cell
            worksheet[f'B{row}'] = 'Hello, world!'
            # Write earning_capacity_value_cyclic to a cell
            worksheet[f'C{row}'] = 'Hello, world!'
            # Write earning_capacity_value_growth to a cell
            worksheet[f'D{row}'] = 'Hello, world!'

    print(f'Processed {line_count} lines.')

# Save the workbook
workbook.save('Tickers with values.xlsx')

