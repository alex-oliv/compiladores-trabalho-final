# Generated from TrabalhoFinalG3.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .TrabalhoFinalG3Parser import TrabalhoFinalG3Parser
else:
    from TrabalhoFinalG3Parser import TrabalhoFinalG3Parser

# This class defines a complete generic visitor for a parse tree produced by TrabalhoFinalG3Parser.

class TrabalhoFinalG3Visitor(ParseTreeVisitor):

    # Visit a parse tree produced by TrabalhoFinalG3Parser#prog.
    def visitProg(self, ctx:TrabalhoFinalG3Parser.ProgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TrabalhoFinalG3Parser#Declarations.
    def visitDeclarations(self, ctx:TrabalhoFinalG3Parser.DeclarationsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TrabalhoFinalG3Parser#t_type.
    def visitT_type(self, ctx:TrabalhoFinalG3Parser.T_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TrabalhoFinalG3Parser#id_list.
    def visitId_list(self, ctx:TrabalhoFinalG3Parser.Id_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TrabalhoFinalG3Parser#attrib_list.
    def visitAttrib_list(self, ctx:TrabalhoFinalG3Parser.Attrib_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TrabalhoFinalG3Parser#func_declaration.
    def visitFunc_declaration(self, ctx:TrabalhoFinalG3Parser.Func_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TrabalhoFinalG3Parser#parameter_list.
    def visitParameter_list(self, ctx:TrabalhoFinalG3Parser.Parameter_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TrabalhoFinalG3Parser#main_block.
    def visitMain_block(self, ctx:TrabalhoFinalG3Parser.Main_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TrabalhoFinalG3Parser#stats.
    def visitStats(self, ctx:TrabalhoFinalG3Parser.StatsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TrabalhoFinalG3Parser#AttribCommand.
    def visitAttribCommand(self, ctx:TrabalhoFinalG3Parser.AttribCommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TrabalhoFinalG3Parser#IfCommand.
    def visitIfCommand(self, ctx:TrabalhoFinalG3Parser.IfCommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TrabalhoFinalG3Parser#condition_block.
    def visitCondition_block(self, ctx:TrabalhoFinalG3Parser.Condition_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TrabalhoFinalG3Parser#ForCommand.
    def visitForCommand(self, ctx:TrabalhoFinalG3Parser.ForCommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TrabalhoFinalG3Parser#RangeCommand.
    def visitRangeCommand(self, ctx:TrabalhoFinalG3Parser.RangeCommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TrabalhoFinalG3Parser#WhileCommand.
    def visitWhileCommand(self, ctx:TrabalhoFinalG3Parser.WhileCommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TrabalhoFinalG3Parser#PrintCommand.
    def visitPrintCommand(self, ctx:TrabalhoFinalG3Parser.PrintCommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TrabalhoFinalG3Parser#InputCommand.
    def visitInputCommand(self, ctx:TrabalhoFinalG3Parser.InputCommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TrabalhoFinalG3Parser#funct_call.
    def visitFunct_call(self, ctx:TrabalhoFinalG3Parser.Funct_callContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TrabalhoFinalG3Parser#funct_return.
    def visitFunct_return(self, ctx:TrabalhoFinalG3Parser.Funct_returnContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TrabalhoFinalG3Parser#BreakCommand.
    def visitBreakCommand(self, ctx:TrabalhoFinalG3Parser.BreakCommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TrabalhoFinalG3Parser#stats_block.
    def visitStats_block(self, ctx:TrabalhoFinalG3Parser.Stats_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TrabalhoFinalG3Parser#NotExp.
    def visitNotExp(self, ctx:TrabalhoFinalG3Parser.NotExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TrabalhoFinalG3Parser#IdExp.
    def visitIdExp(self, ctx:TrabalhoFinalG3Parser.IdExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TrabalhoFinalG3Parser#StringExp.
    def visitStringExp(self, ctx:TrabalhoFinalG3Parser.StringExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TrabalhoFinalG3Parser#ParenExp.
    def visitParenExp(self, ctx:TrabalhoFinalG3Parser.ParenExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TrabalhoFinalG3Parser#BooleanExp.
    def visitBooleanExp(self, ctx:TrabalhoFinalG3Parser.BooleanExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TrabalhoFinalG3Parser#LogicExp.
    def visitLogicExp(self, ctx:TrabalhoFinalG3Parser.LogicExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TrabalhoFinalG3Parser#UnaryExp.
    def visitUnaryExp(self, ctx:TrabalhoFinalG3Parser.UnaryExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TrabalhoFinalG3Parser#NumberExp.
    def visitNumberExp(self, ctx:TrabalhoFinalG3Parser.NumberExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TrabalhoFinalG3Parser#InfixExp.
    def visitInfixExp(self, ctx:TrabalhoFinalG3Parser.InfixExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TrabalhoFinalG3Parser#FuncExp.
    def visitFuncExp(self, ctx:TrabalhoFinalG3Parser.FuncExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TrabalhoFinalG3Parser#expr_list.
    def visitExpr_list(self, ctx:TrabalhoFinalG3Parser.Expr_listContext):
        return self.visitChildren(ctx)



del TrabalhoFinalG3Parser