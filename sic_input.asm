COPY       START     1000 
FIRST      STL       RETADR             SAVE RETURN ADDRESS       
CLOOP      JSUB      RDREC
           LDA       LENGTH             
           COMP      ZERO
           JEQ       ENDFIL
           JSUB      RDREC
           J         CLOOP
ENDFIL     LDA       =C'EOF'            TEST LTORG DIRECTIVE
           STA       BUFFER
           LDA       THREE
           STA       LENGTH
           JSUB      WRREC
           LDL       RETADR
           RSUB
           LTORG 
.
.      CREATING LITERALS POOL
.
THREE      WORD      3
ZERO       WORD      0
RETADR     RESW      1
LENGTH     RESW      1
BUFFER     RESB      4096
.
.      SUBROUTINE TO READ RECORD INTO BUFFER
.
RDREC      LDX       ZERO
           LDA       ZERO
RLOOP      TD        =X'F1'
           JEQ       RLOOP
           RD        =X'F1'
           COMP      ZERO
           JEQ       EXIT
           STCH      BUFFER,X
           TIX       MAXLEN
           JLT       RLOOP
EXIT       STX       LENGTH
           RSUB
MAXLEN     WORD      4096
.
.      SUBROUTINE TO WRITE RECORD FROM BUFFER
.
WRREC      LDX       ZERO
WLOOP      TD        =X'05'
           JEQ       WLOOP
           LDCH      BUFFER,X
           WD        =X'05'
           TIX       LENGTH
           JLT       WLOOP
           RSUB
           END       FIRST