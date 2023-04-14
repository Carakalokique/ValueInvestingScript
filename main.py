import openpyxl
import requests
import csv
import json
import openpyxl
import time

import apicalls
from apicalls import tickerincomestatement, tickerbalancesheet, tickercashflow, tickerstatistics, tickerprice, \
    calculatingvalue



with open('TSX_tickers_test.csv') as csvfile:
    liststocktickers = csv.reader(csvfile, delimiter=' ', quotechar='|')
    line_count = 0

    # Create a new workbook
    workbook = openpyxl.Workbook()

    # Select the active worksheet
    worksheet = workbook.active

    # Write ticker to a cell
    worksheet[f'A1'] = 'Ticker Name'
    # Write price to a cell
    worksheet[f'B1'] = 'Current Price'
    # Write earning_capacity_value_cyclic to a cell
    worksheet[f'C1'] = 'Earning Capacity Value Cyclic'
    # Write earning_capacity_value_growth to a cell
    worksheet[f'E1'] = 'Earning Capacity Value Growth'


    for row in liststocktickers:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            # time.sleep(35)
            # Get the data from API calls from the functions in apicalls.py
            incomestatement_dict = apicalls.tickerincomestatement(row[0])
            if not incomestatement_dict["income_statement"] or incomestatement_dict["income_statement"][0]["sales"] is None or incomestatement_dict["income_statement"][0]["sales"] <= 0:
                continue
            else:
                balancesheet_dict = apicalls.tickerbalancesheet(row[0])
                cashflow_dict = apicalls.tickercashflow(row[0])
                ticker_statistics_dict = apicalls.tickerstatistics(row[0])
                ticker_price_dict = apicalls.tickerprice(row[0])

                current_price, earning_capacity_value_cyclic, earning_capacity_value_growth = calculatingvalue(incomestatement_dict, balancesheet_dict, cashflow_dict, ticker_statistics_dict, ticker_price_dict)

                if float(current_price) < earning_capacity_value_cyclic:
                    buy_cyclic = "BUY"
                else:
                    buy_cyclic = "NO"
                if float(current_price) < earning_capacity_value_growth:
                    buy_growth = "BUY"
                else:
                    buy_growth = "NO"


                print(row[0])
                line_count += 1

                # Write ticker to a cell
                worksheet[f'A{line_count}'] = row[0]
                # Write price to a cell
                worksheet[f'B{line_count}'] = float(current_price)
                # Write earning_capacity_value_cyclic to a cell
                worksheet[f'C{line_count}'] = earning_capacity_value_cyclic
                worksheet[f'D{line_count}'] = buy_cyclic
                # Write earning_capacity_value_growth to a cell
                worksheet[f'E{line_count}'] = earning_capacity_value_growth
                worksheet[f'F{line_count}'] = buy_growth


    print(f'Processed {line_count} lines.')

# Save the workbook
workbook.save('Tickers with values.xlsx')

