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


"""
data = FileStream('entrada.txt')
    lexer = TarefaLexer(data)

    lines = []
    lines.append("Token" + " "*17 + "Tipo" + "\n" + "-"*26 + "\n")

    for token in lexer.getAllTokens():
        rule = lexer.ruleNames[token.type-1]

        if "T__" in rule:
            rule = 'Simbolo'

        if rule == 'NUM':
            rule = 'Numero'

        linhaArquivo = token.text.ljust(12) + "||" + rule.rjust(12) + "\n"
        if(rule != 'NEWLINE'):
            lines.append(linhaArquivo)

    with open('saida.txt', 'w+') as writer:
        writer.writelines(lines)
        writer.close()
"""