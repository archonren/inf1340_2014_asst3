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
from decimal import *
from operator import itemgetter


def read_json_from_file(file_name):
    # open and read json files#
    with open(file_name) as file_handle:
        file_contents = file_handle.read()
    return json.loads(file_contents)

global avg_price
avg_price = []


def read_stock_data(stock_name, stock_file_name):
    """
    calculate the average price for given stock per month

    :param stock_name: The name of a stock.
    :param stock_file_name: The name of a JSON formatted file that contains stock information.
    :return: List of tuples.tuple contains year/month and the average price.
    """
    stock_data_list = read_json_from_file(stock_file_name)
    year_dict = {}
    global avg_price
    avg_price = []
    stock_data_list = clear_incomplete_month(stock_data_list)
    for day_stock_price_detail in stock_data_list:
        stock_date = datetime.strptime(day_stock_price_detail["Date"], "%Y-%m-%d")
        day_stock_price_detail["Date"] = str(stock_date.year)+"/"+str(stock_date.month).zfill(2)
        year_dict.setdefault(day_stock_price_detail["Date"], [0, 0])
  #fix the date, delete the day, only leave the year and month and set up space for sales and volume#
    for day_stock_price_detail in stock_data_list:
        year_dict[day_stock_price_detail["Date"]][0] += day_stock_price_detail["Close"]*day_stock_price_detail["Volume"]
        year_dict[day_stock_price_detail["Date"]][1] += day_stock_price_detail["Volume"]
  #year_dict has key as year/month, and value as stock detail (0 element as sales and 1 element as volume)#
    for key_time in year_dict:
        price = year_dict[key_time][0]/year_dict[key_time][1]
        price = Decimal(price).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
        avg_price.append((key_time, float(price)))


def clear_incomplete_month(stock_data_list):
    """
    remove months that are not start from the first week or does not end at the last week from stock data

    :param stock_data_list: the stock data
    :return: List of stock data that across a whole month
    """
    delete_list = []
    stock_month_start_from_beginning = []
    stock_month_end_properly = []
    for day_stock_price_detail in stock_data_list:
        stock_date = datetime.strptime(day_stock_price_detail["Date"], "%Y-%m-%d")
        if (stock_date - timedelta(days=7)).month != stock_date.month:
            stock_month_start_from_beginning.append(str(stock_date.year)+"/"+str(stock_date.month).zfill(2))
    stock_month_start_from_beginning = list(set(stock_month_start_from_beginning))
    #find the month that start from the first week#
    for day_stock_price_detail in stock_data_list:
        stock_date = datetime.strptime(day_stock_price_detail["Date"], "%Y-%m-%d")
        if (stock_date + timedelta(days=7)).month != stock_date.month:
            stock_month_end_properly.append(str(stock_date.year)+"/"+str(stock_date.month).zfill(2))
    stock_month_end_properly = list(set(stock_month_end_properly))
    #find the month that end at the last week#
    stock_year_month = set(stock_month_end_properly).intersection(set(stock_month_start_from_beginning))
    for day_stock_price_detail in stock_data_list:
        stock_date = datetime.strptime(day_stock_price_detail["Date"], "%Y-%m-%d")
        if str(stock_date.year)+"/"+str(stock_date.month).zfill(2) not in stock_year_month:
            delete_list.append(day_stock_price_detail)
    for key in delete_list:
        stock_data_list.remove(key)
    return stock_data_list


def six_best_months():
    """
    find the six best months

    :return: List of tuples.tuple contains the six best average price and year/month.
    """
    global avg_price
    list.sort(avg_price, key=itemgetter(1), reverse=True)
    return avg_price[:6]


def six_worst_months():
    """
    find the six worst months

    :return: List of tuples.tuple contains the six worst average price and year/month.
    """
    global avg_price
    list.sort(avg_price, key=itemgetter(1))
    return avg_price[:6]