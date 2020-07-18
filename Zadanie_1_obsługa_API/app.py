# Zadanie 1 moduł 9

import csv
import requests
from flask import Flask, render_template, request

app = Flask(__name__)


def get_rates():
    response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
    return response.json()[0]['rates']


@app.route("/kantor/", methods=["GET", "POST"])
def kantor():
    data = get_rates()

    with open('datadump.csv', 'w', newline='') as csvfile:
        fieldnames = ['currency', 'code', 'bid', 'ask']
        writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=fieldnames)
        writer.writeheader()
        for item in data:
            writer.writerow(item)

    currency_codes = []
    for item in data:
        currency_codes.append(item['code'])

    message = ""

    if request.method == "POST":
        data_form = request.form
        amount = float(data_form.get('amount'))
        currency = data_form.get("currency")

        for item in data:
            if item['code'] == currency:
                bid_rate = float(item['bid'])
                # ask_rate = float(item['ask'])

        message = f"Total cost: {amount * bid_rate} PLN"

    return render_template("currency.html", codes=currency_codes, message=message)

app.run()