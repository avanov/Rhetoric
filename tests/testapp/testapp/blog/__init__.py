def includeme(config):
    config.add_route('test.new.routes', '/test/new/routes/{param:[a-z]+}')
