# Notatki dokumentacja – PostgreSQL (18)

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
  - [1.12 IDENTITY](#112-identity)
- [2. DML](#2-dml)
  - [2.1 INSERT … VALUES](#21-insert--values)
  - [2.2 DATE literal](#22-date-literal)
  - [2.3 UPDATE](#23-update)
  - [2.4 UPDATE … FROM](#24-update--from)
  - [2.5 DELETE](#25-delete)
  - [2.6 RETURNING](#26-returning)
  - [2.7 BEGIN / COMMIT / ROLLBACK](#27-begin--commit--rollback)
- [3. SELECT basics](#3-select-basics)
  - [3.1 SELECT … FROM](#31-select--from)
  - [3.2 Column alias](#32-column-alias)
  - [3.3 Table alias](#33-table-alias)
  - [3.4 DISTINCT](#34-distinct)
  - [3.5 DISTINCT ON](#35-distinct-on)
  - [3.6 WHERE](#36-where)
  - [3.7 BETWEEN](#37-between)
  - [3.8 IN](#38-in)
  - [3.9 LIKE / ILIKE](#39-like--ilike)
  - [3.10 IS NULL](#310-is-null)
  - [3.11 ORDER BY](#311-order-by)
  - [3.12 LIMIT / OFFSET](#312-limit--offset)
  - [3.13 FETCH FIRST](#313-fetch-first)
  - [3.14 SELECT without FROM](#314-select-without-from)
- [4. Strings](#4-strings)
  - [4.1 ||](#41-)
  - [4.2 CONCAT](#42-concat)
  - [4.3 CONCAT_WS](#43-concat_ws)
  - [4.4 LOWER / UPPER / INITCAP](#44-lower--upper--initcap)
  - [4.5 LENGTH](#45-length)
  - [4.6 POSITION / STRPOS](#46-position--strpos)
  - [4.7 SUBSTRING](#47-substring)
  - [4.8 LEFT / RIGHT](#48-left--right)
  - [4.9 LPAD / RPAD](#49-lpad--rpad)
  - [4.10 REPEAT](#410-repeat)
  - [4.11 REPLACE](#411-replace)
  - [4.12 OVERLAY](#412-overlay)
  - [4.13 REGEXP_REPLACE](#413-regexp_replace)
  - [4.14 TRIM](#414-trim)
  - [4.15 Empty string](#415-empty-string)
- [5. NULL handling](#5-null-handling)
  - [5.1 COALESCE](#51-coalesce)
  - [5.2 NULLIF](#52-nullif)
  - [5.3 Comparing with NULL](#53-comparing-with-null)
  - [5.4 IS DISTINCT FROM](#54-is-distinct-from)
- [6. Numbers](#6-numbers)
  - [6.1 ROUND](#61-round)
  - [6.2 TRUNC](#62-trunc)
  - [6.3 MOD / %](#63-mod--)
  - [6.4 CEIL / FLOOR](#64-ceil--floor)
  - [6.5 Integer division](#65-integer-division)
- [7. Dates](#7-dates)
  - [7.1 CURRENT_DATE / NOW()](#71-current_date--now)
  - [7.2 DATE_TRUNC](#72-date_trunc)
  - [7.3 EXTRACT](#73-extract)
  - [7.4 Date arithmetic](#74-date-arithmetic)
  - [7.5 INTERVAL](#75-interval)
  - [7.6 AGE](#76-age)
  - [7.7 Last day of month](#77-last-day-of-month)
  - [7.8 Last Wednesday of month](#78-last-wednesday-of-month)
  - [7.9 MAKE_DATE](#79-make_date)
- [8. Conversions](#8-conversions)
  - [8.1 ::](#81-)
  - [8.2 CAST](#82-cast)
  - [8.3 TO_CHAR(date, format)](#83-to_chardate-format)
  - [8.4 TO_CHAR(number, format)](#84-to_charnumber-format)
  - [8.5 TO_DATE](#85-to_date)
- [9. Conditionals](#9-conditionals)
  - [9.1 CASE WHEN](#91-case-when)
  - [9.2 CASE value](#92-case-value)
  - [9.3 GREATEST / LEAST](#93-greatest--least)
- [10. Grouping](#10-grouping)
  - [10.1 COUNT](#101-count)
  - [10.2 SUM / AVG / MIN / MAX](#102-sum--avg--min--max)
  - [10.3 GROUP BY](#103-group-by)
  - [10.4 HAVING](#104-having)
  - [10.5 Conditional COUNT](#105-conditional-count)
  - [10.6 FILTER](#106-filter)
  - [10.7 STRING_AGG](#107-string_agg)
  - [10.8 GROUP BY alias / position](#108-group-by-alias--position)
  - [10.9 ROLLUP](#109-rollup)
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
  - [11.11 LATERAL](#1111-lateral)
  - [11.12 LEFT JOIN + WHERE trap](#1112-left-join--where-trap)
- [12. Set operators](#12-set-operators)
  - [12.1 UNION / UNION ALL](#121-union--union-all)
  - [12.2 INTERSECT](#122-intersect)
  - [12.3 EXCEPT](#123-except)
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
  - [14.1 WITH RECURSIVE](#141-with-recursive)
  - [14.2 Level](#142-level)
  - [14.3 Upwards](#143-upwards)
  - [14.4 Path and root](#144-path-and-root)
  - [14.5 Leaf check](#145-leaf-check)
  - [14.6 SEARCH DEPTH FIRST](#146-search-depth-first)
  - [14.7 generate_series](#147-generate_series)
- [15. Window functions (OVER)](#15-window-functions-over)
  - [15.1 OVER ()](#151-over-)
  - [15.2 PARTITION BY](#152-partition-by)
  - [15.3 ROW_NUMBER](#153-row_number)
  - [15.4 RANK / DENSE_RANK](#154-rank--dense_rank)
  - [15.5 Running total](#155-running-total)
  - [15.6 ROWS BETWEEN](#156-rows-between)
  - [15.7 LAG / LEAD](#157-lag--lead)
  - [15.8 FIRST_VALUE](#158-first_value)
  - [15.9 WINDOW clause](#159-window-clause)
  - [15.10 Top-N per group](#1510-top-n-per-group)
- [16. Pivot](#16-pivot)
  - [16.1 Pivot with CASE](#161-pivot-with-case)
  - [16.2 Pivot with FILTER](#162-pivot-with-filter)
  - [16.3 crosstab](#163-crosstab)
  - [16.4 Unpivot](#164-unpivot)
- [17. psql](#17-psql)
  - [17.1 \dt](#171-dt)
  - [17.2 \d](#172-d)
  - [17.3 \i](#173-i)
  - [17.4 \x](#174-x)
  - [17.5 \q](#175-q)

## 1. DDL

### 1.1 CREATE TABLE

Creates a table; `IF NOT EXISTS` skips it when it already exists.

```sql
CREATE TABLE IF NOT EXISTS wrogowie (imie_wroga VARCHAR(15) PRIMARY KEY, gatunek VARCHAR(15));
```

### 1.2 Data types

`NUMERIC(p)`, `VARCHAR(n)`, `TEXT`, `INTEGER`, `BOOLEAN`, `DATE` (no time) and `TIMESTAMP`.

```sql
pseudo VARCHAR(15), przydzial_myszy NUMERIC(3), w_stadku_od DATE
```

### 1.3 PRIMARY KEY

Unique, non-null row id; a composite key goes at table level.

```sql
PRIMARY KEY (pseudo, imie_wroga)
```

### 1.4 NOT NULL / UNIQUE

`UNIQUE` allows many `NULL`s (`UNIQUE NULLS NOT DISTINCT` forbids that).

```sql
nazwa VARCHAR(20) NOT NULL, teren VARCHAR(15) UNIQUE
```

### 1.5 CHECK

A column CHECK may use other columns too.

```sql
max_myszy NUMERIC(3) CHECK (max_myszy >= min_myszy) CHECK (max_myszy < 200)
```

### 1.6 REFERENCES

Foreign key, can point to the same table.

```sql
szef VARCHAR(15) REFERENCES kocury(pseudo)
```

### 1.7 DEFAULT

Value used when the column is left out of an INSERT.

```sql
w_stadku_od DATE DEFAULT CURRENT_DATE
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

Adds, changes, renames or removes a column.

```sql
ALTER TABLE kocury ADD COLUMN ulubiona VARCHAR(20);
ALTER TABLE kocury ALTER COLUMN ulubiona TYPE VARCHAR(30);
ALTER TABLE kocury RENAME COLUMN ulubiona TO przysmak;
ALTER TABLE kocury DROP COLUMN przysmak;
```

### 1.11 DROP TABLE

Removes a table; `CASCADE` also drops FKs pointing at it.

```sql
DROP TABLE IF EXISTS kocury CASCADE;
```

### 1.12 IDENTITY

Auto-increment column (older style: `SERIAL`).

```sql
CREATE TABLE incydenty (id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY, opis VARCHAR(50));
```

## 2. DML

### 2.1 INSERT … VALUES

Inserts one or more rows.

```sql
INSERT INTO funkcje (funkcja, min_myszy, max_myszy) VALUES ('SZEFUNIO', 90, 110), ('BANDZIOR', 70, 90);
```

### 2.2 DATE literal

ISO date constant; a plain `'2008-12-01'` string is also cast automatically.

```sql
INSERT INTO kocury (imie, pseudo, w_stadku_od) VALUES ('JACEK', 'PLACEK', DATE '2008-12-01');
```

### 2.3 UPDATE

Changes values in matching rows.

```sql
UPDATE bandy SET szef_bandy = 'TYGRYS' WHERE nr_bandy = 1;
```

### 2.4 UPDATE … FROM

Update using values from another table.

```sql
UPDATE kocury K SET nr_bandy = B.nr_bandy FROM bandy B WHERE B.szef_bandy = K.szef;
```

### 2.5 DELETE

Removes matching rows.

```sql
DELETE FROM wrogowie_kocurow WHERE imie_wroga = 'KAZIO';
```

### 2.6 RETURNING

Returns the rows changed by INSERT / UPDATE / DELETE.

```sql
UPDATE kocury SET przydzial_myszy = przydzial_myszy + 1 WHERE pseudo = 'ZERO' RETURNING pseudo, przydzial_myszy;
```

### 2.7 BEGIN / COMMIT / ROLLBACK

psql auto-commits each statement; `BEGIN` starts a transaction you can undo.

```sql
BEGIN; DELETE FROM wrogowie_kocurow; ROLLBACK;
```

## 3. SELECT basics

### 3.1 SELECT … FROM

Picks columns from a table.

```sql
SELECT imie, funkcja FROM kocury;
```

### 3.2 Column alias

Unquoted names turn lowercase; double quotes keep spaces and letter case.

```sql
SELECT przydzial_myszy AS "Zjada" FROM kocury;
```

### 3.3 Table alias

`AS` is optional.

```sql
SELECT K.imie FROM kocury AS K;
```

### 3.4 DISTINCT

Removes duplicate rows.

```sql
SELECT DISTINCT funkcja FROM kocury;
```

### 3.5 DISTINCT ON

Keeps the first row of each group, by `ORDER BY` (Postgres only).

```sql
SELECT DISTINCT ON (nr_bandy) nr_bandy, pseudo FROM kocury ORDER BY nr_bandy, przydzial_myszy DESC;
```

### 3.6 WHERE

Filters rows.

```sql
SELECT imie FROM kocury WHERE plec = 'D' AND przydzial_myszy >= 55;
```

### 3.7 BETWEEN

Range check, both ends inclusive.

```sql
SELECT imie FROM kocury WHERE w_stadku_od BETWEEN '2005-09-01' AND '2007-07-31';
```

### 3.8 IN

Matches any value from a list.

```sql
SELECT imie FROM kocury WHERE funkcja IN ('MILUSIA', 'KOT');
```

### 3.9 LIKE / ILIKE

Pattern match (`%` any text, `_` one char); `ILIKE` ignores letter case.

```sql
SELECT pseudo FROM kocury WHERE pseudo ILIKE '%a%' AND pseudo ILIKE '%l%';
```

### 3.10 IS NULL

The only correct way to test for `NULL`.

```sql
SELECT imie_wroga FROM wrogowie WHERE lapowka IS NULL;
```

### 3.11 ORDER BY

Sorts the result; `NULL`s go last in `ASC` unless `NULLS FIRST`.

```sql
SELECT pseudo, myszy_extra FROM kocury ORDER BY myszy_extra DESC NULLS LAST, pseudo;
```

### 3.12 LIMIT / OFFSET

Top-N rows after sorting, optionally skipping some.

```sql
SELECT pseudo FROM kocury ORDER BY przydzial_myszy DESC LIMIT 3 OFFSET 1;
```

### 3.13 FETCH FIRST

Standard-SQL version of `LIMIT`.

```sql
SELECT pseudo FROM kocury ORDER BY przydzial_myszy DESC FETCH FIRST 3 ROWS ONLY;
```

### 3.14 SELECT without FROM

No dummy table needed.

```sql
SELECT CURRENT_DATE;
```

## 4. Strings

### 4.1 ||

Concatenation; any `NULL` makes the whole result `NULL`.

```sql
SELECT imie || ' zwany ' || pseudo FROM kocury;
```

### 4.2 CONCAT

Concatenates any number of arguments and skips `NULL`s.

```sql
SELECT CONCAT(imie, ' zwany ', pseudo, ' od ', w_stadku_od) FROM kocury;
```

### 4.3 CONCAT_WS

Concatenates with a separator between values.

```sql
SELECT CONCAT_WS(', ', imie, pseudo, funkcja) FROM kocury;
```

### 4.4 LOWER / UPPER / INITCAP

Changes letter case.

```sql
SELECT LOWER(pseudo), INITCAP(imie) FROM kocury;
```

### 4.5 LENGTH

Number of characters.

```sql
SELECT pseudo FROM kocury WHERE LENGTH(pseudo) > 4;
```

### 4.6 POSITION / STRPOS

Position of a substring (1-based), 0 when not found.

```sql
SELECT pseudo, POSITION('a' IN LOWER(pseudo)), STRPOS(pseudo, 'L') FROM kocury;
```

### 4.7 SUBSTRING

Substring from a position, with optional length (`SUBSTR` works too).

```sql
SELECT SUBSTRING(pseudo FROM 2 FOR 3), SUBSTR(pseudo, 2, 3) FROM kocury;
```

### 4.8 LEFT / RIGHT

First / last n characters.

```sql
SELECT LEFT(pseudo, 2), RIGHT(pseudo, 2) FROM kocury;
```

### 4.9 LPAD / RPAD

Pads text to a length; handy for tree indentation.

```sql
SELECT LPAD(pseudo, 10, '*') FROM kocury;
```

### 4.10 REPEAT

Repeats a string n times.

```sql
SELECT REPEAT(' ', 4) || pseudo FROM kocury;
```

### 4.11 REPLACE

Replaces all occurrences.

```sql
SELECT REPLACE(pseudo, 'A', '#') FROM kocury;
```

### 4.12 OVERLAY

Replaces characters at a given position.

```sql
SELECT OVERLAY(pseudo PLACING '#' FROM POSITION('A' IN pseudo) FOR 1) FROM kocury WHERE pseudo LIKE '%A%';
```

### 4.13 REGEXP_REPLACE

Regex replace; without the `g` flag only the 1st match, `i` ignores case.

```sql
SELECT REGEXP_REPLACE(pseudo, 'a', '#', 'i') FROM kocury;
```

### 4.14 TRIM

Removes surrounding spaces.

```sql
SELECT TRIM('  TYGRYS  ');
```

### 4.15 Empty string

`''` is a normal value, not `NULL`.

```sql
SELECT '' IS NULL;   -- false
```

## 5. NULL handling

### 5.1 COALESCE

First non-`NULL` argument.

```sql
SELECT przydzial_myszy + COALESCE(myszy_extra, 0) FROM kocury;
```

### 5.2 NULLIF

Returns `NULL` when both arguments are equal.

```sql
SELECT NULLIF(przydzial_myszy, 0) FROM kocury;
```

### 5.3 Comparing with NULL

`= NULL` is never true; aggregates skip `NULL`s.

```sql
SELECT imie FROM kocury WHERE myszy_extra = NULL;   -- always 0 rows
```

### 5.4 IS DISTINCT FROM

`NULL`-safe "not equal" (`NULL` vs value counts as different).

```sql
SELECT imie FROM kocury WHERE myszy_extra IS DISTINCT FROM 0;
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

### 6.3 MOD / %

Remainder of division.

```sql
SELECT pseudo FROM kocury WHERE przydzial_myszy % 2 = 0;
```

### 6.4 CEIL / FLOOR

Rounds up / down to an integer.

```sql
SELECT CEIL(przydzial_myszy / 7), FLOOR(przydzial_myszy / 7) FROM kocury;
```

### 6.5 Integer division

Integer / integer drops the decimals: `5 / 2 = 2` (`NUMERIC` columns are fine).

```sql
SELECT 5 / 2, 5.0 / 2, 5::numeric / 2;
```

## 7. Dates

### 7.1 CURRENT_DATE / NOW()

Today's date, or the current timestamp.

```sql
SELECT CURRENT_DATE, NOW(), CURRENT_TIMESTAMP;
```

### 7.2 DATE_TRUNC

Start of the month/year/…; returns a timestamp.

```sql
SELECT DATE_TRUNC('month', CURRENT_DATE)::date;
```

### 7.3 EXTRACT

Gets a date part as a number; `DOW` is 0 = Sunday … 6 = Saturday.

```sql
SELECT imie_wroga FROM wrogowie_kocurow WHERE EXTRACT(YEAR FROM data_incydentu) = 2009;
```

### 7.4 Date arithmetic

`date + n` adds days; date minus date gives an integer of days.

```sql
SELECT pseudo, CURRENT_DATE - w_stadku_od, w_stadku_od + 7 FROM kocury;
```

### 7.5 INTERVAL

Adds months/years; the result is a timestamp, so cast back with `::date`.

```sql
SELECT (w_stadku_od + INTERVAL '6 months')::date FROM kocury;
```

### 7.6 AGE

Interval between two dates in years/months/days.

```sql
SELECT pseudo FROM kocury WHERE AGE(CURRENT_DATE, w_stadku_od) > INTERVAL '15 years';
```

### 7.7 Last day of month

Start of next month minus one day.

```sql
SELECT (DATE_TRUNC('month', CURRENT_DATE) + INTERVAL '1 month - 1 day')::date;
```

### 7.8 Last Wednesday of month

Last day minus `(DOW + 4) % 7` days.

```sql
SELECT ostatni - (EXTRACT(DOW FROM ostatni)::int + 4) % 7 FROM (SELECT (DATE_TRUNC('month', CURRENT_DATE) + INTERVAL '1 month - 1 day')::date AS ostatni) AS dni;
```

### 7.9 MAKE_DATE

Builds a date from numbers.

```sql
SELECT MAKE_DATE(2009, 1, 7);
```

## 8. Conversions

### 8.1 ::

Postgres cast shorthand.

```sql
SELECT przydzial_myszy::text, '42'::int, '2009-01-07'::date FROM kocury;
```

### 8.2 CAST

Standard type conversion.

```sql
SELECT CAST(przydzial_myszy AS VARCHAR(10)) FROM kocury;
```

### 8.3 TO_CHAR(date, format)

Formats a date; `Month` is space-padded, `FM` removes the padding.

```sql
SELECT TO_CHAR(w_stadku_od, 'YYYY-MM-DD'), TO_CHAR(w_stadku_od, 'FMMonth') FROM kocury;
```

### 8.4 TO_CHAR(number, format)

Number to text needs a format (`::text` is simpler).

```sql
SELECT TO_CHAR(przydzial_myszy, 'FM999') FROM kocury;
```

### 8.5 TO_DATE

Text to date using a format.

```sql
SELECT TO_DATE('07-01-2009', 'DD-MM-YYYY');
```

## 9. Conditionals

### 9.1 CASE WHEN

Conditions checked in order; all branches must return the same type.

```sql
SELECT CASE WHEN 12 * przydzial_myszy > 660 THEN (12 * przydzial_myszy)::text ELSE 'Ponizej 660' END FROM kocury;
```

### 9.2 CASE value

Compares one expression against values.

```sql
SELECT CASE plec WHEN 'M' THEN 'Kocur' ELSE 'Kotka' END FROM kocury;
```

### 9.3 GREATEST / LEAST

Largest / smallest of the arguments.

```sql
SELECT pseudo, GREATEST(przydzial_myszy, COALESCE(myszy_extra, 0)) FROM kocury;
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

One row per group; grouping by a primary key lets you select that table's other columns.

```sql
SELECT B.nazwa, COUNT(*) FROM bandy B JOIN kocury K ON K.nr_bandy = B.nr_bandy GROUP BY B.nr_bandy;
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

### 10.6 FILTER

Shorter conditional aggregate.

```sql
SELECT nr_bandy, COUNT(*) FILTER (WHERE plec = 'D') AS kotki FROM kocury GROUP BY nr_bandy;
```

### 10.7 STRING_AGG

Joins a group's values into one string.

```sql
SELECT nr_bandy, STRING_AGG(pseudo, ', ' ORDER BY pseudo) FROM kocury GROUP BY nr_bandy;
```

### 10.8 GROUP BY alias / position

Postgres lets you group by an output alias or column number.

```sql
SELECT EXTRACT(MONTH FROM w_stadku_od) AS miesiac, COUNT(*) FROM kocury GROUP BY miesiac ORDER BY 1;
```

### 10.9 ROLLUP

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

Joins on same-named columns.

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

### 11.11 LATERAL

Subquery that can use columns of the tables before it.

```sql
SELECT K.pseudo, O.imie_wroga FROM kocury K LEFT JOIN LATERAL (SELECT imie_wroga FROM wrogowie_kocurow WK WHERE WK.pseudo = K.pseudo ORDER BY data_incydentu DESC LIMIT 1) O ON TRUE;
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

### 12.3 EXCEPT

Rows from the first result but not the second (`MINUS` in Oracle).

```sql
SELECT nr_bandy FROM bandy EXCEPT SELECT nr_bandy FROM kocury;
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

Uses a query result as a table (alias optional since v16).

```sql
SELECT * FROM (SELECT nr_bandy, SUM(przydzial_myszy) AS suma FROM kocury GROUP BY nr_bandy) AS sumy WHERE suma > 200;
```

### 13.9 WITH (CTE)

Names a subquery so it can be reused.

```sql
WITH sumy AS (SELECT nr_bandy, SUM(przydzial_myszy) AS suma FROM kocury GROUP BY nr_bandy) SELECT * FROM sumy WHERE suma > 200;
```

## 14. Hierarchical queries

### 14.1 WITH RECURSIVE

Tree query: anchor rows `UNION ALL` a step that joins back to the CTE (no `CONNECT BY`).

```sql
WITH RECURSIVE drzewo AS (SELECT pseudo FROM kocury WHERE szef IS NULL UNION ALL SELECT K.pseudo FROM kocury K JOIN drzewo D ON K.szef = D.pseudo) SELECT * FROM drzewo;
```

### 14.2 Level

Carry a counter column, increased in each step.

```sql
WITH RECURSIVE drzewo AS (SELECT pseudo, 1 AS poziom FROM kocury WHERE funkcja = 'BANDZIOR' UNION ALL SELECT K.pseudo, D.poziom + 1 FROM kocury K JOIN drzewo D ON K.szef = D.pseudo) SELECT REPEAT(' ', 4 * (poziom - 1)) || pseudo FROM drzewo;
```

### 14.3 Upwards

Swap the join direction to walk from a cat to its bosses.

```sql
WITH RECURSIVE szefowie AS (SELECT pseudo, szef FROM kocury WHERE pseudo = 'ZERO' UNION ALL SELECT K.pseudo, K.szef FROM kocury K JOIN szefowie S ON K.pseudo = S.szef) SELECT pseudo FROM szefowie;
```

### 14.4 Path and root

Carry the root value and a text path (cast to `text` so types match).

```sql
WITH RECURSIVE sciezki AS (SELECT imie AS korzen, szef, imie::text AS sciezka FROM kocury WHERE funkcja = 'KOT' UNION ALL SELECT S.korzen, K.szef, S.sciezka || ' | ' || K.imie FROM sciezki S JOIN kocury K ON K.pseudo = S.szef) SELECT korzen, sciezka FROM sciezki WHERE szef IS NULL;
```

### 14.5 Leaf check

A row is a leaf when nobody points to it.

```sql
SELECT K.pseudo FROM kocury K WHERE NOT EXISTS (SELECT 1 FROM kocury P WHERE P.szef = K.pseudo);
```

### 14.6 SEARCH DEPTH FIRST

Orders the result like a tree (Oracle's `ORDER SIBLINGS BY`).

```sql
WITH RECURSIVE drzewo AS (SELECT pseudo FROM kocury WHERE szef IS NULL UNION ALL SELECT K.pseudo FROM kocury K JOIN drzewo D ON K.szef = D.pseudo) SEARCH DEPTH FIRST BY pseudo SET kolejnosc SELECT pseudo FROM drzewo ORDER BY kolejnosc;
```

### 14.7 generate_series

Generates numbers (or dates) 1..n.

```sql
SELECT generate_series(1, 12);
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
SELECT pseudo, ROUND(100.0 * przydzial_myszy / SUM(przydzial_myszy) OVER (PARTITION BY nr_bandy)) AS proc FROM kocury;
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

### 15.9 WINDOW clause

Names a window once and reuses it.

```sql
SELECT pseudo, RANK() OVER w, SUM(przydzial_myszy) OVER w FROM kocury WINDOW w AS (PARTITION BY nr_bandy ORDER BY przydzial_myszy DESC);
```

### 15.10 Top-N per group

Window functions aren't allowed in `WHERE`, so filter in an outer query.

```sql
SELECT * FROM (SELECT pseudo, nr_bandy, RANK() OVER (PARTITION BY nr_bandy ORDER BY przydzial_myszy DESC) AS rnk FROM kocury) AS ranking WHERE rnk = 1;
```

## 16. Pivot

### 16.1 Pivot with CASE

No `PIVOT` keyword; one conditional aggregate per column.

```sql
SELECT nr_bandy, SUM(CASE WHEN plec = 'M' THEN przydzial_myszy ELSE 0 END) AS samce, SUM(CASE WHEN plec = 'D' THEN przydzial_myszy ELSE 0 END) AS samice FROM kocury GROUP BY nr_bandy;
```

### 16.2 Pivot with FILTER

Same pivot, shorter.

```sql
SELECT nr_bandy, SUM(przydzial_myszy) FILTER (WHERE plec = 'M') AS samce, SUM(przydzial_myszy) FILTER (WHERE plec = 'D') AS samice FROM kocury GROUP BY nr_bandy;
```

### 16.3 crosstab

Real pivot from the `tablefunc` extension; output columns must be declared.

```sql
CREATE EXTENSION IF NOT EXISTS tablefunc;
SELECT * FROM crosstab('SELECT nr_bandy, plec, SUM(przydzial_myszy) FROM kocury GROUP BY 1, 2 ORDER BY 1, 2', 'VALUES (''D''), (''M'')') AS wynik(nr_bandy NUMERIC, samice NUMERIC, samce NUMERIC);
```

### 16.4 Unpivot

Columns into rows with `LATERAL (VALUES …)`.

```sql
SELECT K.pseudo, U.rodzaj, U.ile FROM kocury K CROSS JOIN LATERAL (VALUES ('PRZYDZIAL', K.przydzial_myszy), ('EXTRA', K.myszy_extra)) AS U(rodzaj, ile);
```

## 17. psql

### 17.1 \dt

Lists tables.

```sql
\dt
```

### 17.2 \d

Shows a table's columns and constraints.

```sql
\d kocury
```

### 17.3 \i

Runs a script file.

```sql
\i lista3/zad1.sql
```

### 17.4 \x

Toggles one-column-per-line output for wide rows.

```sql
\x
```

### 17.5 \q

Quits psql.

```sql
\q
```
