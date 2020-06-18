import lexer, parser
from pandas import DataFrame
from sys import argv

table = DataFrame([
    ['err', 'err', 'err', 'F1 F', 'F1 F', 'err', None],
    ['err', 'err', 'err', 'D = R1 R .', 'D = R1 R .', 'err', 'err'],
    ['err', 'err', 'err', 'a', 'n', 'err', 'err'],
    ['err', None, '| R1 R', 'err', 'err', 'err', 'err'],
    ['err', None, 'err', 'err', 'A', 'A', 'err'],
    ['err', None, None, 'err', 'A1 A', 'A1 A', 'err'],
    ['err', None, 'err', 'err', 'n', 't', 'err']
],
    columns=['=', '.', '|', 'a', 'n', 't', '$'],
    index=['F', 'F1', 'D', 'R', 'R1', 'A', 'A1']
)

lexer = lexer.Lexer(argv[1])
tokens = lexer.get_next_token()
tree = parser.parse('F', '=.|ant', lambda X, a: table.loc[X][a], tokens)
print(table)
print(tree)
