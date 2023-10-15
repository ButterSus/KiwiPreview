from frontend.lexer.Lexer import Lexer
from frontend.parser.Parser import Parser

if __name__ == '__main__':
    with open('resources/main.kiwi', 'r') as f:
        source = f.read()
    # LEXER TEST
    # ==========>
    # lexer = Lexer().load(source)
    # print(*map(lambda x: x.toFormatString(), lexer.wrapper()), sep='\n')

    # PARSER TEST
    # ===========>
    print(
        Parser(Lexer().load(source).tokenize()).start().toFormatString(indent=2)
    )
