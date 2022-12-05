import requests
from bs4 import BeautifulSoup
import csv
import re
from today_time import datetime_now
import pandas as pd

BASE_URL = "https://www.youtube.com/"
filename = BASE_URL


class ParseWebPage:
    def __init__(self, sourse_url):
        self.filename = re.search(
            r'https://(.*?)/', sourse_url).group(1).replace('.', '')+'.csv'
        self.url = sourse_url
        self.old_urls = set()
        self.repeat_data = set()

    def extract_recently_page(self, sub_url=None):
        if sub_url is not None:
            my_url = sub_url
        else:
            my_url = self.url
        # print(my_url,"nima bu")
        try:
            r = requests.get(my_url)
        except:
            r = requests.get(self.url)
            return 
        soup = BeautifulSoup(r.content, 'html5lib')
        data = set()

        for row in soup.findAll('p'):
            title = row.text.replace('\n', ' ').replace(
                '\t', '').replace(':', '').replace('/', '')
            if title != '':
                cleaning_data = ''.join([i for i in title if not i.isdigit()])
                if cleaning_data in self.repeat_data:
                    continue
                else:
                    data.add(cleaning_data)
                    self.repeat_data.add(cleaning_data)

        for row in soup.findAll('span'):
            title = row.text.replace('\n', ' ').replace(
                '\t', '').replace(':', '').replace('/', '')
            if title != '':
                cleaning_data = ''.join([i for i in title if not i.isdigit()])
                if cleaning_data in self.repeat_data:
                    continue
                else:
                    data.add(cleaning_data)
                    self.repeat_data.add(cleaning_data)

        for row in soup.find_all('h1'):
            title = row.text.replace('\n', ' ').replace(
                '\t', '').replace(':', '').replace('/', '')
            if title != '':
                cleaning_data = ''.join([i for i in title if not i.isdigit()])
                if cleaning_data in self.repeat_data:
                    continue
                else:
                    data.add(cleaning_data)
                    self.repeat_data.add(cleaning_data)

        for row in soup.find_all('h2'):
            title = row.text.replace('\n', ' ').replace(
                '\t', '').replace(':', '').replace('/', '')
            if title != '':
                cleaning_data = ''.join([i for i in title if not i.isdigit()])
                if cleaning_data in self.repeat_data:
                    continue
                else:
                    data.add(cleaning_data)
                    self.repeat_data.add(cleaning_data)

        for row in soup.find_all('h3'):
            title = row.text.replace('\n', ' ').replace(
                '\t', '').replace(':', '').replace('/', '')
            if title != '':
                cleaning_data = ''.join([i for i in title if not i.isdigit()])
                if cleaning_data in self.repeat_data:
                    continue
                else:
                    data.add(cleaning_data)
                    self.repeat_data.add(cleaning_data)
        
        for row in soup.find_all('div'):
            title = row.text.replace('\n', ' ').replace(
                '\t', '').replace(':', '').replace('/', '')
            if title != '':
                cleaning_data = ''.join([i for i in title if not i.isdigit()])
                if cleaning_data in self.repeat_data or ".css" in cleaning_data:
                    continue
                else:
                    data.add(cleaning_data)
                    self.repeat_data.add(cleaning_data)
        
        for row in soup.find_all('i'):
            title = row.text.replace('\n', ' ').replace(
                '\t', '').replace(':', '').replace('/', '')
            if title != '':
                cleaning_data = ''.join([i for i in title if not i.isdigit()])
                if cleaning_data in self.repeat_data:
                    continue
                else:
                    data.add(cleaning_data)
                    self.repeat_data.add(cleaning_data)

        # new csv file created and add webpage text

        if len(data) != 0:
            cleaned_data = ' '.join(data)

            dictionary_data = {
                "source_url": my_url,
                "access_datetime": datetime_now(),
                "content": cleaned_data,
            }

        else:
            return

        if sub_url is None:
            with open(self.filename, 'w', encoding='utf-8', newline='') as f:
                w = csv.DictWriter(
                    f, fieldnames=['source_url', 'access_datetime', 'content'])
                w.writeheader()
                for data in [dictionary_data]:
                    w.writerow(data)
        else:
            # append new data in exists csv file
            with open(self.filename, 'a', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([my_url, datetime_now(), cleaned_data])

        data.clear()

    def extract_text_from_sub_url(self):
        r = requests.get(BASE_URL)
        soup = BeautifulSoup(r.content, 'html5lib')
        for row in soup.findAll('a'):
            sub = row['href']
            if "https://" in sub:
                sub_url = row['href']
            else:
                uz_index = self.url.find('/uz',8)
                if uz_index != -1:
                    main_url = self.url[:uz_index]
                else:
                    main_url = self.url
                sub_url = main_url + sub
            print(sub_url, "url found")

            if sub_url not in self.old_urls:
                self.extract_recently_page(sub_url)
            self.old_urls.add(sub_url)


obj = ParseWebPage(BASE_URL)

obj.extract_recently_page()
obj.extract_text_from_sub_url()


class SplitContent:
    def __init__(self, sourse_url):
        self.filename = re.search(
            r'https://(.*?)/', sourse_url).group(1).replace('.', '')+'.csv'
        self.df = pd.read_csv(self.filename)

    def split_text(self):
        self.df['content'] = self.df['content'].map(lambda x: x.replace(',', ''))
        self.df['content'] = self.df['content'].map(lambda x: x.replace('[', ''))
        self.df['content'] = self.df['content'].map(lambda x: x.replace(']', ''))
        self.df['content'] = self.df['content'].map(lambda x: x.replace('<<', ''))
        self.df['content'] = self.df['content'].map(lambda x: x.replace('>>', '')) 
        self.df['content'] = self.df['content'].map(lambda x: x.replace('"', '')) 
        self.df['content'] = self.df['content'].map(lambda x: x.replace('»', '')) 
        self.df['content'] = self.df['content'].map(lambda x: x.replace('«', ''))
        self.df['content'] = self.df['content'].map(lambda x: x.replace('(', ''))
        self.df['content'] = self.df['content'].map(lambda x: x.replace(')', ''))
        self.df['content'] = self.df['content'].map(lambda x: x.replace('  ', ''))
        self.df['content'] = self.df['content'].str.strip()
        # df_clean = self.df['content'].str.extract(r'{(.*?)}').group(1)
        # self.df['content'].
        
        self.df['word'] = self.df.content.map(lambda x: x.split())
        self.df.to_csv(self.filename)
        print(self.df)


obj2 = SplitContent(filename)
obj2.split_text()

