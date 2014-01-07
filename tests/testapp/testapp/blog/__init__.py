def includeme(config):
    config.add_route('test.new.routes', '/test/new/routes/{param:[a-z]{1,}}')
    config.add_route('blog.page', '/page/{page_slug}')

