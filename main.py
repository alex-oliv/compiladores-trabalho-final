import sys
from antlr4 import *
from antlr4.Token import CommonToken

from TFG3MyVisitor import TFG3MyVisitor
from dist.TrabalhoFinalG3Lexer import TrabalhoFinalG3Lexer
from dist.TrabalhoFinalG3Parser import TrabalhoFinalG3Parser

if __name__ == '__main__':
    print('\nANTLR com Acoes Semanticas')
    data = FileStream('inputExpr.txt')

    lexer = TrabalhoFinalG3Lexer(data)
    stream = CommonTokenStream(lexer)

    parser = TrabalhoFinalG3Parser(stream)
    tree = parser.prog()

    visitor = TFG3MyVisitor()
    output = visitor.visit(tree)
