from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests
from bs4 import BeautifulSoup
import time
from fake_useragent import UserAgent

app = Flask(__name__)

def flipkart_scrape(query):
    url = f'https://www.flipkart.com/search?q={query.replace(" ", "+")}'
    # Generate a random User-Agent
    user_agent = UserAgent().random
    headers = {
        'User-Agent': user_agent,
        'Referer': 'https://www.flipkart.com/'  # Add a Referer header if needed
    }
    
    max_retries = 3
    max_delay_sec = 2

    for attempt in range(max_retries):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            try:
                datas = soup.find_all('div', class_='_4ddWXP')
            except:
                datas = []

            if len(datas) > 0:
                products = []
                for item in datas:
                    try:
                        image = item.find('img', class_='_396cs4')['src']
                    except:
                        image = "url_for('static', filename='img/404_img.jpg')"

                    try:
                        title_element = item.find('a', class_='s1Q9rs')
                        title = (title_element.text.strip()[:12] + '...') if len(title_element.text.strip()) > 12 else title_element.text.strip()

                    except:
                        title = "No Title Found"

                    try:
                        link_raw = item.find('a', class_='s1Q9rs')['href']
                        link = f"https://www.flipkart.com{link_raw}"
                    except:
                        link = "#"

                    try:
                        price = item.find('div', class_='_30jeq3').text.strip()
                    except:
                        price = "Not Found"

                    products.append({
                        'image': image,
                        'title': title,
                        'link': link,
                        'price': price
                    })

                return products  # Return the processed product list
            else:
                print("Nothing Found")

            return []  # Return an empty list if no data is found
        elif response.status_code == 503:
            print(f"Got 503 Error. Retrying ({attempt+1}/{max_retries})...")
            time.sleep(max_delay_sec)
        else:
            print(f"Failed with status code {response.status_code}. Exiting.")
            break

    print(f"Failed after {max_retries} attempts.")
    return None

# run function 
# query = "keyboard"
# result = flipkart_scrape(query)
# print(result)


# home page 
@app.route("/")
def home_page():
    return render_template("index.html")

# on search request 
@app.route("/s", methods=["POST"])
def search():
    if request.method == "POST":
        query = request.form["query_is"]
        result = flipkart_scrape(query)
        return render_template("result.html", data=result)



# run Environment
if __name__ == "__main__":
    app.run(debug=True)