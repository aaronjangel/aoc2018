      * Advent of Code 2018, Day 1, in COBOL.
      *
      * This is slow as fuck.
      *
      * It is also the first COBOL program that I have ever written. The
      * fact that it actually spits out the right answers is, frankly,
      * amazeballs to me.
      *
      * I mean, if we're going to time travel...might as well try COBOL.
      *
       IDENTIFICATION DIVISION.
       PROGRAM-ID. AOC1801.
      *
       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT PUZZLE ASSIGN TO 'input'
           ORGANIZATION IS LINE SEQUENTIAL
           ACCESS IS SEQUENTIAL.
      *
       DATA DIVISION.
       FILE SECTION.
       FD PUZZLE
          LABEL RECORDS ARE OMITTED
          DATA RECORD IS PUZZLE-CLUE
          RECORD IS VARYING IN SIZE FROM 2 TO 7
              DEPENDING ON WS-RECORD-SIZE.
       01 PUZZLE-CLUE          PIC X(7).
      *
       WORKING-STORAGE SECTION.
       01 WS-RECORD-SIZE       PIC 9(4).
       01 WS-PART-NUM          PIC 9.
       01 WS-FREQ.
         05 WS-FREQ-SHFT       PIC S9(9)    VALUE 0.
         05 WS-FREQ-LAST       PIC S9(9)    VALUE 0.
         05 WS-FREQ-DISP       PIC -ZZZZZZZ9.
         05 WS-FREQ-MATCH      PIC X        VALUE 'N'.
       01 WS-PUZZLE-TABLE.
         05 WS-PUZZLE-COUNT    PIC 999999   VALUE 0.
         05 WS-PUZZLE-HIST     PIC X(7)
                               OCCURS 1004 TIMES
                               INDEXED BY P.
       01 WS-FREQ-HIST-TABLE.
         05 WS-FREQ-HIST-IDX   PIC 999999.
         05 WS-FREQ-HIST       PIC S9(9)    VALUE 0
                               OCCURS 150000 TIMES
                               INDEXED BY F.
       01 WS-EOF               PIC X(1)     VALUE 'N'.
      *
       PROCEDURE DIVISION.
       MAIN.
           DISPLAY 'Advent of Code 2018, Day 1'
           PERFORM PREPARE-RECORDS THRU PREPARE-RECORDS-EXIT.
           PERFORM PART-1 THRU PART-1-EXIT.
           PERFORM PART-2 THRU PART-2-EXIT.
           STOP RUN.
      *
       PREPARE-RECORDS.
           OPEN INPUT PUZZLE.
           READ PUZZLE RECORD.
           PERFORM PROCESS-RECORD
               VARYING P FROM 1
                   BY 1 UNTIL WS-EOF = 'Y'.
           CLOSE PUZZLE.
           SUBTRACT 1 FROM P.
           MOVE P TO WS-PUZZLE-COUNT.
           SET P TO 1.
      *
       PREPARE-RECORDS-EXIT.
           EXIT.
      *
       PROCESS-RECORD.
           MOVE PUZZLE-CLUE TO WS-PUZZLE-HIST(P).
           READ PUZZLE RECORD
               AT END MOVE 'Y' TO WS-EOF
           END-READ.
      *
       PROCESS-RECORD-EXIT.
           EXIT.
      *
       PART-1.
           MOVE '1' TO WS-PART-NUM.
           PERFORM FREQUENCY-SHIFT THRU FREQUENCY-SHIFT-EXIT
               VARYING P FROM 1
                   BY 1 UNTIL P > WS-PUZZLE-COUNT.
           PERFORM DISPLAY-RESULT.
      *
       PART-1-EXIT.
           EXIT.
      *
       PART-2.
           MOVE '2' TO WS-PART-NUM.
           PERFORM FREQUENCY-SHIFT THRU FREQUENCY-SHIFT-EXIT
               VARYING P FROM 1
                   BY 1 UNTIL WS-FREQ-MATCH = 'Y'.
           PERFORM DISPLAY-RESULT.
      *
       PART-2-EXIT.
           EXIT.
      *
       DISPLAY-RESULT.
           MOVE WS-FREQ-LAST TO WS-FREQ-DISP.
           DISPLAY 'Part ' WS-PART-NUM ': ' WS-FREQ-DISP.
      *
       DISPLAY-RESULT-EXIT.
           EXIT.
      *
       FREQUENCY-SHIFT.
           IF P > WS-PUZZLE-COUNT SET P TO 1.
           MOVE WS-PUZZLE-HIST(P) TO WS-FREQ-SHFT.
           ADD WS-FREQ-SHFT TO WS-FREQ-LAST.
           MOVE F TO WS-FREQ-HIST-IDX.
           SET F TO 1.
           SEARCH WS-FREQ-HIST
               WHEN WS-FREQ-HIST(F) = WS-FREQ-LAST
                   MOVE 'Y' TO WS-FREQ-MATCH
           END-SEARCH.
           MOVE WS-FREQ-HIST-IDX TO F.
           SET F UP BY 1.
           MOVE WS-FREQ-LAST TO WS-FREQ-HIST(F).
      *
       FREQUENCY-SHIFT-EXIT.
           EXIT.
