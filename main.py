import sys

import yaml
import unittest


def calculate_tax(income: int, selected_country_year: str) -> float:
    with open('config.yaml') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    # print("Please enter the abbreviated name of the country for which you want to know the tax bracket and the year. "
    #       "Example: tr2022, uk2022, tr2021")
    # selected_country_year = input()
    # print("Please enter your salary")
    # salary = int(input())
    tax_rates = []

    for tax_year in config:
        if tax_year == selected_country_year:

            for tax_rate_money in config[tax_year]:
                if tax_rate_money == "None":
                    tax_rates.append((None, config[tax_year][tax_rate_money]))
                    continue
                tax_rates.append((tax_rate_money, config[tax_year][tax_rate_money]))

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
