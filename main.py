import sys

import yaml
import unittest

with open('config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

print("Please enter the abbreviated name of the country for which you want to know the tax bracket and the year. "
      "Example: tr2022, uk2022, tr2021")
selected_country_year = input()
print("Please enter your salary")
salary = int(input())
tax_rates = []

for tax_year in config:

    if str(tax_year) == selected_country_year:

        for tax_rate_money in config[tax_year]:
            if tax_rate_money == "None":
                tax_rates.append((None, config[tax_year][tax_rate_money]))
                continue
            tax_rates.append((tax_rate_money, config[tax_year][tax_rate_money]))


def calculate_tax(income: int, tax_table):
    tax_rates = tax_table
    print(tax_rates)
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
        print(band, tax_rate, limit, prev_limit, band_amount, band_taxable_amount, band_tax, tax)
        band += 1
    return tax


#
print(f"tax: {calculate_tax(income=salary, tax_table=tax_rates)}")


class TestStringMethods(unittest.TestCase):



    def test_equal_2022(self):
        tr2022 = [(32000, 0.15), (70000, 0.2), (250000, 0.27), (880000, 0.35), (None, 0.4)]
        tr2021 = [(24000, 0.15), (53000, 0.2), (190000, 0.27), (650000, 0.35), (None, 0.4)]
        uk2022 = [(12570, 0.0), (50270, 0.2), (150000, 0.4), (None, 0.45)]

        self.assertEqual(calculate_tax(salary, tr2022), 89000.0)
        # self.assertEqual(calculate_tax(salary, uk2022), 89000.0)

    def test_equal_2021(self):
        tr2021 = [(24000, 0.15), (53000, 0.2), (190000, 0.27), (650000, 0.35), (None, 0.4)]

        self.assertEqual(calculate_tax(53000, tr2021), 9400.0)

