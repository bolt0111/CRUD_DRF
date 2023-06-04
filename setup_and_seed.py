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
Article.objects.create(title="Fake Article", content="Fake Content", author = Author.objects.create(first_name="Kevin", last_name="Makker"))
Article.objects.create(title="Fake Article", content="Fake Content").regions.set(
    [
        Region.objects.create(code="Fr", name="France"),
        Region.objects.create(code="Jp", name="Japan"),
    ]
)
