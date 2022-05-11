.class TrabalhoFinal
.super java/lang/Object
.method public static main([Ljava/lang/String;)V
.limit stack 50
.limit locals 10
ldc 0
istore 0
Lforx:
iload 0
ldc 5
if_icmpge L0
getstatic java/lang/System/out Ljava/io/PrintStream;
ldc "Valor x ="
invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
getstatic java/lang/System/out Ljava/io/PrintStream;
iload 0
invokevirtual java/io/PrintStream/println(I)V
goto Lforx_inc
Lforx_inc:
iinc 0 1
goto Lforx
L0:
return
Fim:
return
.end method