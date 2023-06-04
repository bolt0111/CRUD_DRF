import json

from marshmallow import ValidationError
from django.views.generic import View

from techtest.authors.models import Author
from techtest.authors.schemas import AuthorSchema
from techtest.utils import json_response

class AuthorListView(View):
    def get(self, request, *args, **kwargs):
        return json_response(AuthorSchema().dump(Author.objects.all(), many=True))

    def post(self, request, *args, **kwargs):
        try:
            author = AuthorSchema.load(json.loads(request.body))
        except ValidationError as e:
            return json_response(e.messages, 400)
        return json_response(AuthorSchema().dump(author), 201)

class AuthorView(View):

    def get(self, request, author_id, *args, **kwargs):
        try:
            self.author = Author.objects.get(pk=author_id)
        except Author.DoesNotExist:
            return json_response({"error": "No Author matches the given query"}, 404)
        return json_response(AuthorSchema().dump(self.author))

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            self.author = AuthorSchema().load(data)
            self.author.save()
        except ValidationError as e:
            return json_response(e.messages, 400)
        return json_response(AuthorSchema().dump(self.author))

    def put(self, request, author_id, *args, **kwargs):
        try:
            self.author = Author.objects.get(pk=author_id)
            data = json.loads(request.body)
            self.author.first_name = data['first_name']
            self.author.last_name = data['last_name']
            self.author.save()
        except Author.DoesNotExist:
            return json_response({"error": "No Author matches the given query"}, 404)
        except ValidationError as e:
            return json_response(e.messages, 400)
        return json_response(AuthorSchema().dump(self.author))

    def delete(self, request, *args, **kwargs):
        self.author.delete()
        return json_response()