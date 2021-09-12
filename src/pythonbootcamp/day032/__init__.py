__all__ = [
]

import random
import re
import pkg_resources


class MotivationQuote:

    def __init__(self):
        super(MotivationQuote, self).__init__()
        with open(pkg_resources.resource_filename(__name__, 'data/quotes.txt')) as file:
            data = file.readlines()
        self.data = {i: [{'author': author.strip(), 'text': text.strip()+'\"'}
                         for text, author in [re.split('\" - ', line) for line in data]][i]
                     for i in range(0, len(data))}

    def random_quote(self):
        return self.data[random.randint(0, len(self.data)-1)]


if __name__ == '__main__':
    print("Example output:")
    print(MotivationQuote().random_quote())
