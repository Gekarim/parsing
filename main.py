import requests
from bs4 import BeautifulSoup

def get_details_links(url): # cilka na diputata
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    table = soup.find('table', class_='table')
    deputy_tds = table.find_all('td')
    profile_links = []
    for td in deputy_tds:
        if td.find('a').get('href').startswith('/ru/deputy/show/') and td.find('a').get('href') not in profile_links:
            profile_links.append(td.find('a').get('href'))
    return profile_links

def parse_details(details_url): # information o diputate
    response = requests.get(details_url)
    soup = BeautifulSoup(response.text, 'lxml')
    name = soup.find('h3', class_ = 'deputy-name').text.strip()
    commitee_fraction = soup.find_all('h4', class_ = 'mb-10')
    commitee_fraction = list(map(lambda x: x.text.strip(), commitee_fraction))
    fraction, commitee = commitee_fraction
    return {'name': name, 'fraction': fraction, 'commitee': commitee}

    

def main(): # ccslka na sait
    site_url = 'http://kenesh.kg'
    list_url = site_url + '/ru/deputy/list/35'
    deputy_profiles_list = get_details_links(list_url)
    profiles_info_list = []
    for deputy in deputy_profiles_list:
        profiles_info_list.append(parse_details(site_url + deputy))
    print(profiles_info_list)


if __name__ == '__main__':
    main()