.class TrabalhoFinal
.super java/lang/Object
.method public static main([Ljava/lang/String;)V
.limit stack 50
.limit locals 10
ldc 5
istore 1
2-iload 0
istore 0
getstatic java/lang/System/out Ljava/io/PrintStream;
ldc "1-Valor x ="
invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
getstatic java/lang/System/out Ljava/io/PrintStream;
iload 0
invokevirtual java/io/PrintStream/println(I)V
1-iload 0
ineg
istore 0
getstatic java/lang/System/out Ljava/io/PrintStream;
ldc "2-Valor x ="
invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
getstatic java/lang/System/out Ljava/io/PrintStream;
iload 0
invokevirtual java/io/PrintStream/println(I)V
Fim:
return
.end method