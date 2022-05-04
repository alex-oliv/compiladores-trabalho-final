from antlr4.RuleContext import RuleContext
from antlr4.Token import Token
from antlr4.error.ErrorListener import ProxyErrorListener, ConsoleErrorListener

RecognitionException = None


class MyRecognizer(object):
    def getErrorHeader(self, e: RecognitionException):
        line = e.getOffendingToken().line
        column = e.getOffendingToken().column
        return "line "+line+":"+column
