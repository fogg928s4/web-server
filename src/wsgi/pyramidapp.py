# A small pyramid web app
from pyramid.config import Configurator
from pyramid.response import Response


def greeting(request):
    return Response(
        'Hello Mom & Dad from Pyramid!\n',
        content_type='text/plain',
    )


config = Configurator()
config.add_route('hello', '/hello')  # localhost:8888/hello
config.add_view(greeting, route_name='hello')
app = config.make_wsgi_app()
