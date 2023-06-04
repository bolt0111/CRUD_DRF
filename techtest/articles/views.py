import json

from marshmallow import ValidationError
from django.views.generic import View

from techtest.articles.models import Article
from techtest.articles.schemas import ArticleSchema
from techtest.utils import json_response


class ArticlesListView(View):
    def get(self, request, *args, **kwargs):
        return json_response(ArticleSchema().dump(Article.objects.all(), many=True))

    def post(self, request, *args, **kwargs):
        try:
            article = ArticleSchema().load(json.loads(request.body))
        except ValidationError as e:
            return json_response(e.messages, 400)
        return json_response(ArticleSchema().dump(article), 201)


class ArticleView(View):
    def get(self, request, article_id, *args, **kwargs):
        try:
            self.article = Article.objects.get(pk=article_id)
        except Article.DoesNotExist:
            return json_response({"error": "Article does not exist."}, status=404)
        return json_response(ArticleSchema().dump(self.article))

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            print("Data", data)
            self.article = ArticleSchema().load(data)
            self.article.save()
        except ValidationError as e:
            return json_response(e.messages, 400)
        return json_response(ArticleSchema().dump(self.article))

    def put(self, request, article_id, *args, **kwargs):
        print("Here is PUT")
        try:
            self.article = Article.objects.get(pk=article_id)
            data = json.loads(request.body)
            self.article.content = data["content"]
            self.article.title = data["title"]
            if data["author"]:
                self.article.author.id = data["author"]["id"]
                self.article.author.first_name = data["author"]["first_name"]
                self.article.author.last_name = data["author"]["last_name"]
            else:
                self.article.author = None
            if data["regions"]:
                region_ids = [region["id"] for region in data["regions"]]
                self.article.regions.set(region_ids)
        except Article.DoesNotExist:
            return json_response({"error": "No article matches the given query"}, 404)
        except ValidationError as e:
            return json_response(e.messages, 400)
        return json_response(ArticleSchema().dump(self.article))

    def delete(self, request, article_id, *args, **kwargs):
        try:
            self.article = Article.objects.get(pk=article_id)
        except Article.DoesNotExist:
            return json_response({"error": "Article does not exist."}, status=404)
        if request.path.endswith('/delete_author/'):
            if self.article.author:
                self.article.author = None
                self.article.save()
                return json_response(ArticleSchema().dump(self.article))
            else:
                return json_response({"error": "Author does not exist for the article"}, status=404)
        elif request.path.endswith('/delete/'):
            self.article.delete()
        return json_response({"success":"Delete article successfully "})
