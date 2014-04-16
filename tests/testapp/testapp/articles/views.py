from rhetoric.view import view_config, view_defaults
from ..types import Language


@view_defaults(route_name='articles.regional.index', renderer='json')
class ArticlesHandler(object):
    def __init__(self, request, language):
        self.request = request
        self.language = language
        self.region_strategy = Language.match(language)

    @view_config(request_method='GET')
    def show_local_entries(self):
        return {
            'language': self.language,
        }
