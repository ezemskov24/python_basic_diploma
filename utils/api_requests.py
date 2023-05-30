def get_request(url, params):
    pass


def post_request(url, params):
    pass


def api_requests(method_endswith, params, method_type):
    url = f"https://hotels4.p.rapidapi.com/{method_endswith}"

    if method_type == 'GET':
        return get_request(
            url=url,
            params=params
        )
    elif method_type == 'POST':
        return post_request(
            url=url,
            params=params
        )

