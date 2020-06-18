import re


class Token:
    def __init__(self, domain, coords, attr):
        self.domain = domain
        self.coords = coords
        self.attr = attr

    def __str__(self):
        return '{} {}: {}'.format(self.domain, self.coords, self.attr)

    def __repr__(self):
        return '{} {}: {}\n'.format(self.domain, self.coords, self.attr)


class Lexer:
    lexems = (
        ('n', '\([A-Z][0-9]*\)'),
        ('a', '\(axiom [A-Z][0-9]*\)'),
        ('|', '\|'),
        ('.', '\.'),
        ('=', '\='),
        ('t', '(\\\\[^\n \t]|[^\n \t])'),
    )
    tokens = []

    def get_next_token(self):
        return (t for t in self.tokens)

    def match_all(self, line, line_pos, data_pos):
        for lexem in self.lexems:
            match = re.match(lexem[1], self.data[data_pos:])
            if match:
                self.tokens.append(Token(lexem[0], (line, line_pos), match.group()))
                return match
        return re.match('[\t \n]+', self.data[data_pos:])

    def scroll_data(self, data_pos, line, line_pos, count):
        for ch in self.data[data_pos:data_pos + count]:
            if ch == '\n':
                line += 1
                line_pos -= line_pos
            else:
                line_pos += 1
        return data_pos + count, line, line_pos

    def __init__(self, file):
        f = open(file, 'r')
        self.data = f.read()
        f.close()
        line, line_pos = 1, 0
        data_pos = 0

        while data_pos < len(self.data):
            match = self.match_all(line, line_pos, data_pos)
            if match:
                data_pos, line, line_pos = self.scroll_data(data_pos, line, line_pos, match.end())
            else:
                print('\033[33mlexem error', '(', line, ',', line_pos, ')\033[0m')
                data_pos, line, line_pos = self.scroll_data(data_pos, line, line_pos, 1)
        self.tokens.append(Token('$', (line, line_pos), ''))
