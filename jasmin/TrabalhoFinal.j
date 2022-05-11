.class TrabalhoFinal
.super java/lang/Object
.method public static main([Ljava/lang/String;)V
.limit stack 50
.limit locals 10
ldc 0
istore 0
Lfori:
iload 0
ldc 3
if_icmpge L0
iload 0
ldc 2
if_icmpeq L1
goto L2
L1:
getstatic java/lang/System/out Ljava/io/PrintStream;
ldc "Valor i ="
invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
getstatic java/lang/System/out Ljava/io/PrintStream;
iload 0
invokevirtual java/io/PrintStream/println(I)V
L2:
getstatic java/lang/System/out Ljava/io/PrintStream;
ldc "For i ="
invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
getstatic java/lang/System/out Ljava/io/PrintStream;
iload 0
invokevirtual java/io/PrintStream/println(I)V
goto Lfori_inc
Lfori_inc:
iinc 0 1
goto Lfori
L0:
return
Fim:
return
.end method