import requests
from bs4 import BeautifulSoup
url = "https://www.noticiasagricolas.com.br/cotacoes/cafe/cafe-cereja-descascado-mercado-fisico"

userAgent = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

def money_coffe_requests():
    response = requests.get(url, headers=userAgent)

    if response.status_code == 200:
        #Search for data in the HTML
        """
        <div class="cotacao">
            <div class="info">
                            <div class="fechamento">Fechamento: 01/12/2025</div>
                </div>
            <div class="table-content">
                <table class="cot-fisicas">
                <thead>
                    <tr>
                                <th>Município</th>
                                <th>Preço (R$/Sc de 60 kg)</th>
                                <th>Variação (%)</th>
                            </tr>
                </thead>
                <tbody>
                                        <tr>
                                        <td>Guaxupé/MG (Cooxupé)</td>
                                        <td>2.323,00</td>
                                        <td>-0,85</td>
                                    </tr>
                                <tr>
                                        <td>Poços de Caldas/MG (CaféPoços)</td>
                                        <td>2.640,00</td>
                                        <td>-0,38</td>
                                    </tr>
                                <tr>
                                        <td>Patrocínio/MG (Expocaccer)</td>
                                        <td>2.390,00</td>
                                        <td>+0,63</td>
                                    </tr>
                                <tr>
                                        <td>Varginha/MG (Minasul)</td>
                                        <td>2.400,00</td>
                                        <td>0,00</td>
                                    </tr>
                                <tr>
                                        <td>Campos Gerais/MG (Coopercam)</td>
                                        <td>2.355,00</td>
                                        <td>-1,26</td>
                                    </tr>
                                    </tbody>
                    </table>
            </div>
            </div>
        """
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
            no_thousands_str = price.replace('.', '')
            decimal_point_str = no_thousands_str.replace(',', '.')
            amount_float = float(decimal_point_str)
            coffee_prices.append({
                "municipality": municipality,
                "price": amount_float,
                "price_br": price,
                "variation": variation
            })
        return coffee_prices, response.status_code
        
    else:
        return None, response.status_code