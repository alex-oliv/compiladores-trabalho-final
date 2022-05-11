.class TrabalhoFinal
.super java/lang/Object
.method public static main([Ljava/lang/String;)V
.limit stack 50
.limit locals 10
ldc 0
istore 1
ldc 555
istore 2
Lforx:
iload 1
ldc 3
if_icmpge L0
iload 1
ldc 1
if_icmpeq L1
goto ELSE2
L1:
getstatic java/lang/System/out Ljava/io/PrintStream;
ldc "Valor if(x) ="
invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
getstatic java/lang/System/out Ljava/io/PrintStream;
iload 1
invokevirtual java/io/PrintStream/println(I)V
ELSE2:
getstatic java/lang/System/out Ljava/io/PrintStream;
ldc "DIFERENTE DE 1"
invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
getstatic java/lang/System/out Ljava/io/PrintStream;
ldc "ELSEZIN"
invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
L2:
getstatic java/lang/System/out Ljava/io/PrintStream;
ldc "For x ="
invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
getstatic java/lang/System/out Ljava/io/PrintStream;
iload 1
invokevirtual java/io/PrintStream/println(I)V
goto Lforx_inc
Lforx_inc:
iinc 1 1
goto Lforx
L0:
return
Fim:
return
.end method