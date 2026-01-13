import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

def find_vessel_url(url):
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=30)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        vessel_links = []
        for link in soup.find_all('a', href=re.compile(r'/vessels/details/')):
            href = link['href']
            full_url = f"https://www.vesselfinder.com{href}" if href.startswith('/') else href
            vessel_links.append(full_url)
        
        if len(vessel_links) == 1:
            return vessel_links[0]
        if '/vessels/details/' in response.url:
            return response.url
        
        return None
    except:
        return None

def extract_vessel_info(vessel_url):
    try:
        r = requests.get(vessel_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=30)

        imo = re.search(r'vu_imo=(\d{7})', r.text)
        mmsi = re.search(r'MMSI=(\d{9})', r.text)
        
        soup = BeautifulSoup(r.text, 'html.parser')
        name = soup.find('h1').text.strip() if soup.find('h1') else 'unknown'

        vtype = 'unknown'
        for td in soup.find_all('td', class_='n3'):
            if 'AIS тип' in td.text:
                next_td = td.find_next('td', class_='v3')
                if next_td:
                    vtype = next_td.text.strip()
                    break
        
        return {
            'Название': name,
            'IMO': imo.group(1) if imo else 'unknown',
            'MMSI': mmsi.group(1) if mmsi else 'unknown',
            'Тип': vtype
        }
    except:
        return {k: 'unknown' for k in ['Название', 'IMO', 'MMSI', 'Тип']}

def main():
    links = pd.read_excel('Links.xlsx')['Ссылка'].dropna().tolist()
    results = []
    
    for i, link in enumerate(links, 1):
        print(f"{i}/{len(links)}")
        
        if url := find_vessel_url(link):
            results.append(extract_vessel_info(url))
    
    if results:
        pd.DataFrame(results).to_excel('result.xlsx', index=False)
        print(f"Сохранено: {len(results)} судов")

if __name__ == "__main__":
    main()