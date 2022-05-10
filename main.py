import sys

import yaml
import unittest
import pandas as pd
import matplotlib.pyplot as plt
import numpy


def calculate_tax(income: int, selected_country_year: str) -> float:
    with open('config.yaml') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    # print("Please enter the abbreviated name of the country for which you want to know the tax bracket and the year. "
    #       "Example: tr2022, uk2022, tr2021")
    # selected_country_year = input()
    # print("Please enter your salary")
    # salary = int(input())
    tax_rates = []
    # print(config)
    # for tax_year in config:
    #     if tax_year == selected_country_year:
    #
    #         for tax_rate_money in config[tax_year]:
    #             if tax_rate_money == "None":
    #                 tax_rates.append((None, config[tax_year][tax_rate_money]))
    #                 continue
    #             tax_rates.append((tax_rate_money, config[tax_year][tax_rate_money]))

    if config[selected_country_year]:
        tax_rates = config[selected_country_year]
        for index, rates in enumerate(tax_rates):
            for value in rates:
                if value == "None":
                    tax_rates[index][0] = None
    else:
        raise Exception("tr2021 or tr2022 or uk2022 available")

    tax = 0
    band = 0
    income_remaining = income
    while income_remaining > 0:
        limit = tax_rates[band][0] or sys.maxsize
        prev_limit = tax_rates[band - 1][0] if band > 0 else 0
        band_amount = limit - prev_limit
        tax_rate = tax_rates[band][1]
        band_taxable_amount = min(income_remaining, band_amount)
        band_tax = band_taxable_amount * tax_rate
        tax += band_tax
        income_remaining -= band_taxable_amount
        # print(band, tax_rate, limit, prev_limit, band_amount, band_taxable_amount, band_tax, tax)
        band += 1
    return tax


# income = 500000
# year_country = "tr2022"
# print(f"tax: {calculate_tax(income=income, selected_country_year=year_country)}")

def plot_country(selected_country_year: str, zero_to_where: int):
    results = []
    values = list(range(0, zero_to_where, 250))

    for i in values:
        results.append(calculate_tax(i, selected_country_year))
        print(results[:-1])

    plt.plot(values, results, label='money-tax')
    plt.autoscale(tight=True)
    plt.title(selected_country_year)
    plt.legend(loc=0)
    plt.ylabel('Tax')
    plt.xlabel('Money')
    plt.ticklabel_format(style='plain')

    plt.show()


plot_country("uk2022", 1200000)


def plot_all(zero_to_where: int):
    values = list(range(0, zero_to_where, 250))

    results_uk2022 = []
    for i in values:
        results_uk2022.append(calculate_tax(i, "uk2022"))
    print("1/3 finish")

    results_tr2021 = []
    for i in values:
        results_tr2021.append(calculate_tax(i, "tr2021"))
    print("2/3 finish")

    results_tr2022 = []
    for i in values:
        results_tr2022.append(calculate_tax(i, "tr2022"))
    print("3/3 finish")

    plt.plot(values, results_uk2022, label="uk2022")
    plt.plot(values, results_tr2021, label="tr2021")
    plt.plot(values, results_tr2022, label="tr2022")
    plt.autoscale(tight=True)
    plt.title("TAX-MONEY")
    plt.legend(loc=0)
    plt.ylabel('Tax')
    plt.xlabel('Money')
    plt.ticklabel_format(style='plain')

    plt.show()


plot_all(1200000)


class TestStringMethods(unittest.TestCase):

    def test_equal_2022(self):
        self.assertEqual(calculate_tax(500000, "tr2022"), 148500)
        self.assertEqual(calculate_tax(190000, "tr2021"), 46390.0)
        self.assertEqual(calculate_tax(50270, "uk2022"), 7540.0)
        self.assertEqual(calculate_tax(0, "uk2022"), 0)
        self.assertEqual(calculate_tax(0, "tr2022"), 0)
        self.assertEqual(calculate_tax(0, "tr2021"), 0)
        self.assertEqual(calculate_tax(1000000, "tr2022"), 329500)
        self.assertEqual(calculate_tax(1000000, "tr2022"), 329500)
