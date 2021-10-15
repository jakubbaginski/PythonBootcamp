import pythonbootcamp.day032


def test032_001():
    assert pythonbootcamp.day032.MotivationQuote().random_quote()['author'] != ''


def test032_002():
    a = pythonbootcamp.day032.MotivationQuote().random_quote()['author']
    b = pythonbootcamp.day032.MotivationQuote().random_quote()['author']
    c = pythonbootcamp.day032.MotivationQuote().random_quote()['author']
    d = pythonbootcamp.day032.MotivationQuote().random_quote()['author']

    assert not (a == b == c == d)
