import requests
from bs4 import BeautifulSoup
import csv

# Plan:
# 1. stranitsi
# 2. url na stratitsi
# 3. sobrat dannie

def get_html(url):
    r = requests.get(url)
    return r.text


def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')

    pages = soup.find('div', class_='pager-wrap').find('li', class_= 'active').find('a').get('href')
    total_pages = pages.split('=')[1]
    return int(total_pages)



def write_csv(data):
    with open('kivano.csv', 'a') as f:
        writer = csv.writer(f)

        writer.writerow( (data['title'],
                          data['price'],
                          data['photo'],
                          data['url']) )
    
    

def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find('div', class_= 'list-view').find_all('div', class_= 'item product_listbox oh')
    for ad in ads:
        # title, url, price, photo
        try:
            title = ad.find('div', class_= 'listbox_title oh').find('a').text
        except:
            title = ''
        try:
            url = 'https://www.kivano.kg' + ad.find('div', class_= 'listbox_title oh').find('a').get('href')
        except:
            url = ''
        try:
            price = ad.find('div', class_= 'listbox_price text-center').text.strip()
        except:
            price = ''
        try:
            photo = 'https://www.kivano.kg' + ad.find('div', class_= 'listbox_img pull-left').find('a').get('href')
        except:
            photo = ''

        data = {'title': title,
                    'price': price,
                    'photo': photo,
                    'url': url}

        write_csv(data)
    

def main():
    url = 'https://www.kivano.kg/mobilnye-telefony?page=20'
    base_url = 'https://www.kivano.kg/mobilnye-telefony?'
    page_part = 'p='

    total_pages = get_total_pages(get_html(url))

    for i in range(1, total_pages + 1):
        url_gen = base_url + page_part + str(i)
        # print(url_gen)
        html = get_html(url_gen)
        get_page_data(html)





if __name__ == '__main__':
    main()
