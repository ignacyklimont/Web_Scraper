import requests
import string
from bs4 import BeautifulSoup
import os


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
		for num in range(1, self.pages + 1):
			url_link = f'https://www.nature.com/nature/articles?sort=PubDate&year=2020&page={num}'
			r = requests.get(url_link)
			if r and r.status_code == 200:  # If r is true ("if r") means that the HTTP response is positive = we can proceed
				soup = BeautifulSoup(r.content, 'html.parser')
				articles = soup.find_all('article')
				for article in articles:
					if article.find('span', {"class": 'c-meta__type'}).text == self.type:
						self.article_dic[article.a['href']] = {num}
						WebScraper.news_scraper(self, article)
			else:
				print(f'The URL returned {r.status_code}')
				exit()

	def news_scraper(self, news_article):
		news_title = news_article.a.text
		news_link = news_article.a["href"]
		link_content = requests.get('https://www.nature.com' + news_link)
		news_content = BeautifulSoup(link_content.content, 'html.parser')
		news_body = news_content.find("div", {"class": "c-article-body"}).text.strip()
		for x in news_title:
			if x in string.punctuation:
				news_title.replace(x, "")
		news_title = news_title.strip()
		news_title = news_title.replace(' ', '_') + '.txt'
		num = self.article_dic[news_link]
		num = str(num).strip("{}")
		save_path = f'/Users/ignacyklimont/PycharmProjects/Web Scraper/Web Scraper/task/Page_{num}'
		full_name = os.path.join(save_path, news_title)
		new_file = open(full_name, 'w')
		new_file.write(news_body)
		new_file.close()
		print('File successfully saved')


if __name__ == '__main__':
	scraper = WebScraper()
	scraper.make_dir()
