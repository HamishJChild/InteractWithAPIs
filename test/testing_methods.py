"""
A set of methods used in testing.
Methods:
    construct_url
"""


def construct_url(url, params) -> str:
    """
    This function takes the urls and params and constructs the full url
     that would be used in an api call. This is then passed to the HTTP client mocker, HTTPretty.
    :param url: str - the base_url
    :param params: dict - the query name and value
    :return: url: str - the full url
    """
    # loop over the parms, and append them to the url
    for param in params:
        url = url + '?' + param + '=' + str(params.get(param))
    return url
