REM **********************************
REM ** Listing 5.1                  **
REM ** Robot Maze Learner           **
REM **********************************

REM SW% is Screen Width and SH% is Screen Height
SW%=80
SH%=23
DIM MAZE$(SH%,SW%),VISITS%(SH%,SW%),ROUTE%(2000,2)

CLS
REM These are IBM Special Characters.
ROBOT$=CHR$(1)
WALL$=CHR$(219)

FOR I%=3 TO SW%
LOCATE 1,I%:PRINT WALL$;
NEXT

FOR J%=2 TO SH%
LOCATE J%,SW%:PRINT WALL$;
NEXT

FOR I%=SW%-2 TO 1 STEP -1
LOCATE SH%,I%:PRINT WALL$;
NEXT

FOR J%=SH%-1 TO 1 STEP -1
LOCATE J%,1:PRINT WALL$;
NEXT

RANDOMIZE TIMER
FOR I%=2 TO SW%-1
FOR J%=2 TO SH%-1
IF RND <.25 THEN LOCATE J%,I%:PRINT WALL$;
NEXT
NEXT

FOR I%=2 TO 4
FOR J%=2 TO 4
LOCATE I%,J%:PRINT" ";
LOCATE SH%-I%+1,SW%-J%+1
PRINT" "
NEXT
NEXT

REM Search maze using sensors
LOCATE 24,1
PRINT"Exploring...";
I%=1
J%=2

WHILE I%<>SH% OR J%<>SW%-1
GOSUB 390
MEMORY%=MEMORY%+1
ROUTE%(MEMORY%,1)=I%
ROUTE%(MEMORY%,2)=J%
VISITS%(I%,J%)=VISITS%(I%,J%)+1
IF MAZE$(I%,J%)="" THEN:GOSUB 470

REM Remember the route, how often you visit each cell and use sensors if you haven't been there before
B$=MAZE$(I%,J%)
IF VISITS%(I%,J%)=1 THEN 230

FOR K%=MEMORY%-1 TO 1 STEP -1
REM If you've been here before, forget the route that brought you back here
IF ROUTE%(K%,1)=I% AND ROUTE%(K%,2)=J% THEN MEMORY%=K%:K%=1
NEXT

ON VISITS%(I%,J%)-INT((VISITS%(I%,J%)-1)/4)*4 GOTO 230,240,250,260

230 IF MID$(B$,1,1)="0" THEN:GOSUB 430
I%=I%+1
GOTO 270

240 IF MID$(B$,2,1)="0" THEN:GOSUB 430
J%=J%+1
GOTO 270

250 IF MID$(B$,3,1)="0" THEN:GOSUB 430
I%=I%-1
GOTO 270

260 IF MID$(B$,4,1)="0" THEN:GOSUB 430
J%=J%-1

270 WEND

GOSUB 390

MEMORY%=MEMORY%+1
ROUTE%(MEMORY%,1)=I%
ROUTE%(MEMORY%,2)=J%
LOCATE 24,1:PRINT"Got there !";

REM Re-run maze
GOSUB 430

FOR K%=1 TO MEMORY%
I%=ROUTE%(K%,1)
J%=ROUTE%(K%,2)
GOSUB 390

REM delay
FOR Q=1 TO 25
X=X+1-1
NEXT

GOSUB 430
NEXT

GOSUB 390
LOCATE 24,1:PRINT"How's that !";
LOCATE 1,1
END

390 REM Subroutine to position robot at I%,J%
LOCATE I%,J%:PRINT ROBOT$;
RETURN

430 REM Subroutine to delete robot from I%,J%
LOCATE I%,J%:PRINT" ";
RETURN

470 REM Use sensors to build up map at position I%,J% and place in array MAZE$
VERTICAL%=I%
HORIZONTAL%=J%

IF SCREEN(VERTICAL%,HORIZONTAL%-1) = 219 THEN
MAZE%(I%,J%)="1" ELSE MAZE$(I%,J%)="0"

IF MEMORY%=1 THEN
MAZE$(I%,J%)="1"+MAZE$(I%,J%)
GOTO 540

IF SCREEN(VERTICAL%-1,HORIZONTAL%) = 219 THEN
MAZE%(I%,J%)="1"+MAZE$(I%,J%) ELSE MAZE$(I%,J%)="0"+MAZE$(I%,J%)

IF SCREEN(VERTICAL%,HORIZONTAL%+1) = 219 THEN
MAZE%(I%,J%)="1"+MAZE$(I%,J%) ELSE MAZE$(I%,J%)="0"+MAZE$(I%,J%)

IF SCREEN(VERTICAL%+1,HORIZONTAL%) = 219 THEN
MAZE%(I%,J%)="1"+MAZE$(I%,J%) ELSE MAZE$(I%,J%)="0"+MAZE$(I%,J%)
RETURN

