from ..types import Language


def includeme(config):
    """
    :type config: :class:`rhetoric.Configurator`
    """
    RULES = {
        'language': Language
    }
    config.add_route('articles.regional.index', '/articles/{language}', rules=RULES)
