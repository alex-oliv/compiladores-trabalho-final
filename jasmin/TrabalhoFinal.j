.class TrabalhoFinal
.super java/lang/Object
.method public static main([Ljava/lang/String;)V
.limit stack 50
.limit locals 10
getstatic java/lang/System/out Ljava/io/PrintStream;
ldc "Digite um numero:"
invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
invokestatic TrabalhoFinal.read()I
istore 0
getstatic java/lang/System/out Ljava/io/PrintStream;
ldc "Valor n ="
invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V
getstatic java/lang/System/out Ljava/io/PrintStream;
iload 0
invokevirtual java/io/PrintStream/println(I)V
Fim:
return
.end method

.method public static read()I

        .limit stack 5   ; up to five items can be pushed
        .limit locals 100

        ; the input function starts at this point
            ldc 0
            istore 50     ; storage for a dummy integer for reading it by input()
            ldc 0
            istore 49     ; preparacao para negativo
        Label1:
            getstatic java/lang/System/in Ljava/io/InputStream;
            invokevirtual java/io/InputStream/read()I
            istore 51
            iload 51
            ldc 10 ; uso no mac (valor ASCII da tecla ENTER)
        ;    ldc 13 ; uso no windows (valor ASCII da tecla ENTER)
            isub
            ifeq Label2
            iload 51
            ldc 32 ; space 
            isub
            ifeq Label2
            iload 51
            ldc 43 ; plus sign
            isub
            ifeq Label1
            iload 51
            ldc 45 ; minus sign
            isub
            ifeq Label3
            iload 51
            ldc 48
            isub
            ldc 10
            iload 50
            imul
            iadd
            istore 50
            goto Label1

        Label3:
            ldc 1
            istore 49
            goto Label1
            
        Label2:     ; now our dummy integer contains the integer read from the keyboard
            ldc 1
            iload 49
            isub
            ifeq Label4
            iload 50       ; input function ends here
            ireturn
        Label4:
            ldc 0
            iload 50
            isub
            ireturn
        .end method