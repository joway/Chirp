def test_pipeline(backend, user, response, strategy, *args, **kwargs):
    strategy.session_get('ident')
    print(response)
