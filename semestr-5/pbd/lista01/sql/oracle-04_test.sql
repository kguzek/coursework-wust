-- SQL*Plus: fail on unexpected results and leave the seed data unchanged.
WHENEVER SQLERROR EXIT SQL.SQLCODE ROLLBACK
SET SERVEROUTPUT ON

DECLARE
    joined_on DATE;

    PROCEDURE expect_failure(label VARCHAR2, statement VARCHAR2, expected_code NUMBER) IS
    BEGIN
        EXECUTE IMMEDIATE statement;
        RAISE_APPLICATION_ERROR(-20000, 'Unexpected acceptance: ' || label);
    EXCEPTION
        WHEN OTHERS THEN
            IF SQLCODE != expected_code THEN
                RAISE;
            END IF;
            DBMS_OUTPUT.PUT_LINE('PASS: ' || label || ' (SQLCODE ' || SQLCODE || ')');
    END;
BEGIN
    SAVEPOINT test_start;

    expect_failure('minimum > 5',
        'INSERT INTO funkcje VALUES (''BAD_MIN'',5,20)', -2290);
    expect_failure('maximum < 200',
        'INSERT INTO funkcje VALUES (''BAD_MAX'',6,200)', -2290);
    expect_failure('maximum >= minimum',
        'INSERT INTO funkcje VALUES (''BAD_RANGE'',20,19)', -2290);
    expect_failure('hostility between 1 and 10',
        'INSERT INTO wrogowie VALUES (''BAD'',11,NULL,NULL)', -2290);
    expect_failure('sex M or D',
        'INSERT INTO kocury (imie,pseudo,plec) VALUES (''TEST'',''TEST'',''X'')', -2290);
    expect_failure('unique cat primary key',
        'INSERT INTO kocury (imie,pseudo) VALUES (''TEST'',''TYGRYS'')', -1);
    expect_failure('existing gang reference',
        'INSERT INTO kocury (imie,pseudo,nr_bandy) VALUES (''TEST'',''TEST'',99)', -2291);
    expect_failure('unique territory',
        'INSERT INTO bandy VALUES (6,''TEST'',''POLE'',NULL)', -1);
    expect_failure('unique gang leader',
        'INSERT INTO bandy VALUES (6,''TEST'',NULL,''TYGRYS'')', -1);
    expect_failure('required cat name',
        'INSERT INTO kocury (pseudo) VALUES (''TEST'')', -1400);
    expect_failure('unique cat/enemy pair',
        'INSERT INTO wrogowie_kocurow VALUES (''TYGRYS'',''KAZIO'',DATE ''2026-01-01'',NULL)', -1);
    expect_failure('required incident date',
        'INSERT INTO wrogowie_kocurow VALUES (''TYGRYS'',''BUREK'',NULL,NULL)', -1400);

    INSERT INTO kocury (imie,pseudo) VALUES ('TEST','TEST');
    SELECT w_stadku_od INTO joined_on FROM kocury WHERE pseudo = 'TEST';
    IF joined_on IS NULL OR TRUNC(joined_on) != TRUNC(SYSDATE) THEN
        RAISE_APPLICATION_ERROR(-20001, 'Default date failed');
    END IF;
    DBMS_OUTPUT.PUT_LINE('PASS: default date and optional attributes');

    INSERT INTO bandy VALUES (6,'TEST',NULL,NULL);
    INSERT INTO bandy VALUES (7,'TEST2',NULL,NULL);
    DBMS_OUTPUT.PUT_LINE('PASS: multiple NULLs in UNIQUE columns');

    INSERT INTO funkcje VALUES ('TEST_LOW',6,6);
    INSERT INTO funkcje VALUES ('TEST_HIGH',6,199);
    DBMS_OUTPUT.PUT_LINE('PASS: valid mouse-range boundaries');

    ROLLBACK TO test_start;
    DBMS_OUTPUT.PUT_LINE('PASS: all test data rolled back');
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK TO test_start;
        RAISE;
END;
/
