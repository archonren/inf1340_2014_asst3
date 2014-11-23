#!/usr/bin/env python3

""" Docstring """

__author__ = 'Paul and Archon'
__email__ = "guanhua.ren@mail.utoronto.ca"

__copyright__ = "2014 Paul and Archon"
__license__ = "MIT License"

__status__ = "Prototype"

# imports one per line
import json
from datetime import *


stock_data = []
monthly_averages = []


def read_json_from_file(file_name):
    with open(file_name) as file_handle:
        file_contents = file_handle.read()
    return json.loads(file_contents)


def read_stock_data(stock_name, stock_file_name):
    stock_data_list = read_json_from_file(stock_file_name)
    date_list = []
    for day_stock_price_detail in stock_data_list:
        stock_date = datetime.strptime(day_stock_price_detail["Date"], "%Y-%m-%d")
        date_list.append(stock_date)
    date_list = sorted(date_list)
    year_range = []
    for year in range(date_list[0].year, date_list[-1].year+1):
        year_range.append(year)
  #find the range of year#
    year_dict = {}
    for year in year_range:
        year_dict[year] = [[], [], [], [], [], [], [], [], [], [], [], [], []]
    for day_stock_price_detail in stock_data_list:
        stock_date = datetime.strptime(day_stock_price_detail["Date"], "%Y-%m-%d")
        stock_month = stock_date.month
        stock_year = stock_date.year
        year_dict[stock_year][stock_month] = day_stock_price_detail
  #year_dict has key as year, and value as stock detail#






def six_best_months():
    return [('', 0.0), ('', 0.0), ('', 0.0), ('', 0.0), ('', 0.0), ('', 0.0)]


def six_worst_months():
    return [('', 0.0), ('', 0.0), ('', 0.0), ('', 0.0), ('', 0.0), ('', 0.0)]


read_stock_data("GOOG", "data/GOOG.json")