def call_api(http_client_method_func, endpoint, *args, **kwargs):
    from src.framework.settings import get_settings
    settings = get_settings()
    url = '{0}{1}'.format(getattr(settings, 'BASE_URL_PREFIX'), endpoint)
    api_response = http_client_method_func(
        url,
        *args,
        **kwargs
    )

    return api_response
