import requests
from bs4 import BeautifulSoup

url = "https://www.noticiasagricolas.com.br/cotacoes/cafe/cafe-cereja-descascado-mercado-fisico"

userAgent = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}


def money_coffe_requests():
    try:
        response = requests.get(url, headers=userAgent)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            table = soup.find("table", class_="cot-fisicas")
            tbody = table.find("tbody")
            rows = tbody.find_all("tr")
            coffee_prices = []
            for row in rows:
                cols = row.find_all("td")
                municipality = cols[0].text.strip()
                price = cols[1].text.strip()
                variation = cols[2].text.strip()
                no_thousands_str = price.replace(".", "")
                decimal_point_str = no_thousands_str.replace(",", ".")
                amount_float = float(decimal_point_str)
                coffee_prices.append(
                    {
                        "municipality": municipality,
                        "price": amount_float,
                        "price_br": price,
                        "variation": variation,
                    }
                )
            return coffee_prices, response.status_code

        else:
            return [
                {
                    "municipality": None,
                    "price": None,
                    "price_br": None,
                    "variation": None,
                }
            ], response.status_code
    except:
        return [
            {
                "municipality": None,
                "price": None,
                "price_br": None,
                "variation": None,
            }
        ], 0
