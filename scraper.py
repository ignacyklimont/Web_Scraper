# Project: Web Scraper
# Python 3.10
# Date: 13/08/2022

import requests
import string
from bs4 import BeautifulSoup
import os


# Main WebScraper class
class WebScraper:

	def __init__(self):
		self.pages = int(input())
		self.type = input()
		self.article_dic = {}

	def make_dir(self):
		for num in range(1, self.pages + 1):
			os.makedirs(f'Page_{num}', exist_ok=True)
			print(f'Directory "Page_{num}" created!')
		WebScraper.url_input(self)

	def url_input(self):
		for num in range(1, self.pages + 1):  # Scraping by the webpage number
			url_link = f'https://www.nature.com/nature/articles?sort=PubDate&year=2020&page={num}'
			r = requests.get(url_link)
			if r and r.status_code == 200:  # If r is true ("if r") means that the HTTP response is positive = we can proceed
				soup = BeautifulSoup(r.content, 'html.parser')
				articles = soup.find_all('article')
				for article in articles:
					if article.find('span', {"class": 'c-meta__type'}).text == self.type:
						self.article_dic[article.a['href']] = {num}  # Saving to dictionary to keep track of page number
						WebScraper.article_scraper(self, article)
			else:
				print(f'The URL returned {r.status_code}')
				exit()

	def article_scraper(self, news_article):
		news_title = news_article.a.text  # Title of an article
		news_link = news_article.a["href"]
		link_content = requests.get('https://www.nature.com' + news_link)  # URL of an article
		news_content = BeautifulSoup(link_content.content, 'html.parser')
		news_body = news_content.find("div", {"class": "c-article-body"}).text.strip()  # Body of an article
		for x in news_title:  # Standardizing the article (and thus file) title
			if x in string.punctuation:
				news_title.replace(x, "")
		news_title = news_title.strip()
		news_title = news_title.replace(' ', '_') + '.txt'
		num = self.article_dic[news_link]
		num = str(num).strip("{}")
		path_to_dir = f'/Users/ignacyklimont/PycharmProjects/Web Scraper/Web Scraper/task/Page_{num}'
		path_to_file = os.path.join(path_to_dir, news_title)
		new_file = open(path_to_file, 'w')
		new_file.write(news_body)
		new_file.close()
		print('File successfully saved')


if __name__ == '__main__':
	scraper = WebScraper()
	scraper.make_dir()
