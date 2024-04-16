import random
from typing import Literal

import gnews
import newspaper
import requests
from pydantic import BaseModel


class Article(BaseModel):
    topic: str

    n: int = 10
    language: str = 'en'
    country: str = 'US'

    url: str = None
    title: str = None
    summary: str = None

    def __init__(self, **data):
        super().__init__(**data)

        self.language = Article.map_language(self.language)
        self.country = Article.map_country(self.country)

        news_page = self.retrieve_news_page()
        news = random.choice(news_page)

        self.url = requests.get(news['url']).url

        article = self.retrieve_article()

        self.title = article.title
        self.summary = article.summary.replace('\n', ' ')

    def __call__(self) -> dict:
        return {
            'url': self.url,
            'title': self.title,
            'summary': self.summary.replace('\n', ' ')
        }

    def __str__(self) -> str:
        return f'Title:{self.title}\nSummary:{self.summary}'

    def retrieve_news_page(self):
        return gnews.GNews(
            max_results=self.n,
            language=self.language,
            country=self.country
        ).get_news(self.topic)

    def retrieve_article(self):
        article = newspaper.Article(self.url)
        article.download()
        article.parse()
        article.nlp()

        return article

    @staticmethod
    def map_language(language: str) -> Literal['en', 'de', 'nl', 'sr', 'it']:
        return {
            'english': 'en',
            'german': 'de',
            'dutch': 'nl',
        }[language.lower()]

    @staticmethod
    def map_country(country: str) -> Literal['US', 'DE', 'NL', 'RS', 'IT']:
        return {
            'english': 'US',
            'german': 'DE',
            'dutch': 'NL',
        }[country.lower()]
