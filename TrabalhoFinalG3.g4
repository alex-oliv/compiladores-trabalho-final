grammar TrabalhoFinalG3;

prog: var_declaration* func_declaration* main_block EOF;

var_declaration:
	type_decl = t_type (var = id_list | attrib = attrib_list) ';' #Declarations;

t_type: 'int' | 'float' | 'string' | 'boolean' | 'void';

id_list: ID (',' ID)*;

attrib_list:
	ID '=' (ID | NUMBER | STRING | TRUE | FALSE) (
		',' ID '=' (ID | NUMBER | STRING | TRUE | FALSE)
	)*;

func_declaration:
	'def' func_type=t_type func_name=ID '(' (parameter_list+)? ')' ':' stats+ '}' #FuncDeclaration;

parameter_list: t_type ID (',')?;

main_block: 'main' '(' ')' ':' stats+ '}';

stats:
	attribution ';'
	| if_command 
	| for_command 
	| while_command 
	| print_command ';'
	| input_command ';'
	| break_command ';'
	| funct_return ';'
	| expr ';' ;

attribution: var=ID ('=' op=expr)+ #AttribCommand;

if_command:
	'if' condition_block '}' ('else' ':' stmt=stats_block '}')? #IfCommand;

condition_block: op=expr ':' stmt=stats_block;

for_command:
	'for' var=ID 'in' 'range' '(' rang=range_command ')' ':' stmt=stats_block+ '}' #ForCommand;

range_command: (start=(NUMBER | ID) ':')? stop=(NUMBER | ID) (':' step=(NUMBER | ID))? #RangeCommand;

while_command: 'while' '(' op=expr ')' ':' stmt=stats_block+ '}' #WhileCommand;

print_command: 'print' op1=expr (',' op2=expr)* #PrintCommand;

input_command: var=ID '=' 'input' '(' ')' #InputCommand;

funct_return: 'return' op=expr;

break_command: 'break' #BreakCommand;

stats_block:
  stats+;

expr:
	ID '(' expr_list? ')' 									                          # FuncExp
	| 'not' op=expr															        	            # NotExp
	| '-' op=expr															                        # UnaryExp
	| left = expr op = ('*' | '/') right = expr							          # InfixExp
	| left = expr op = ('+' | '-') right = expr							          # InfixExp
	| left = expr op = ('>' | '>=' | '<' | '<=' | '==' | '!=') right = expr	# LogicExp
	| left = expr op = ('and' | 'or') right = expr						        # LogicExp
	| '(' op=expr ')'														                      # ParenExp
	| atom = ID															                          # IdExp
	| atom = NUMBER													                         	# NumberExp
	| atom = STRING														                        # StringExp
	| atom = TRUE 								                    # BooleanExp;

expr_list: expr (',' expr)*;

ID: [a-zA-Z][a-zA-Z0-9_]*;
NUMBER: [0-9]+ ('.' [0-9]+)?;
STRING: '"' .*? '"';
TRUE: 'True';
FALSE: 'False';
SL_COMMENT: '//' .*? '\n' -> skip;
WS: [ \t\r\n]+ -> skip;