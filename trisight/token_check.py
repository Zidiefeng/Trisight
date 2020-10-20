import webbrowser
import requests
token = "bu7668f48v6rajd4rrrg"

def token_check(token):
    '''Check whether the token is okay

    Use example:
        .. code-block:: python

            token_check("btj810748v6p9f1q5vpg")

    :param token:
        token to test
    :type token:
        str

    :returns:
        True (okay), False (not okay)
    :rtype:
        bool
    '''

    status = requests.get(f'https://finnhub.io/api/v1/stock/profile2?symbol=AAPL&token={token}').ok
    return status

def get_token(token):
    '''Check token. If not good, let the user to enter the right token.

    Use example:
        .. code-block:: python

            get_token("btj810748v6p9f1q5vpg")

    :param token: default token to check, can be empty if not know
    :type token: str

    :returns: correct token to use
    :rtype: str
    '''
    while not token_check(token):
        answer = input("Bad token. Need to update.Go to the website? (y or n):")
        if answer=="y":
            webbrowser.open("https://finnhub.io/dashboard")
        token = input("Please enter the new token:")
    print("Congrats! Great token.")
    return token
