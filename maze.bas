5 REM An exercise in translating BASIC to Python using example code from "The Hitch-Hiker's Guide to Artificial Intelligence"

10 REM **********************************
11 REM ** Listing 5.1                  **
12 REM ** Robot Maze Learner           **
12 REM **********************************
20 SW%=80:SH%=23:REM SW% is Screen Width and SH% is Screen Height
30 DIM MAZE$(SH%,SW%),VISITS%(SH%,SW%),ROUTE%(2000,2)
40 CLS:ROBOT$=CHR$(1):WALL$=CHR$(219): REM These are IBM Special Characters.
50 FOR I%=3 TO SW%:LOCATE 1,I%:PRINT WALL$;:NEXT
60 FOR J%=2 TO SH%:LOCATE J%,SW%:PRINT WALL$;:NEXT
70 FOR I%=SW%-2 TO 1 STEP -1:LOCATE SH%,I%:PRINT WALL$;:NEXT
80 FOR J%=SH%-1 TO 1 STEP -1:LOCATE J%,1:PRINT WALL$;:NEXT
90 RANDOMIZE TIMER: FOR I%=2 TO SW%-1
100 FOR J%=2 TO SH%-1
110 IF RND <.25 THEN LOCATE J%,I%:PRINT WALL$;
120 NEXT :NEXT
130 FOR I%=2 TO 4: FOR J%=2 TO 4:LOCATE I%,J%:PRINT" ";:LOCATE SH%-I%+1,SW%-J%+1:PRINT" ":NEXT:NEXT
140 REM Search maze using sensors
150 LOCATE 24,1: PRINT"Exploring...";
160 I%=1:J%=2:WHILEI%<>SH% OR J%<>SW%-1
170 GOSUB 390: MEMORY%=MEMORY%+1:ROUTE%(MEMORY%,1)=I%:ROUTE%(MEMORY%,2)=J%:VISITS%(I%,J%)=VISITS%(I%,J%)+1:IF MAZE$(I%,J%)="" THEN:GOSUB 470: REM Remember the route, how often you visit each cell and use sensors if you haven't been there before
180 B$=MAZE$(I%,J%)
190 IF VISITS%(I%,J%)=1 THEN 230
200 FOR K%=MEMORY%-1 TO 1 STEP -1: IF ROUTE%(K%,1)=I% AND ROUTE%(K%,2)=J% THEN MEMORY%=K%:K%=1: REM If you've been her before, forget the route that brought you back here
210 NEXT
220 ON VISITS%(I%,J%)-INT((VISITS%(I%,J%)-1)/4)*4 GOTO 230,240,250,260
230 IF MID$(B$,1,1)="0" THEN: GOSUB 430:I%=I%+1:GOTO 270
240 IF MID$(B$,2,1)="0" THEN:GOSUB 430:J%=J%+1:GOTO 270
250 IF MID$(B$,3,1)="0" THEN: GOSUB 430:I%=I%-1:GOTO 270
260 IF MID$(B$,4,1)="0" THEN:GOSUB 430:J%=J%-1
270 WEND
280 GOSUB 390: MEMORY%=MEMORY%+1:ROUTE%(MEMORY%,1)=I%:ROUTE%(MEMORY%,2)=J%
290 LOCATE 24,1:PRINT"Got there !";
300 REM Re-run maze
310 GOSUB 430
320 FOR K%=1 TO MEMORY%
330 I%=ROUTE%(K%,1):J%=ROUTE%(K%,2)
340 GOSUB 390
350 FOR Q=1 TO 25:X=X+1-1:REM delay
360 GOSUB 430
370 NEXT: GOSUB 390
380 LOCATE 24,1: PRINT"How's that !";:LOCATE 1,1:END
390 REM Subroutine to position robot at I%,J%
410 LOCATE I%,J%:PRINT ROBOT$;
420 RETURN
430 REM Subroutine to delete robot from I%,J%
450 LOCATE I%,J%:PRINT" ";
460 RETURN
470 REM Use sensors to build up map at position I%,J% and place in array MAZE$
480 VERTICAL%=I%:HORIZONTAL%=J%
500 IF SCREEN(VERTICAL%,HORIZONTAL%-1) = 219 THEN: MAZE%(I%,J%)="1" ELSE MAZE$(I%,J%)="0"
510 IF MEMORY%=1 THEN: MAZE$(I%,J%)="1"+MAZE$(I%,J%):GOTO 540
520 IF SCREEN(VERTICAL%-1,HORIZONTAL%) = 219 THEN: MAZE%(I%,J%)="1"+MAZE$(I%,J%) ELSE MAZE$(I%,J%)="0"+MAZE$(I%,J%)
540 IF SCREEN(VERTICAL%,HORIZONTAL%+1) = 219 THEN: MAZE%(I%,J%)="1"+MAZE$(I%,J%) ELSE MAZE$(I%,J%)="0"+MAZE$(I%,J%)
560 IF SCREEN(VERTICAL%+1,HORIZONTAL%) = 219 THEN: MAZE%(I%,J%)="1"+MAZE$(I%,J%) ELSE MAZE$(I%,J%)="0"+MAZE$(I%,J%)
580 RETURN

