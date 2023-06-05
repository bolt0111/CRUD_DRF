import django, os, sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "techtest.settings")
sys.path.append(os.path.join(os.path.realpath(os.path.dirname(__file__)), "..", ".."))
django.setup()

from techtest.articles.models import Article
from techtest.regions.models import Region
from techtest.authors.models import Author
from django.core import management

# Migrate
management.call_command("migrate", no_input=True)
# Seed
region_1 = Region.objects.create(code="AL", name="Albania")
region_2 = Region.objects.create(code="UK", name="United Kingdom")
region_3 = Region.objects.create(code="AU", name="Austria"),
region_4 = Region.objects.create(code="US", name="United States of America")

author_1 = Author.objects.create(first_name="Riley", last_name="Taylor")
author_2 = Author.objects.create(first_name="Kevin", last_name="Makker")

Article.objects.create(title="Fake Article", content="Fake Content", author=author_1).regions.set(
    [
        region_1, region_2
    ]
)

Article.objects.create(title="Fake Article", content="Fake Content", author=author_2).regions.set(
    [
        region_3, region_4
    ]
)
