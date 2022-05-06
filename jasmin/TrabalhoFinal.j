.class TrabalhoFinal
.super java/lang/Object
.method public static main([Ljava/lang/String;)V
.limit stack 50
.limit locals 10
ldc 105.5
fstore 1
ldc 10.5
fstore 2
getstatic java/lang/System/out Ljava/io/PrintStream;
ldc "Hello World!"
invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
fload 1
fload 2
fadd
fstore 0
getstatic java/lang/System/out Ljava/io/PrintStream;
ldc "Valor z ="
invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
getstatic java/lang/System/out Ljava/io/PrintStream;
fload 0
invokevirtual java/io/PrintStream/println(F)V
ldc 100.5
ldc 110.5
fmul
fstore 0
getstatic java/lang/System/out Ljava/io/PrintStream;
ldc "Valor z ="
invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
getstatic java/lang/System/out Ljava/io/PrintStream;
fload 0
invokevirtual java/io/PrintStream/println(F)V
getstatic java/lang/System/out Ljava/io/PrintStream;
ldc "Valor palavra ="
invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
getstatic java/lang/System/out Ljava/io/PrintStream;
ldc "Arroz"
invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
return
.end method