import csv
import requests
from bs4 import BeautifulSoup
from email_scraper import scrape_emails


HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    'accept': '*/*'
}

def get_html(url,params=None):
    r = requests.get(url,headers= HEADERS, params=params)
    return r.text

def get_all_links(html):
    soup = BeautifulSoup(html,'html.parser')
    ds = soup.find('div',class_="list-view").find_all('a', class_="tender-item__name tender-item__name--padded")
    links = []
    for d in ds:
        a = d.get('href')
        link = 'https://energybase.ru'+ a
        links.append(link)
    return links
    # print(links)

def email(string):     
    r = int(string[:2], 16)     
    email = ''.join([chr(int(string[i:i+2], 16) ^ r)                      
    for i in range(2, len(string), 2)])     
    return email   

def get_page_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        name_c = soup.find('h5',).text
        # name_c = soup.find('h5',)


    except:
        print('No name company')
    try: 
        contact = soup.find('section', id="contact-person").get_text(separator=' ')
        email = soup.find('a', {"class": "__cf_email__"})["data-cfemail"]
        r = int(email[:2],16)
        email= ''.join([chr(int(email[i:i+2], 16) ^ r) for i in range(2, len(email), 2)])
        # return e
    except:
        contact = 'No contact'
        email= 'No contact'
        # e = 'no em'
    # data = {'name_c':name_c,'contact':contact,}
    # return data
    print(name_c)
    print(contact)
    print('Электонная почта '+ email)

    


# def write_csv(data):
#     with open('deputy.csv','a') as file:
#         writer = csv.writer(file)
#         writer.writerow((data['name_c'],data['contact'],))
#         print(data['name_c'],data['contact'],'parsed')

def main():
    new_links = []
    url = 'https://energybase.ru/tender/catalog/heat-exchangers?page=1'
    all_links =get_all_links(get_html(url))
    for url in all_links:
        # html = get_html(url)
        # data = get_page_content(html)
        inf = get_page_content(get_html(url))
        # write_csv(data)
        # new_links.append(i)
    # print(new_links)
    

if __name__ == '__main__':
    main()