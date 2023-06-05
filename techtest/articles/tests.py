import json

from django.test import TestCase
from django.urls import reverse

from techtest.articles.models import Article
from techtest.regions.models import Region
from techtest.authors.models import Author


class ArticleListViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse("articles-list")
        self.article_1 = Article.objects.create(title="Article 1")

        self.region_1 = Region.objects.create(code="AL", name="Albania")
        self.region_2 = Region.objects.create(code="UK", name="United Kingdom")
        self.region_3 = Region.objects.create(code="AU", name="Australia")
        self.article_2 = Article.objects.create(
            title="Article 2", content="Lorem Ipsum"
        )
        self.article_2.regions.set([self.region_1, self.region_2])

        self.author_1 = Author.objects.create(first_name="Riley", last_name="Taylor")
        self.author_2 = Author.objects.create(first_name="Kevin", last_name="Makker")

        self.article_3 = Article.objects.create(title="Article 3", content="Content", author = self.author_1)
        self.article_3.regions.set(
            [
                self.region_3
            ]
        )


    def test_serializes_with_correct_data_shape_and_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(
            response.json(),
            [
                {
                    "id": self.article_1.id,
                    "title": "Article 1",
                    "content": "",
                    "regions": [],
                    "author": None
                },
                {
                    "id": self.article_2.id,
                    "title": "Article 2",
                    "content": "Lorem Ipsum",
                    "regions": [
                        {
                            "id": self.region_1.id,
                            "code": "AL",
                            "name": "Albania",
                        },
                        {
                            "id": self.region_2.id,
                            "code": "UK",
                            "name": "United Kingdom",
                        },
                    ],
                    "author": None
                },
                {
                    "id": self.article_3.id,
                    "title": "Article 3",
                    "content": "Content",
                    "regions": [
                        {
                            "id": self.region_3.id,
                            "code": "AU",
                            "name": "Australia",
                        }
                    ],
                    "author": {
                        "id": self.author_1.id,
                        "first_name": "Riley",
                        "last_name": "Taylor"
                    },
                },
            ],
        )

    def test_creates_new_article_with_regions_and_author(self):
            payload = {
                "title": "Fake Article 3",
                "content": "To be or not to be",
                "regions": [
                    {"code": "US", "name": "United States of America"}
                ],
                "author": {
                    "first_name": "Kevin",
                    "last_name": "Makker"
                }
            }
            response = self.client.post(
                self.url, data=json.dumps(payload), content_type="application/json"
            )
            article = Article.objects.last()
            regions = Region.objects.filter(articles__id=article.id)
            self.assertEqual(response.status_code, 200)
            self.assertIsNotNone(article)
            self.assertEqual(regions.count(), 1)
            self.assertDictEqual(
                {
                    "id": article.id,
                    "title": "Fake Article 3",
                    "content": "To be or not to be",
                    "regions": [
                        {
                            "id": regions.all()[0].id,
                            "code": "US",
                            "name": "United States of America",
                        }
                    ],
                    "author": {
                        "id": article.author.id,
                        "first_name": "Kevin",
                        "last_name": "Makker"
                    }
                },
                response.json(),
            )

class ArticleViewTestCase(TestCase):
    def setUp(self):
        self.region_1 = Region.objects.create(code="AL", name="Albania")
        self.region_2 = Region.objects.create(code="UK", name="United Kingdom")

        self.author_1 = Author.objects.create(first_name="Riley", last_name="Taylor")

        self.article = Article.objects.create(title="Fake Article 1", content="Fake Content 1", author=self.author_1)

        self.article.regions.set([self.region_1, self.region_2])
        self.url = reverse("article", kwargs={"article_id": self.article.id})

    def test_serializes_single_record_with_correct_data_shape_and_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.json(),
            {
                "id": self.article.id,
                "title": "Fake Article 1",
                "content": "Fake Content 1",
                "regions": [
                    {
                        "id": self.region_1.id,
                        "code": "AL",
                        "name": "Albania",
                    },
                    {
                        "id": self.region_2.id,
                        "code": "UK",
                        "name": "United Kingdom",
                    },
                ],
                "author": {
                    "id": self.author_1.id,
                    "first_name": "Riley",
                    "last_name": "Taylor"
                }
            },
        )

    def test_updates_article_and_regions(self):
        payload = {
            "title": "Fake Article 1 (Modified)",
            "content": "To be or not to be here",
            "regions": [
                {"code": "US", "name": "United States of America"},
                {"id": self.region_2.id},
            ],
            "author": {
                "first_name": "Kevin",
                "last_name": "Makker",
            }
        }
        response = self.client.put(
            self.url, data=json.dumps(payload), content_type="application/json"
        )
        article = Article.objects.first()
        regions = Region.objects.filter(articles__id=article.id)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(article)
        self.assertEqual(regions.count(), 2)
        self.assertEqual(Article.objects.count(), 1)
        self.assertDictEqual(
            {
                "id": article.id,
                "title": "Fake Article 1 (Modified)",
                "content": "To be or not to be here",
                "regions": [
                    {
                        "id": self.region_2.id,
                        "code": "UK",
                        "name": "United Kingdom",
                    },
                    {
                        "id": regions.all()[1].id,
                        "code": "US",
                        "name": "United States of America",
                    },
                ],
                "author": {
                    "id": 2,
                    "first_name": "Kevin",
                    "last_name": "Makker"
                }
            },
            response.json(),
        )

    def test_removes_article(self):
        self.url = reverse("delete_article", kwargs={"article_id": self.article.id})
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Article.objects.count(), 0)

    def test_removes_author_from_article(self):
        self.url = reverse("delete_author_from_article", kwargs={"article_id": self.article.id})
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Article.objects.first().author, None)