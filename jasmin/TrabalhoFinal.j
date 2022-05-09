.class TrabalhoFinal
.super java/lang/Object
.method public static main([Ljava/lang/String;)V
.limit stack 50
.limit locals 10
ldc 2.5
fstore 1
fload 1
ldc 5.0
fadd
fstore 0
getstatic java/lang/System/out Ljava/io/PrintStream;
ldc "Num ="
invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
getstatic java/lang/System/out Ljava/io/PrintStream;
fload 0
invokevirtual java/io/PrintStream/println(F)V
Fim:
return
.end method