def includeme(config):
    config.add_route('index.dashboard', '/dashboard')
    config.add_route('index.dashboard.api', '/api/dashboard/')
    config.add_route('index.versions', '/versions')
    config.add_route('index.json_body', '/json-body')
