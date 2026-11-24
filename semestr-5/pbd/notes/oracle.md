# Notatki dokumentacja – Oracle (23ai)

## Spis treści

- [1. DDL](#1-ddl)
  - [1.1 CREATE TABLE](#11-create-table)
  - [1.2 Data types](#12-data-types)
  - [1.3 PRIMARY KEY](#13-primary-key)
  - [1.4 NOT NULL / UNIQUE](#14-not-null--unique)
  - [1.5 CHECK](#15-check)
  - [1.6 REFERENCES](#16-references)
  - [1.7 DEFAULT](#17-default)
  - [1.8 ALTER TABLE ADD CONSTRAINT](#18-alter-table-add-constraint)
  - [1.9 DEFERRABLE](#19-deferrable)
  - [1.10 ALTER TABLE columns](#110-alter-table-columns)
  - [1.11 DROP TABLE](#111-drop-table)
- [2. DML](#2-dml)
  - [2.1 INSERT … VALUES](#21-insert--values)
  - [2.2 INSERT ALL](#22-insert-all)
  - [2.3 DATE literal](#23-date-literal)
  - [2.4 UPDATE](#24-update)
  - [2.5 DELETE](#25-delete)
  - [2.6 COMMIT / ROLLBACK](#26-commit--rollback)
- [3. SELECT basics](#3-select-basics)
  - [3.1 SELECT … FROM](#31-select--from)
  - [3.2 Column alias](#32-column-alias)
  - [3.3 Table alias](#33-table-alias)
  - [3.4 DISTINCT](#34-distinct)
  - [3.5 WHERE](#35-where)
  - [3.6 BETWEEN](#36-between)
  - [3.7 IN](#37-in)
  - [3.8 LIKE](#38-like)
  - [3.9 IS NULL](#39-is-null)
  - [3.10 ORDER BY](#310-order-by)
  - [3.11 FETCH FIRST](#311-fetch-first)
  - [3.12 ROWNUM](#312-rownum)
  - [3.13 DUAL](#313-dual)
- [4. Strings](#4-strings)
  - [4.1 ||](#41-)
  - [4.2 CONCAT](#42-concat)
  - [4.3 LOWER / UPPER / INITCAP](#43-lower--upper--initcap)
  - [4.4 LENGTH](#44-length)
  - [4.5 INSTR](#45-instr)
  - [4.6 SUBSTR](#46-substr)
  - [4.7 LPAD / RPAD](#47-lpad--rpad)
  - [4.8 REPLACE](#48-replace)
  - [4.9 REGEXP_REPLACE](#49-regexp_replace)
  - [4.10 TRIM](#410-trim)
  - [4.11 Replace one character](#411-replace-one-character)
  - [4.12 Empty string](#412-empty-string)
- [5. NULL handling](#5-null-handling)
  - [5.1 NVL](#51-nvl)
  - [5.2 COALESCE](#52-coalesce)
  - [5.3 NVL2](#53-nvl2)
  - [5.4 NULLIF](#54-nullif)
  - [5.5 Comparing with NULL](#55-comparing-with-null)
- [6. Numbers](#6-numbers)
  - [6.1 ROUND](#61-round)
  - [6.2 TRUNC](#62-trunc)
  - [6.3 MOD](#63-mod)
  - [6.4 CEIL / FLOOR](#64-ceil--floor)
  - [6.5 Division](#65-division)
- [7. Dates](#7-dates)
  - [7.1 SYSDATE / CURRENT_DATE](#71-sysdate--current_date)
  - [7.2 TRUNC(date)](#72-truncdate)
  - [7.3 EXTRACT](#73-extract)
  - [7.4 Date arithmetic](#74-date-arithmetic)
  - [7.5 ADD_MONTHS](#75-add_months)
  - [7.6 MONTHS_BETWEEN](#76-months_between)
  - [7.7 LAST_DAY](#77-last_day)
  - [7.8 NEXT_DAY](#78-next_day)
  - [7.9 INTERVAL](#79-interval)
- [8. Conversions](#8-conversions)
  - [8.1 TO_CHAR(number)](#81-to_charnumber)
  - [8.2 TO_CHAR(date, format)](#82-to_chardate-format)
  - [8.3 TO_NUMBER](#83-to_number)
  - [8.4 TO_DATE](#84-to_date)
  - [8.5 CAST](#85-cast)
- [9. Conditionals](#9-conditionals)
  - [9.1 CASE WHEN](#91-case-when)
  - [9.2 CASE value](#92-case-value)
  - [9.3 DECODE](#93-decode)
- [10. Grouping](#10-grouping)
  - [10.1 COUNT](#101-count)
  - [10.2 SUM / AVG / MIN / MAX](#102-sum--avg--min--max)
  - [10.3 GROUP BY](#103-group-by)
  - [10.4 HAVING](#104-having)
  - [10.5 Conditional COUNT](#105-conditional-count)
  - [10.6 LISTAGG](#106-listagg)
  - [10.7 Group by expression](#107-group-by-expression)
  - [10.8 ROLLUP](#108-rollup)
- [11. Joins](#11-joins)
  - [11.1 JOIN](#111-join)
  - [11.2 LEFT JOIN](#112-left-join)
  - [11.3 RIGHT JOIN](#113-right-join)
  - [11.4 FULL JOIN](#114-full-join)
  - [11.5 CROSS JOIN](#115-cross-join)
  - [11.6 USING / NATURAL](#116-using--natural)
  - [11.7 Self join](#117-self-join)
  - [11.8 Join chain](#118-join-chain)
  - [11.9 Join to a fixed row](#119-join-to-a-fixed-row)
  - [11.10 Anti-join](#1110-anti-join)
  - [11.11 (+) outer join](#1111--outer-join)
  - [11.12 LEFT JOIN + WHERE trap](#1112-left-join--where-trap)
- [12. Set operators](#12-set-operators)
  - [12.1 UNION / UNION ALL](#121-union--union-all)
  - [12.2 INTERSECT](#122-intersect)
  - [12.3 MINUS](#123-minus)
  - [12.4 ORDER BY in set operations](#124-order-by-in-set-operations)
- [13. Subqueries](#13-subqueries)
  - [13.1 Scalar subquery](#131-scalar-subquery)
  - [13.2 Subquery in SELECT / HAVING](#132-subquery-in-select--having)
  - [13.3 IN (subquery)](#133-in-subquery)
  - [13.4 NOT IN + NULL trap](#134-not-in--null-trap)
  - [13.5 EXISTS / NOT EXISTS](#135-exists--not-exists)
  - [13.6 ALL](#136-all)
  - [13.7 ANY](#137-any)
  - [13.8 Subquery in FROM](#138-subquery-in-from)
  - [13.9 WITH (CTE)](#139-with-cte)
- [14. Hierarchical queries](#14-hierarchical-queries)
  - [14.1 START WITH](#141-start-with)
  - [14.2 CONNECT BY PRIOR](#142-connect-by-prior)
  - [14.3 LEVEL](#143-level)
  - [14.4 ORDER SIBLINGS BY](#144-order-siblings-by)
  - [14.5 WHERE vs CONNECT BY condition](#145-where-vs-connect-by-condition)
  - [14.6 CONNECT_BY_ROOT](#146-connect_by_root)
  - [14.7 SYS_CONNECT_BY_PATH](#147-sys_connect_by_path)
  - [14.8 CONNECT_BY_ISLEAF](#148-connect_by_isleaf)
  - [14.9 Recursive WITH](#149-recursive-with)
  - [14.10 Row generator](#1410-row-generator)
- [15. Window functions (OVER)](#15-window-functions-over)
  - [15.1 OVER ()](#151-over-)
  - [15.2 PARTITION BY](#152-partition-by)
  - [15.3 ROW_NUMBER](#153-row_number)
  - [15.4 RANK / DENSE_RANK](#154-rank--dense_rank)
  - [15.5 Running total](#155-running-total)
  - [15.6 ROWS BETWEEN](#156-rows-between)
  - [15.7 LAG / LEAD](#157-lag--lead)
  - [15.8 FIRST_VALUE](#158-first_value)
  - [15.9 RATIO_TO_REPORT](#159-ratio_to_report)
  - [15.10 Top-N per group](#1510-top-n-per-group)
- [16. Pivot](#16-pivot)
  - [16.1 PIVOT](#161-pivot)
  - [16.2 PIVOT with several aggregates](#162-pivot-with-several-aggregates)
  - [16.3 UNPIVOT](#163-unpivot)
  - [16.4 Pivot with CASE](#164-pivot-with-case)
- [17. SQL*Plus](#17-sqlplus)
  - [17.1 SET LINESIZE / PAGESIZE](#171-set-linesize--pagesize)
  - [17.2 COLUMN FORMAT](#172-column-format)
  - [17.3 @file](#173-file)
  - [17.4 /](#174-)
  - [17.5 DESC](#175-desc)

## 1. DDL

### 1.1 CREATE TABLE

Creates a table; `IF NOT EXISTS` works since 23ai.

```sql
CREATE TABLE IF NOT EXISTS wrogowie (imie_wroga VARCHAR2(15) PRIMARY KEY, gatunek VARCHAR2(15));
```

### 1.2 Data types

`NUMBER(p)`, `VARCHAR2(n)` and `DATE`, which also stores the time.

```sql
pseudo VARCHAR2(15), przydzial_myszy NUMBER(3), w_stadku_od DATE
```

### 1.3 PRIMARY KEY

Unique, non-null row id; a composite key goes at table level.

```sql
PRIMARY KEY (pseudo, imie_wroga)
```

### 1.4 NOT NULL / UNIQUE

`UNIQUE` allows many `NULL`s in Oracle.

```sql
nazwa VARCHAR2(20) NOT NULL, teren VARCHAR2(15) UNIQUE
```

### 1.5 CHECK

A column CHECK sees only its own column; multi-column checks go at table level.

```sql
plec VARCHAR2(1) CHECK (plec IN ('M', 'D')),
CONSTRAINT fu_max_ch CHECK (max_myszy >= min_myszy)
```

### 1.6 REFERENCES

Foreign key, can point to the same table.

```sql
szef VARCHAR2(15) REFERENCES kocury(pseudo)
```

### 1.7 DEFAULT

Value used when the column is left out of an INSERT.

```sql
w_stadku_od DATE DEFAULT SYSDATE
```

### 1.8 ALTER TABLE ADD CONSTRAINT

Adds a constraint later, e.g. to break the `bandy` ↔ `kocury` cycle.

```sql
ALTER TABLE bandy ADD CONSTRAINT bandy_szef_fk FOREIGN KEY (szef_bandy) REFERENCES kocury(pseudo);
```

### 1.9 DEFERRABLE

Checks the constraint at COMMIT instead of after each statement.

```sql
FOREIGN KEY (szef_bandy) REFERENCES kocury(pseudo) DEFERRABLE INITIALLY DEFERRED
```

### 1.10 ALTER TABLE columns

Adds, changes or removes a column.

```sql
ALTER TABLE kocury ADD (ulubiona VARCHAR2(20));
ALTER TABLE kocury MODIFY (ulubiona VARCHAR2(30));
ALTER TABLE kocury DROP COLUMN ulubiona;
```

### 1.11 DROP TABLE

Removes a table; `CASCADE CONSTRAINTS` also drops FKs pointing at it.

```sql
DROP TABLE kocury CASCADE CONSTRAINTS;
```

## 2. DML

### 2.1 INSERT … VALUES

Inserts rows; several rows in one `VALUES` works since 23ai.

```sql
INSERT INTO funkcje (funkcja, min_myszy, max_myszy) VALUES ('SZEFUNIO', 90, 110), ('BANDZIOR', 70, 90);
```

### 2.2 INSERT ALL

Multi-row insert for older Oracle versions.

```sql
INSERT ALL INTO funkcje VALUES ('LOWCZY', 60, 70) INTO funkcje VALUES ('LAPACZ', 50, 60) SELECT * FROM dual;
```

### 2.3 DATE literal

ISO date constant.

```sql
INSERT INTO kocury (imie, pseudo, w_stadku_od) VALUES ('JACEK', 'PLACEK', DATE '2008-12-01');
```

### 2.4 UPDATE

Changes values in matching rows.

```sql
UPDATE bandy SET szef_bandy = 'TYGRYS' WHERE nr_bandy = 1;
```

### 2.5 DELETE

Removes matching rows.

```sql
DELETE FROM wrogowie_kocurow WHERE imie_wroga = 'KAZIO';
```

### 2.6 COMMIT / ROLLBACK

DML isn't auto-committed; these save or undo the transaction.

```sql
COMMIT;
```

## 3. SELECT basics

### 3.1 SELECT … FROM

Picks columns from a table.

```sql
SELECT imie, funkcja FROM kocury;
```

### 3.2 Column alias

Double quotes keep spaces and letter case.

```sql
SELECT przydzial_myszy AS "Zjada" FROM kocury;
```

### 3.3 Table alias

Written without `AS` (in Oracle `AS` there is an error).

```sql
SELECT K.imie FROM kocury K;
```

### 3.4 DISTINCT

Removes duplicate rows.

```sql
SELECT DISTINCT funkcja FROM kocury;
```

### 3.5 WHERE

Filters rows.

```sql
SELECT imie FROM kocury WHERE plec = 'D' AND przydzial_myszy >= 55;
```

### 3.6 BETWEEN

Range check, both ends inclusive.

```sql
SELECT imie FROM kocury WHERE w_stadku_od BETWEEN DATE '2005-09-01' AND DATE '2007-07-31';
```

### 3.7 IN

Matches any value from a list.

```sql
SELECT imie FROM kocury WHERE funkcja IN ('MILUSIA', 'KOT');
```

### 3.8 LIKE

Pattern match (`%` any text, `_` one char); case-sensitive, no `ILIKE`.

```sql
SELECT pseudo FROM kocury WHERE LOWER(pseudo) LIKE '%a%';
```

### 3.9 IS NULL

The only correct way to test for `NULL`.

```sql
SELECT imie_wroga FROM wrogowie WHERE lapowka IS NULL;
```

### 3.10 ORDER BY

Sorts the result; can use column aliases.

```sql
SELECT pseudo, w_stadku_od FROM kocury ORDER BY w_stadku_od DESC, pseudo;
```

### 3.11 FETCH FIRST

Top-N rows after sorting.

```sql
SELECT pseudo FROM kocury ORDER BY przydzial_myszy DESC FETCH FIRST 3 ROWS ONLY;
```

### 3.12 ROWNUM

Row number assigned before `ORDER BY` runs.

```sql
SELECT pseudo FROM kocury WHERE ROWNUM <= 3;
```

### 3.13 DUAL

One-row dummy table for selecting values without a real table.

```sql
SELECT SYSDATE FROM dual;
```

## 4. Strings

### 4.1 ||

Concatenation; `NULL` acts like an empty string.

```sql
SELECT imie || ' zwany ' || pseudo FROM kocury;
```

### 4.2 CONCAT

Concatenation of exactly 2 arguments.

```sql
SELECT CONCAT(imie, pseudo) FROM kocury;
```

### 4.3 LOWER / UPPER / INITCAP

Changes letter case.

```sql
SELECT LOWER(pseudo), INITCAP(imie) FROM kocury;
```

### 4.4 LENGTH

Number of characters.

```sql
SELECT pseudo FROM kocury WHERE LENGTH(pseudo) > 4;
```

### 4.5 INSTR

Position of a substring (1-based), 0 when not found.

```sql
SELECT pseudo, INSTR(pseudo, 'A') FROM kocury;
```

### 4.6 SUBSTR

Substring from a position, with optional length.

```sql
SELECT SUBSTR(pseudo, 2, 3) FROM kocury;
```

### 4.7 LPAD / RPAD

Pads text to a length; handy for tree indentation.

```sql
SELECT LPAD(pseudo, 10, '*') FROM kocury;
```

### 4.8 REPLACE

Replaces all occurrences.

```sql
SELECT REPLACE(pseudo, 'A', '#') FROM kocury;
```

### 4.9 REGEXP_REPLACE

Regex replace; here only the 1st match, case-insensitive.

```sql
SELECT REGEXP_REPLACE(pseudo, 'a', '#', 1, 1, 'i') FROM kocury;
```

### 4.10 TRIM

Removes surrounding spaces.

```sql
SELECT TRIM('  TYGRYS  ') FROM dual;
```

### 4.11 Replace one character

Oracle's equivalent of Postgres `OVERLAY`.

```sql
SELECT SUBSTR(pseudo, 1, INSTR(pseudo, 'A') - 1) || '#' || SUBSTR(pseudo, INSTR(pseudo, 'A') + 1) FROM kocury WHERE pseudo LIKE '%A%';
```

### 4.12 Empty string

`''` is `NULL` in Oracle.

```sql
SELECT imie FROM kocury WHERE '' IS NULL;   -- all rows
```

## 5. NULL handling

### 5.1 NVL

Replaces `NULL` with a value.

```sql
SELECT przydzial_myszy + NVL(myszy_extra, 0) FROM kocury;
```

### 5.2 COALESCE

First non-`NULL` argument.

```sql
SELECT COALESCE(myszy_extra, przydzial_myszy, 0) FROM kocury;
```

### 5.3 NVL2

One value when not `NULL`, another when `NULL`.

```sql
SELECT NVL2(myszy_extra, 'ma extra', 'brak') FROM kocury;
```

### 5.4 NULLIF

Returns `NULL` when both arguments are equal.

```sql
SELECT NULLIF(przydzial_myszy, 0) FROM kocury;
```

### 5.5 Comparing with NULL

`= NULL` is never true; aggregates skip `NULL`s.

```sql
SELECT imie FROM kocury WHERE myszy_extra = NULL;   -- always 0 rows
```

## 6. Numbers

### 6.1 ROUND

Rounds, optionally to n decimal places.

```sql
SELECT ROUND(przydzial_myszy / 1.1), ROUND(przydzial_myszy / 1.1, 1) FROM kocury;
```

### 6.2 TRUNC

Cuts off decimals without rounding.

```sql
SELECT TRUNC(przydzial_myszy / 7) FROM kocury;
```

### 6.3 MOD

Remainder of division.

```sql
SELECT pseudo FROM kocury WHERE MOD(przydzial_myszy, 2) = 0;
```

### 6.4 CEIL / FLOOR

Rounds up / down to an integer.

```sql
SELECT CEIL(przydzial_myszy / 7), FLOOR(przydzial_myszy / 7) FROM kocury;
```

### 6.5 Division

No integer division: `5 / 2 = 2.5`.

```sql
SELECT 5 / 2 FROM dual;
```

## 7. Dates

### 7.1 SYSDATE / CURRENT_DATE

Current date with time.

```sql
SELECT SYSDATE, CURRENT_DATE FROM dual;
```

### 7.2 TRUNC(date)

Midnight of the day, or start of month/year with a format.

```sql
SELECT TRUNC(SYSDATE), TRUNC(SYSDATE, 'MM'), TRUNC(SYSDATE, 'YYYY') FROM dual;
```

### 7.3 EXTRACT

Gets the year, month or day as a number.

```sql
SELECT imie_wroga FROM wrogowie_kocurow WHERE EXTRACT(YEAR FROM data_incydentu) = 2009;
```

### 7.4 Date arithmetic

`+ n` adds days; date minus date gives days.

```sql
SELECT pseudo, SYSDATE - w_stadku_od, w_stadku_od + 7 FROM kocury;
```

### 7.5 ADD_MONTHS

Adds (or subtracts) months.

```sql
SELECT imie FROM kocury WHERE w_stadku_od <= ADD_MONTHS(SYSDATE, -15 * 12);
```

### 7.6 MONTHS_BETWEEN

Months between two dates (fractional).

```sql
SELECT pseudo FROM kocury WHERE MONTHS_BETWEEN(SYSDATE, w_stadku_od) > 15 * 12;
```

### 7.7 LAST_DAY

Last day of the date's month.

```sql
SELECT LAST_DAY(SYSDATE) FROM dual;
```

### 7.8 NEXT_DAY

First given weekday after a date; the day name depends on NLS language.

```sql
SELECT NEXT_DAY(LAST_DAY(SYSDATE) - 7, 'WEDNESDAY') FROM dual;   -- last Wednesday of the month
```

### 7.9 INTERVAL

Adds a time interval; fails on invalid dates (29 Feb), so prefer `ADD_MONTHS`.

```sql
SELECT w_stadku_od + INTERVAL '6' MONTH FROM kocury;
```

## 8. Conversions

### 8.1 TO_CHAR(number)

Number to text.

```sql
SELECT TO_CHAR(12 * przydzial_myszy) FROM kocury;
```

### 8.2 TO_CHAR(date, format)

Formats a date; `MONTH` is space-padded, `FM` removes the padding.

```sql
SELECT TO_CHAR(w_stadku_od, 'YYYY-MM-DD'), TO_CHAR(w_stadku_od, 'FMMONTH') FROM kocury;
```

### 8.3 TO_NUMBER

Text to number.

```sql
SELECT TO_NUMBER('42') + 1 FROM dual;
```

### 8.4 TO_DATE

Text to date using a format.

```sql
SELECT TO_DATE('07-01-2009', 'DD-MM-YYYY') FROM dual;
```

### 8.5 CAST

Standard type conversion.

```sql
SELECT CAST(przydzial_myszy AS VARCHAR2(10)) FROM kocury;
```

## 9. Conditionals

### 9.1 CASE WHEN

Conditions checked in order; all branches must return the same type.

```sql
SELECT CASE WHEN przydzial_myszy > 60 THEN 'powyzej 60' ELSE 'ponizej 60' END FROM kocury;
```

### 9.2 CASE value

Compares one expression against values.

```sql
SELECT CASE plec WHEN 'M' THEN 'Kocur' ELSE 'Kotka' END FROM kocury;
```

### 9.3 DECODE

Oracle shorthand for `CASE value`.

```sql
SELECT DECODE(plec, 'M', 'Kocur', 'D', 'Kotka', '?') FROM kocury;
```

## 10. Grouping

### 10.1 COUNT

`COUNT(*)` counts rows, `COUNT(col)` non-`NULL`s, `COUNT(DISTINCT col)` unique values.

```sql
SELECT COUNT(*), COUNT(myszy_extra), COUNT(DISTINCT nr_bandy) FROM kocury;
```

### 10.2 SUM / AVG / MIN / MAX

Aggregates over a group of rows.

```sql
SELECT SUM(przydzial_myszy), AVG(przydzial_myszy), MIN(w_stadku_od), MAX(przydzial_myszy) FROM kocury;
```

### 10.3 GROUP BY

One row per group; every non-aggregated column must be listed.

```sql
SELECT B.nr_bandy, B.nazwa, COUNT(*) FROM bandy B JOIN kocury K ON K.nr_bandy = B.nr_bandy GROUP BY B.nr_bandy, B.nazwa;
```

### 10.4 HAVING

Filters groups (`WHERE` filters rows before grouping).

```sql
SELECT pseudo FROM wrogowie_kocurow GROUP BY pseudo HAVING COUNT(*) >= 2;
```

### 10.5 Conditional COUNT

`COUNT(CASE …)` counts only rows matching the condition.

```sql
SELECT pseudo FROM wrogowie_kocurow WK JOIN wrogowie W ON W.imie_wroga = WK.imie_wroga GROUP BY pseudo HAVING COUNT(CASE WHEN W.gatunek = 'PIES' THEN 1 END) > 0;
```

### 10.6 LISTAGG

Joins a group's values into one string.

```sql
SELECT nr_bandy, LISTAGG(pseudo, ', ') WITHIN GROUP (ORDER BY pseudo) FROM kocury GROUP BY nr_bandy;
```

### 10.7 Group by expression

Groups by a computed value.

```sql
SELECT EXTRACT(MONTH FROM w_stadku_od), COUNT(*) FROM kocury GROUP BY EXTRACT(MONTH FROM w_stadku_od);
```

### 10.8 ROLLUP

Adds a total row (`NULL` in the grouped column).

```sql
SELECT nr_bandy, SUM(przydzial_myszy) FROM kocury GROUP BY ROLLUP (nr_bandy);
```

## 11. Joins

### 11.1 JOIN

Only rows with a match on both sides.

```sql
SELECT K.pseudo, B.nazwa FROM kocury K JOIN bandy B ON B.nr_bandy = K.nr_bandy;
```

### 11.2 LEFT JOIN

All rows from the left side, `NULL`s where nothing matches.

```sql
SELECT B.nazwa, K.pseudo FROM bandy B LEFT JOIN kocury K ON K.nr_bandy = B.nr_bandy;
```

### 11.3 RIGHT JOIN

All rows from the right side.

```sql
SELECT K.pseudo, B.nazwa FROM kocury K RIGHT JOIN bandy B ON B.nr_bandy = K.nr_bandy;
```

### 11.4 FULL JOIN

All rows from both sides.

```sql
SELECT S.pseudo, P.pseudo FROM kocury S FULL JOIN kocury P ON P.szef = S.pseudo;
```

### 11.5 CROSS JOIN

Every row combined with every row.

```sql
SELECT K.pseudo, F.funkcja FROM kocury K CROSS JOIN funkcje F;
```

### 11.6 USING / NATURAL

Joins on same-named columns; that column is then used without a prefix.

```sql
SELECT pseudo, nazwa FROM kocury JOIN bandy USING (nr_bandy);
```

### 11.7 Self join

Joins a table with itself (cat and its boss).

```sql
SELECT K.imie, S.imie AS szef FROM kocury K LEFT JOIN kocury S ON S.pseudo = K.szef;
```

### 11.8 Join chain

Each extra self join goes one level higher.

```sql
SELECT K.imie, S1.imie, S2.imie FROM kocury K LEFT JOIN kocury S1 ON S1.pseudo = K.szef LEFT JOIN kocury S2 ON S2.pseudo = S1.szef;
```

### 11.9 Join to a fixed row

Joins one specific row to compare every row against it.

```sql
SELECT K.imie FROM kocury K JOIN kocury J ON J.imie = 'JACEK' WHERE K.w_stadku_od < J.w_stadku_od;
```

### 11.10 Anti-join

`LEFT JOIN` + `IS NULL` finds rows with no match.

```sql
SELECT B.nazwa FROM bandy B LEFT JOIN kocury K ON K.nr_bandy = B.nr_bandy WHERE K.pseudo IS NULL;
```

### 11.11 (+) outer join

Old Oracle syntax; `(+)` marks the side that may be `NULL`.

```sql
SELECT B.nazwa, K.pseudo FROM bandy B, kocury K WHERE B.nr_bandy = K.nr_bandy(+);
```

### 11.12 LEFT JOIN + WHERE trap

A `WHERE` condition on the right table turns it into an inner join; put it in `ON`.

```sql
SELECT B.nazwa, K.pseudo FROM bandy B LEFT JOIN kocury K ON K.nr_bandy = B.nr_bandy AND K.plec = 'M';
```

## 12. Set operators

### 12.1 UNION / UNION ALL

Stacks results; `UNION` removes duplicates, `UNION ALL` doesn't.

```sql
SELECT pseudo FROM kocury WHERE plec = 'M' UNION ALL SELECT pseudo FROM kocury WHERE przydzial_myszy > 60;
```

### 12.2 INTERSECT

Rows present in both results.

```sql
SELECT pseudo FROM kocury WHERE plec = 'M' INTERSECT SELECT pseudo FROM wrogowie_kocurow;
```

### 12.3 MINUS

Rows from the first result but not the second (`EXCEPT` elsewhere).

```sql
SELECT nr_bandy FROM bandy MINUS SELECT nr_bandy FROM kocury;
```

### 12.4 ORDER BY in set operations

Written once at the end, using names from the first `SELECT`.

```sql
SELECT pseudo, 'Prominent' AS typ FROM kocury UNION ALL SELECT pseudo, 'Szarak' FROM kocury ORDER BY typ, pseudo;
```

## 13. Subqueries

### 13.1 Scalar subquery

Returns one value, usable like a constant.

```sql
SELECT pseudo FROM kocury WHERE przydzial_myszy > (SELECT AVG(przydzial_myszy) FROM kocury);
```

### 13.2 Subquery in SELECT / HAVING

Same value repeated per row or compared per group.

```sql
SELECT nr_bandy, AVG(przydzial_myszy) FROM kocury GROUP BY nr_bandy HAVING AVG(przydzial_myszy) > (SELECT AVG(przydzial_myszy) FROM kocury);
```

### 13.3 IN (subquery)

Matches any value the subquery returns.

```sql
SELECT imie FROM kocury WHERE nr_bandy IN (SELECT nr_bandy FROM bandy WHERE teren IN ('SAD', 'POLE'));
```

### 13.4 NOT IN + NULL trap

One `NULL` in the subquery makes the result empty.

```sql
SELECT pseudo FROM kocury WHERE pseudo NOT IN (SELECT szef FROM kocury WHERE szef IS NOT NULL);
```

### 13.5 EXISTS / NOT EXISTS

Checks if a correlated subquery returns any row; immune to `NULL`s.

```sql
SELECT K.pseudo FROM kocury K WHERE NOT EXISTS (SELECT 1 FROM kocury P WHERE P.szef = K.pseudo);
```

### 13.6 ALL

True if the condition holds for every value (empty set → true).

```sql
SELECT imie FROM kocury WHERE przydzial_myszy >= ALL (SELECT 3 * przydzial_myszy FROM kocury WHERE funkcja = 'MILUSIA');
```

### 13.7 ANY

True if the condition holds for at least one value (empty set → false).

```sql
SELECT imie FROM kocury WHERE przydzial_myszy > ANY (SELECT przydzial_myszy FROM kocury WHERE funkcja = 'KOT');
```

### 13.8 Subquery in FROM

Uses a query result as a table.

```sql
SELECT * FROM (SELECT nr_bandy, SUM(przydzial_myszy) AS suma FROM kocury GROUP BY nr_bandy) WHERE suma > 200;
```

### 13.9 WITH (CTE)

Names a subquery so it can be reused.

```sql
WITH sumy AS (SELECT nr_bandy, SUM(przydzial_myszy) AS suma FROM kocury GROUP BY nr_bandy) SELECT * FROM sumy WHERE suma > 200;
```

## 14. Hierarchical queries

### 14.1 START WITH

Picks the root rows of the tree.

```sql
SELECT pseudo FROM kocury START WITH szef IS NULL CONNECT BY PRIOR pseudo = szef;
```

### 14.2 CONNECT BY PRIOR

Defines the parent–child link; `PRIOR` marks the parent's column.

```sql
SELECT pseudo FROM kocury START WITH pseudo = 'ZERO' CONNECT BY PRIOR szef = pseudo;   -- upwards: cat → bosses
```

### 14.3 LEVEL

Depth in the tree, 1 for the root.

```sql
SELECT LEVEL, LPAD(' ', 4 * (LEVEL - 1)) || pseudo FROM kocury START WITH szef IS NULL CONNECT BY PRIOR pseudo = szef;
```

### 14.4 ORDER SIBLINGS BY

Sorts children of each node while keeping the tree order.

```sql
SELECT pseudo FROM kocury START WITH funkcja = 'BANDZIOR' CONNECT BY PRIOR pseudo = szef ORDER SIBLINGS BY pseudo;
```

### 14.5 WHERE vs CONNECT BY condition

`WHERE` hides single rows; a condition in `CONNECT BY` cuts whole branches.

```sql
SELECT pseudo FROM kocury START WITH szef IS NULL CONNECT BY PRIOR pseudo = szef AND plec = 'M';
```

### 14.6 CONNECT_BY_ROOT

Value from the root row of the current path.

```sql
SELECT CONNECT_BY_ROOT imie, imie FROM kocury START WITH funkcja = 'KOT' CONNECT BY PRIOR szef = pseudo;
```

### 14.7 SYS_CONNECT_BY_PATH

Path from root to the current row as one string.

```sql
SELECT SYS_CONNECT_BY_PATH(imie, ' | ') FROM kocury START WITH funkcja = 'KOT' CONNECT BY PRIOR szef = pseudo;
```

### 14.8 CONNECT_BY_ISLEAF

1 if the row has no children.

```sql
SELECT pseudo FROM kocury WHERE CONNECT_BY_ISLEAF = 1 START WITH szef IS NULL CONNECT BY PRIOR pseudo = szef;
```

### 14.9 Recursive WITH

Standard SQL recursion; Oracle needs the column list.

```sql
WITH drzewo (pseudo, poziom) AS (SELECT pseudo, 1 FROM kocury WHERE szef IS NULL UNION ALL SELECT K.pseudo, D.poziom + 1 FROM kocury K JOIN drzewo D ON K.szef = D.pseudo) SELECT * FROM drzewo;
```

### 14.10 Row generator

Generates numbers 1..n.

```sql
SELECT LEVEL FROM dual CONNECT BY LEVEL <= 12;
```

## 15. Window functions (OVER)

### 15.1 OVER ()

Aggregate over all rows without collapsing them.

```sql
SELECT pseudo, przydzial_myszy, SUM(przydzial_myszy) OVER () FROM kocury;
```

### 15.2 PARTITION BY

Aggregate per group, kept on every row.

```sql
SELECT pseudo, ROUND(100 * przydzial_myszy / SUM(przydzial_myszy) OVER (PARTITION BY nr_bandy)) AS proc FROM kocury;
```

### 15.3 ROW_NUMBER

Numbers rows 1, 2, 3… with no ties.

```sql
SELECT pseudo, ROW_NUMBER() OVER (PARTITION BY nr_bandy ORDER BY przydzial_myszy DESC) FROM kocury;
```

### 15.4 RANK / DENSE_RANK

Ranks with ties: `RANK` 1,2,2,4 and `DENSE_RANK` 1,2,2,3.

```sql
SELECT pseudo, RANK() OVER (ORDER BY przydzial_myszy DESC), DENSE_RANK() OVER (ORDER BY przydzial_myszy DESC) FROM kocury;
```

### 15.5 Running total

`ORDER BY` inside `OVER` makes the aggregate cumulative.

```sql
SELECT pseudo, SUM(przydzial_myszy) OVER (ORDER BY w_stadku_od) FROM kocury;
```

### 15.6 ROWS BETWEEN

Sets exactly which rows the window covers.

```sql
SELECT pseudo, AVG(przydzial_myszy) OVER (ORDER BY w_stadku_od ROWS BETWEEN 1 PRECEDING AND CURRENT ROW) FROM kocury;
```

### 15.7 LAG / LEAD

Value from the previous / next row.

```sql
SELECT pseudo, LAG(pseudo) OVER (ORDER BY w_stadku_od), LEAD(pseudo) OVER (ORDER BY w_stadku_od) FROM kocury;
```

### 15.8 FIRST_VALUE

First value in the window.

```sql
SELECT pseudo, FIRST_VALUE(pseudo) OVER (PARTITION BY nr_bandy ORDER BY w_stadku_od) FROM kocury;
```

### 15.9 RATIO_TO_REPORT

Row's share of the group sum (0–1).

```sql
SELECT pseudo, RATIO_TO_REPORT(przydzial_myszy) OVER (PARTITION BY nr_bandy) FROM kocury;
```

### 15.10 Top-N per group

Window functions aren't allowed in `WHERE`, so filter in an outer query.

```sql
SELECT * FROM (SELECT pseudo, nr_bandy, RANK() OVER (PARTITION BY nr_bandy ORDER BY przydzial_myszy DESC) AS rnk FROM kocury) WHERE rnk = 1;
```

## 16. Pivot

### 16.1 PIVOT

Turns row values into columns; the source should hold only the needed columns.

```sql
SELECT * FROM (SELECT nr_bandy, plec, przydzial_myszy FROM kocury) PIVOT (SUM(przydzial_myszy) FOR plec IN ('M' AS samce, 'D' AS samice));
```

### 16.2 PIVOT with several aggregates

Creates a column per value × aggregate (`SAMCE_SUMA`, `SAMCE_ILE`, …).

```sql
SELECT * FROM (SELECT nr_bandy, plec, przydzial_myszy FROM kocury) PIVOT (SUM(przydzial_myszy) AS suma, COUNT(*) AS ile FOR plec IN ('M' AS samce, 'D' AS samice));
```

### 16.3 UNPIVOT

Turns columns into rows; skips `NULL`s unless `INCLUDE NULLS`.

```sql
SELECT * FROM kocury UNPIVOT (ile FOR rodzaj IN (przydzial_myszy AS 'PRZYDZIAL', myszy_extra AS 'EXTRA'));
```

### 16.4 Pivot with CASE

Portable pivot: one conditional aggregate per column.

```sql
SELECT nr_bandy, SUM(CASE WHEN plec = 'M' THEN przydzial_myszy ELSE 0 END) AS samce, SUM(CASE WHEN plec = 'D' THEN przydzial_myszy ELSE 0 END) AS samice FROM kocury GROUP BY nr_bandy;
```

## 17. SQL*Plus

### 17.1 SET LINESIZE / PAGESIZE

Wider lines and fewer repeated headers.

```sql
SET LINESIZE 200
SET PAGESIZE 100
```

### 17.2 COLUMN FORMAT

Sets the width of a text column.

```sql
COLUMN imie FORMAT A15
```

### 17.3 @file

Runs a script file.

```sql
@lista3/zad1.sql
```

### 17.4 /

Runs the last statement again.

```sql
/
```

### 17.5 DESC

Shows a table's columns.

```sql
DESC kocury
```
