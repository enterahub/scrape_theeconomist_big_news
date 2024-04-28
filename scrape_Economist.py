import json
import datetime
from bs4 import BeautifulSoup
import requests
from fake_headers import Headers

base_url = "https://www.economist.com"
ua = Headers()
date = datetime.date.today()

def scrape_page():
    f_header = ua.generate()
    html_request = requests.get(base_url, headers=f_header)

    if html_request.status_code == 200:
        soup = BeautifulSoup(html_request.text, 'html.parser')
        news_list = soup.find_all('h3')
        news_dict = {}

        for news in news_list:
            a_tag = news.find('a')
            if a_tag and 'href' in a_tag.attrs:
                href = a_tag['href']
                page_url = base_url + href if href.startswith('/') else href

                news_title = news.get_text(strip=True)

                try:
                    news_description = news.find_next_sibling('p').text.strip()
                except AttributeError:
                    news_description = None

                news_dict[news_title] = {"URL": page_url, "Description": news_description}

        return news_dict
    else:
        return f"Failed to retrieve the webpage(Status Code: {html_request.status_code})"


news_info = scrape_page()
with open(f'{date}_the_economist_heading_news.json', 'w+') as f:
    json.dump(news_info, fp=f, indent=4, ensure_ascii=False)

print(news_info)
