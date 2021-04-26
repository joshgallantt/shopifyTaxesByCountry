import requests
import json
import os

class order:
  def __init__(self, number = '', currency = '', amount = '', tax = '', country = ''):
    self.number = number
    self.currency = currency
    self.amount = amount
    self.tax = tax
    self.amount_after_tax = float(self.amount) - float(self.tax)
    self.country = country

  def __str__(self):
    return f"Order Number: {self.number} \nSales Price: {self.currency} {self.amount} \nTax: {self.tax} \nAfter Tax: {self.amount_after_tax} \nCountry: {self.country}\n"

  def __repr__(self):
    return str(self.number)

def clear_terminal():
    return os.system('cls' if os.name == 'nt' else 'clear')

def get_orders():

  list_of_orders = []

  response = requests.get(f'https://{username}:{password}@{shopify_store}/admin/orders.json?created_at_min={start_date}&created_at_max={end_date}')
  response_data = response.json()


  for i in response_data['orders']:
    create_order = order(number = i['order_number'], currency= i['currency'], amount = i['current_total_price'], tax = i['current_total_tax'], country = i['billing_address']['country'])
    list_of_orders.append(create_order)
  
  return list_of_orders

def sales_by_country(list_of_orders):

  country_list = []
  country_count = {}

  for order in list_of_orders:
    country_list.append(order.country)

  for country in set(country_list):
      country_count[country] = country_list.count(country)
      sales_by_country = dict(sorted(country_count.items(), key=lambda item: item[1], reverse = True))
    
  return sales_by_country

def report(list_of_orders, sales_by_country):

  number_of_sales = 0
  sales_total = 0
  tax_total = 0
  untaxed_profit = 0

  for order in list_of_orders:
    number_of_sales += 1
    sales_total += float(order.amount)
    tax_total += float(order.tax)
  
  clear_terminal()

  print("\n")
  print(f"Number of Sales: {number_of_sales} \nRevenue Before Taxes: {sales_total}\nTax Paid on UK Orders: {tax_total}\nUntaxed Profit on International Orders: {sales_total-tax_total}\n")
  print("Orders per country outside UK:\n")

  for k,v in sales_by_country.items():
    if 'United Kingdom' not in k:
      print(k,v)

  print("\n")

shopify_store = 'ENTER STORE URL HERE'
username = 'API KEY'
password = 'API PASS'
start_date = '2021-01-10'
end_date = '2021-03-30'

if __name__ == "__main__":
  list_of_orders = get_orders()
  sales_by_country = sales_by_country(list_of_orders)
  report(list_of_orders, sales_by_country)
else:
  list_of_orders = get_orders()
  sales_by_country = sales_by_country(list_of_orders)
