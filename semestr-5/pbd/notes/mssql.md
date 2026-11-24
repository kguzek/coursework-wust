# Notatki dokumentacja – SQL Server (2022, T-SQL)

## Spis treści

- [1. DDL](#1-ddl)
  - [1.1 CREATE TABLE](#11-create-table)
  - [1.2 Data types](#12-data-types)
  - [1.3 PRIMARY KEY](#13-primary-key)
  - [1.4 NOT NULL / UNIQUE](#14-not-null--unique)
  - [1.5 Filtered unique index](#15-filtered-unique-index)
  - [1.6 CHECK](#16-check)
  - [1.7 REFERENCES](#17-references)
  - [1.8 DEFAULT](#18-default)
  - [1.9 ALTER TABLE ADD CONSTRAINT](#19-alter-table-add-constraint)
  - [1.10 NOCHECK CONSTRAINT](#110-nocheck-constraint)
  - [1.11 ALTER TABLE columns](#111-alter-table-columns)
  - [1.12 DROP TABLE](#112-drop-table)
  - [1.13 IDENTITY](#113-identity)
- [2. DML](#2-dml)
  - [2.1 INSERT … VALUES](#21-insert--values)
  - [2.2 Date literal](#22-date-literal)
  - [2.3 UPDATE](#23-update)
  - [2.4 UPDATE … FROM JOIN](#24-update--from-join)
  - [2.5 DELETE](#25-delete)
  - [2.6 OUTPUT](#26-output)
  - [2.7 BEGIN TRAN / COMMIT / ROLLBACK](#27-begin-tran--commit--rollback)
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
  - [3.11 TOP](#311-top)
  - [3.12 OFFSET … FETCH](#312-offset--fetch)
  - [3.13 SELECT without FROM](#313-select-without-from)
- [4. Strings](#4-strings)
  - [4.1 +](#41-)
  - [4.2 CONCAT](#42-concat)
  - [4.3 CONCAT_WS](#43-concat_ws)
  - [4.4 LOWER / UPPER](#44-lower--upper)
  - [4.5 LEN](#45-len)
  - [4.6 CHARINDEX](#46-charindex)
  - [4.7 SUBSTRING](#47-substring)
  - [4.8 LEFT / RIGHT](#48-left--right)
  - [4.9 REPLICATE](#49-replicate)
  - [4.10 REPLACE](#410-replace)
  - [4.11 STUFF](#411-stuff)
  - [4.12 TRIM / LTRIM / RTRIM](#412-trim--ltrim--rtrim)
  - [4.13 Empty string](#413-empty-string)
- [5. NULL handling](#5-null-handling)
  - [5.1 ISNULL](#51-isnull)
  - [5.2 COALESCE](#52-coalesce)
  - [5.3 NULLIF](#53-nullif)
  - [5.4 Comparing with NULL](#54-comparing-with-null)
  - [5.5 IS DISTINCT FROM](#55-is-distinct-from)
- [6. Numbers](#6-numbers)
  - [6.1 ROUND](#61-round)
  - [6.2 Truncating](#62-truncating)
  - [6.3 %](#63-)
  - [6.4 CEILING / FLOOR](#64-ceiling--floor)
  - [6.5 Integer division](#65-integer-division)
- [7. Dates](#7-dates)
  - [7.1 GETDATE / SYSDATETIME](#71-getdate--sysdatetime)
  - [7.2 YEAR / MONTH / DAY](#72-year--month--day)
  - [7.3 DATEPART](#73-datepart)
  - [7.4 DATEADD](#74-dateadd)
  - [7.5 DATEDIFF](#75-datediff)
  - [7.6 EOMONTH](#76-eomonth)
  - [7.7 DATETRUNC](#77-datetrunc)
  - [7.8 DATEFROMPARTS](#78-datefromparts)
  - [7.9 DATENAME](#79-datename)
  - [7.10 Last Wednesday of month](#710-last-wednesday-of-month)
- [8. Conversions](#8-conversions)
  - [8.1 CAST](#81-cast)
  - [8.2 CONVERT](#82-convert)
  - [8.3 FORMAT](#83-format)
  - [8.4 TRY_CAST](#84-try_cast)
- [9. Conditionals](#9-conditionals)
  - [9.1 CASE WHEN](#91-case-when)
  - [9.2 CASE value](#92-case-value)
  - [9.3 IIF](#93-iif)
  - [9.4 GREATEST / LEAST](#94-greatest--least)
- [10. Grouping](#10-grouping)
  - [10.1 COUNT](#101-count)
  - [10.2 SUM / AVG / MIN / MAX](#102-sum--avg--min--max)
  - [10.3 GROUP BY](#103-group-by)
  - [10.4 HAVING](#104-having)
  - [10.5 Conditional COUNT](#105-conditional-count)
  - [10.6 STRING_AGG](#106-string_agg)
  - [10.7 Group by expression](#107-group-by-expression)
  - [10.8 ROLLUP](#108-rollup)
- [11. Joins](#11-joins)
  - [11.1 JOIN](#111-join)
  - [11.2 LEFT JOIN](#112-left-join)
  - [11.3 RIGHT JOIN](#113-right-join)
  - [11.4 FULL JOIN](#114-full-join)
  - [11.5 CROSS JOIN](#115-cross-join)
  - [11.6 No USING / NATURAL](#116-no-using--natural)
  - [11.7 Self join](#117-self-join)
  - [11.8 Join chain](#118-join-chain)
  - [11.9 Join to a fixed row](#119-join-to-a-fixed-row)
  - [11.10 Anti-join](#1110-anti-join)
  - [11.11 CROSS / OUTER APPLY](#1111-cross--outer-apply)
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
  - [14.1 Recursive CTE](#141-recursive-cte)
  - [14.2 Level](#142-level)
  - [14.3 Upwards](#143-upwards)
  - [14.4 Path and root](#144-path-and-root)
  - [14.5 Leaf check](#145-leaf-check)
  - [14.6 Tree order](#146-tree-order)
  - [14.7 MAXRECURSION](#147-maxrecursion)
  - [14.8 GENERATE_SERIES](#148-generate_series)
- [15. Window functions (OVER)](#15-window-functions-over)
  - [15.1 OVER ()](#151-over-)
  - [15.2 PARTITION BY](#152-partition-by)
  - [15.3 ROW_NUMBER](#153-row_number)
  - [15.4 RANK / DENSE_RANK](#154-rank--dense_rank)
  - [15.5 Running total](#155-running-total)
  - [15.6 ROWS BETWEEN](#156-rows-between)
  - [15.7 LAG / LEAD](#157-lag--lead)
  - [15.8 FIRST_VALUE](#158-first_value)
  - [15.9 Top-N per group](#159-top-n-per-group)
- [16. Pivot](#16-pivot)
  - [16.1 PIVOT](#161-pivot)
  - [16.2 UNPIVOT](#162-unpivot)
  - [16.3 Unpivot with APPLY](#163-unpivot-with-apply)
  - [16.4 Pivot with CASE](#164-pivot-with-case)
- [17. sqlcmd](#17-sqlcmd)
  - [17.1 GO](#171-go)
  - [17.2 :r](#172-r)
  - [17.3 -I flag](#173--i-flag)
  - [17.4 sp_help](#174-sp_help)
  - [17.5 sys.tables](#175-systables)
  - [17.6 EXIT](#176-exit)

## 1. DDL

### 1.1 CREATE TABLE

Creates a table; there is no `CREATE TABLE IF NOT EXISTS`.

```sql
CREATE TABLE wrogowie (imie_wroga VARCHAR(15) PRIMARY KEY, gatunek VARCHAR(15));
```

### 1.2 Data types

`NUMERIC(p)`, `VARCHAR(n)`, `NVARCHAR(n)` (Unicode), `INT`, `BIT`, `DATE` and `DATETIME2`.

```sql
pseudo VARCHAR(15), przydzial_myszy NUMERIC(3), w_stadku_od DATE
```

### 1.3 PRIMARY KEY

Unique, non-null row id; a composite key goes at table level.

```sql
PRIMARY KEY (pseudo, imie_wroga)
```

### 1.4 NOT NULL / UNIQUE

`UNIQUE` allows only one `NULL` in the column.

```sql
nazwa VARCHAR(20) NOT NULL, teren VARCHAR(15) UNIQUE
```

### 1.5 Filtered unique index

Unique values but many `NULL`s allowed (needed for `szef_bandy`).

```sql
CREATE UNIQUE INDEX bandy_szef_uq ON bandy (szef_bandy) WHERE szef_bandy IS NOT NULL;
```

### 1.6 CHECK

A column CHECK sees only its own column; multi-column checks go at table level.

```sql
plec VARCHAR(1) CHECK (plec IN ('M', 'D')),
CONSTRAINT fu_max_ch CHECK (max_myszy >= min_myszy)
```

### 1.7 REFERENCES

Foreign key, can point to the same table.

```sql
szef VARCHAR(15) REFERENCES kocury(pseudo)
```

### 1.8 DEFAULT

Value used when the column is left out of an INSERT.

```sql
w_stadku_od DATE DEFAULT GETDATE()
```

### 1.9 ALTER TABLE ADD CONSTRAINT

Adds a constraint later, e.g. to break the `bandy` ↔ `kocury` cycle.

```sql
ALTER TABLE bandy ADD CONSTRAINT bandy_szef_fk FOREIGN KEY (szef_bandy) REFERENCES kocury(pseudo);
```

### 1.10 NOCHECK CONSTRAINT

No `DEFERRABLE`; a constraint can be switched off and back on instead.

```sql
ALTER TABLE bandy NOCHECK CONSTRAINT bandy_szef_fk;
ALTER TABLE bandy WITH CHECK CHECK CONSTRAINT bandy_szef_fk;
```

### 1.11 ALTER TABLE columns

Adds, changes or removes a column (no `COLUMN` keyword in `ADD`).

```sql
ALTER TABLE kocury ADD ulubiona VARCHAR(20);
ALTER TABLE kocury ALTER COLUMN ulubiona VARCHAR(30);
ALTER TABLE kocury DROP COLUMN ulubiona;
```

### 1.12 DROP TABLE

Removes a table; no `CASCADE`, so drop FKs pointing at it first.

```sql
DROP TABLE IF EXISTS wrogowie_kocurow;
```

### 1.13 IDENTITY

Auto-increment column.

```sql
CREATE TABLE incydenty (id INT IDENTITY(1, 1) PRIMARY KEY, opis VARCHAR(50));
```

## 2. DML

### 2.1 INSERT … VALUES

Inserts one or more rows (up to 1000 per `VALUES`).

```sql
INSERT INTO funkcje (funkcja, min_myszy, max_myszy) VALUES ('SZEFUNIO', 90, 110), ('BANDZIOR', 70, 90);
```

### 2.2 Date literal

A plain string; `DATE '…'` is not supported, `'YYYYMMDD'` is safe under any settings.

```sql
INSERT INTO kocury (imie, pseudo, w_stadku_od) VALUES ('JACEK', 'PLACEK', '2008-12-01');
```

### 2.3 UPDATE

Changes values in matching rows.

```sql
UPDATE bandy SET szef_bandy = 'TYGRYS' WHERE nr_bandy = 1;
```

### 2.4 UPDATE … FROM JOIN

Update using values from a joined table.

```sql
UPDATE K SET nr_bandy = B.nr_bandy FROM kocury K JOIN bandy B ON B.szef_bandy = K.szef;
```

### 2.5 DELETE

Removes matching rows.

```sql
DELETE FROM wrogowie_kocurow WHERE imie_wroga = 'KAZIO';
```

### 2.6 OUTPUT

Returns the changed rows (`inserted` = new values, `deleted` = old).

```sql
UPDATE kocury SET przydzial_myszy += 1 OUTPUT deleted.przydzial_myszy, inserted.przydzial_myszy WHERE pseudo = 'ZERO';
```

### 2.7 BEGIN TRAN / COMMIT / ROLLBACK

Statements auto-commit; `BEGIN TRAN` starts a transaction you can undo.

```sql
BEGIN TRAN; DELETE FROM wrogowie_kocurow; ROLLBACK;
```

## 3. SELECT basics

### 3.1 SELECT … FROM

Picks columns from a table.

```sql
SELECT imie, funkcja FROM kocury;
```

### 3.2 Column alias

Double quotes or square brackets keep spaces.

```sql
SELECT przydzial_myszy AS "Zjada", myszy_extra AS [Myszy extra] FROM kocury;
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

### 3.5 WHERE

Filters rows.

```sql
SELECT imie FROM kocury WHERE plec = 'D' AND przydzial_myszy >= 55;
```

### 3.6 BETWEEN

Range check, both ends inclusive.

```sql
SELECT imie FROM kocury WHERE w_stadku_od BETWEEN '2005-09-01' AND '2007-07-31';
```

### 3.7 IN

Matches any value from a list.

```sql
SELECT imie FROM kocury WHERE funkcja IN ('MILUSIA', 'KOT');
```

### 3.8 LIKE

Pattern match; case-insensitive with the default collation, `[ ]` matches a set of chars.

```sql
SELECT pseudo FROM kocury WHERE pseudo LIKE '%a%' AND pseudo LIKE '[L-T]%';
```

### 3.9 IS NULL

The only correct way to test for `NULL`.

```sql
SELECT imie_wroga FROM wrogowie WHERE lapowka IS NULL;
```

### 3.10 ORDER BY

Sorts the result; `NULL`s come first in `ASC`.

```sql
SELECT pseudo, w_stadku_od FROM kocury ORDER BY w_stadku_od DESC, pseudo;
```

### 3.11 TOP

First n rows; `WITH TIES` also keeps rows equal to the last one.

```sql
SELECT TOP 3 WITH TIES pseudo FROM kocury ORDER BY przydzial_myszy DESC;
```

### 3.12 OFFSET … FETCH

Skips and takes rows; requires `ORDER BY`.

```sql
SELECT pseudo FROM kocury ORDER BY przydzial_myszy DESC OFFSET 1 ROWS FETCH NEXT 3 ROWS ONLY;
```

### 3.13 SELECT without FROM

No dummy table needed.

```sql
SELECT GETDATE();
```

## 4. Strings

### 4.1 +

Concatenation; numbers and dates must be cast, and `NULL` makes the result `NULL`.

```sql
SELECT imie + ' zwany ' + pseudo + ' z bandy ' + CAST(nr_bandy AS VARCHAR) FROM kocury;
```

### 4.2 CONCAT

Concatenates any number of arguments, converts types and skips `NULL`s.

```sql
SELECT CONCAT(imie, ' zwany ', pseudo, ' od ', w_stadku_od) FROM kocury;
```

### 4.3 CONCAT_WS

Concatenates with a separator between values.

```sql
SELECT CONCAT_WS(', ', imie, pseudo, funkcja) FROM kocury;
```

### 4.4 LOWER / UPPER

Changes letter case (no `INITCAP`).

```sql
SELECT LOWER(pseudo), UPPER(imie) FROM kocury;
```

### 4.5 LEN

Number of characters, ignoring trailing spaces.

```sql
SELECT pseudo FROM kocury WHERE LEN(pseudo) > 4;
```

### 4.6 CHARINDEX

Position of a substring (1-based), 0 when not found; the searched text goes first.

```sql
SELECT pseudo, CHARINDEX('A', pseudo) FROM kocury;
```

### 4.7 SUBSTRING

Substring from a position; the length is required.

```sql
SELECT SUBSTRING(pseudo, 2, 3) FROM kocury;
```

### 4.8 LEFT / RIGHT

First / last n characters.

```sql
SELECT LEFT(pseudo, 2), RIGHT(pseudo, 2) FROM kocury;
```

### 4.9 REPLICATE

Repeats a string; used for padding since there is no `LPAD`.

```sql
SELECT RIGHT(REPLICATE('*', 10) + pseudo, 10) FROM kocury;
```

### 4.10 REPLACE

Replaces all occurrences.

```sql
SELECT REPLACE(pseudo, 'A', '#') FROM kocury;
```

### 4.11 STUFF

Replaces characters at a given position (like Postgres `OVERLAY`).

```sql
SELECT STUFF(pseudo, CHARINDEX('A', pseudo), 1, '#') FROM kocury WHERE pseudo LIKE '%A%';
```

### 4.12 TRIM / LTRIM / RTRIM

Removes surrounding spaces.

```sql
SELECT TRIM('  TYGRYS  ');
```

### 4.13 Empty string

`''` is a normal value, not `NULL`.

```sql
SELECT CASE WHEN '' IS NULL THEN 'NULL' ELSE 'nie NULL' END;
```

## 5. NULL handling

### 5.1 ISNULL

Replaces `NULL` with a value (2 arguments).

```sql
SELECT przydzial_myszy + ISNULL(myszy_extra, 0) FROM kocury;
```

### 5.2 COALESCE

First non-`NULL` argument.

```sql
SELECT COALESCE(myszy_extra, przydzial_myszy, 0) FROM kocury;
```

### 5.3 NULLIF

Returns `NULL` when both arguments are equal.

```sql
SELECT NULLIF(przydzial_myszy, 0) FROM kocury;
```

### 5.4 Comparing with NULL

`= NULL` is never true; aggregates skip `NULL`s.

```sql
SELECT imie FROM kocury WHERE myszy_extra = NULL;   -- always 0 rows
```

### 5.5 IS DISTINCT FROM

`NULL`-safe "not equal" (since 2022).

```sql
SELECT imie FROM kocury WHERE myszy_extra IS DISTINCT FROM 0;
```

## 6. Numbers

### 6.1 ROUND

Rounds to n decimal places; the 2nd argument is required.

```sql
SELECT ROUND(przydzial_myszy / 1.1, 0), ROUND(przydzial_myszy / 1.1, 1) FROM kocury;
```

### 6.2 Truncating

`ROUND(x, n, 1)` cuts off instead of rounding.

```sql
SELECT ROUND(przydzial_myszy / 7.0, 0, 1) FROM kocury;
```

### 6.3 %

Remainder of division.

```sql
SELECT pseudo FROM kocury WHERE przydzial_myszy % 2 = 0;
```

### 6.4 CEILING / FLOOR

Rounds up / down to an integer.

```sql
SELECT CEILING(przydzial_myszy / 7.0), FLOOR(przydzial_myszy / 7.0) FROM kocury;
```

### 6.5 Integer division

Integer / integer drops the decimals: `5 / 2 = 2`.

```sql
SELECT 5 / 2, 5.0 / 2, CAST(5 AS NUMERIC(5, 2)) / 2;
```

## 7. Dates

### 7.1 GETDATE / SYSDATETIME

Current date and time; cast to `DATE` for just the day.

```sql
SELECT GETDATE(), SYSDATETIME(), CAST(GETDATE() AS DATE);
```

### 7.2 YEAR / MONTH / DAY

Gets a date part as a number.

```sql
SELECT imie_wroga FROM wrogowie_kocurow WHERE YEAR(data_incydentu) = 2009;
```

### 7.3 DATEPART

Any date part as a number; `WEEKDAY` depends on `@@DATEFIRST`.

```sql
SELECT DATEPART(QUARTER, w_stadku_od), DATEPART(WEEKDAY, w_stadku_od) FROM kocury;
```

### 7.4 DATEADD

Adds days, months, years… (no `date + n`).

```sql
SELECT DATEADD(MONTH, 6, w_stadku_od) FROM kocury;
```

### 7.5 DATEDIFF

Counts unit boundaries crossed, not full units.

```sql
SELECT pseudo FROM kocury WHERE w_stadku_od <= DATEADD(YEAR, -15, GETDATE());
```

### 7.6 EOMONTH

Last day of the month, optionally n months ahead.

```sql
SELECT EOMONTH(GETDATE()), EOMONTH(GETDATE(), 1);
```

### 7.7 DATETRUNC

Start of the month/year/… (since 2022).

```sql
SELECT DATETRUNC(MONTH, GETDATE());
```

### 7.8 DATEFROMPARTS

Builds a date from numbers.

```sql
SELECT DATEFROMPARTS(2009, 1, 7);
```

### 7.9 DATENAME

Name of a date part, in the session language.

```sql
SELECT DATENAME(MONTH, w_stadku_od), DATENAME(WEEKDAY, w_stadku_od) FROM kocury;
```

### 7.10 Last Wednesday of month

Last day minus the days back to Wednesday, independent of `@@DATEFIRST`.

```sql
SELECT DATEADD(DAY, -((DATEPART(WEEKDAY, EOMONTH(GETDATE())) + @@DATEFIRST + 3) % 7), EOMONTH(GETDATE()));
```

## 8. Conversions

### 8.1 CAST

Standard type conversion.

```sql
SELECT CAST(przydzial_myszy AS VARCHAR(10)) FROM kocury;
```

### 8.2 CONVERT

Conversion with a style code (`23` = `yyyy-mm-dd`).

```sql
SELECT CONVERT(VARCHAR(10), w_stadku_od, 23) FROM kocury;
```

### 8.3 FORMAT

.NET-style formatting of dates and numbers.

```sql
SELECT FORMAT(w_stadku_od, 'yyyy-MM-dd'), FORMAT(w_stadku_od, 'MMMM') FROM kocury;
```

### 8.4 TRY_CAST

Returns `NULL` instead of an error when conversion fails.

```sql
SELECT TRY_CAST('abc' AS INT);
```

## 9. Conditionals

### 9.1 CASE WHEN

Conditions checked in order; all branches must return the same type.

```sql
SELECT CASE WHEN 12 * przydzial_myszy > 660 THEN CAST(12 * przydzial_myszy AS VARCHAR) ELSE 'Ponizej 660' END FROM kocury;
```

### 9.2 CASE value

Compares one expression against values.

```sql
SELECT CASE plec WHEN 'M' THEN 'Kocur' ELSE 'Kotka' END FROM kocury;
```

### 9.3 IIF

Short if-else.

```sql
SELECT IIF(plec = 'M', 'Kocur', 'Kotka') FROM kocury;
```

### 9.4 GREATEST / LEAST

Largest / smallest of the arguments (since 2022).

```sql
SELECT pseudo, GREATEST(przydzial_myszy, ISNULL(myszy_extra, 0)) FROM kocury;
```

## 10. Grouping

### 10.1 COUNT

`COUNT(*)` counts rows, `COUNT(col)` non-`NULL`s, `COUNT(DISTINCT col)` unique values.

```sql
SELECT COUNT(*), COUNT(myszy_extra), COUNT(DISTINCT nr_bandy) FROM kocury;
```

### 10.2 SUM / AVG / MIN / MAX

Aggregates; `AVG` of an `INT` column returns an `INT`.

```sql
SELECT SUM(przydzial_myszy), AVG(przydzial_myszy), MIN(w_stadku_od), MAX(przydzial_myszy) FROM kocury;
```

### 10.3 GROUP BY

One row per group; every non-aggregated column must be listed, aliases not allowed.

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

### 10.6 STRING_AGG

Joins a group's values into one string.

```sql
SELECT nr_bandy, STRING_AGG(pseudo, ', ') WITHIN GROUP (ORDER BY pseudo) FROM kocury GROUP BY nr_bandy;
```

### 10.7 Group by expression

The full expression must be repeated in `GROUP BY`.

```sql
SELECT MONTH(w_stadku_od), COUNT(*) FROM kocury GROUP BY MONTH(w_stadku_od);
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

### 11.6 No USING / NATURAL

Always write the join condition with `ON`.

```sql
SELECT K.pseudo, B.nazwa FROM kocury K JOIN bandy B ON B.nr_bandy = K.nr_bandy;
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

### 11.11 CROSS / OUTER APPLY

Subquery run per row that can use its columns (`OUTER` keeps rows without a match).

```sql
SELECT K.pseudo, O.imie_wroga FROM kocury K OUTER APPLY (SELECT TOP 1 imie_wroga FROM wrogowie_kocurow WK WHERE WK.pseudo = K.pseudo ORDER BY data_incydentu DESC) O;
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

Uses a query result as a table; the alias is required and `ORDER BY` inside needs `TOP`.

```sql
SELECT * FROM (SELECT nr_bandy, SUM(przydzial_myszy) AS suma FROM kocury GROUP BY nr_bandy) AS sumy WHERE suma > 200;
```

### 13.9 WITH (CTE)

Names a subquery so it can be reused; end the previous statement with `;`.

```sql
WITH sumy AS (SELECT nr_bandy, SUM(przydzial_myszy) AS suma FROM kocury GROUP BY nr_bandy) SELECT * FROM sumy WHERE suma > 200;
```

## 14. Hierarchical queries

### 14.1 Recursive CTE

Anchor rows `UNION ALL` a step that joins back to the CTE (no `RECURSIVE` keyword).

```sql
WITH drzewo AS (SELECT pseudo FROM kocury WHERE szef IS NULL UNION ALL SELECT K.pseudo FROM kocury K JOIN drzewo D ON K.szef = D.pseudo) SELECT * FROM drzewo;
```

### 14.2 Level

Carry a counter column, increased in each step.

```sql
WITH drzewo AS (SELECT pseudo, 1 AS poziom FROM kocury WHERE funkcja = 'BANDZIOR' UNION ALL SELECT K.pseudo, D.poziom + 1 FROM kocury K JOIN drzewo D ON K.szef = D.pseudo) SELECT REPLICATE(' ', 4 * (poziom - 1)) + pseudo FROM drzewo;
```

### 14.3 Upwards

Swap the join direction to walk from a cat to its bosses.

```sql
WITH szefowie AS (SELECT pseudo, szef FROM kocury WHERE pseudo = 'ZERO' UNION ALL SELECT K.pseudo, K.szef FROM kocury K JOIN szefowie S ON K.pseudo = S.szef) SELECT pseudo FROM szefowie;
```

### 14.4 Path and root

Carry the root value and a path; both parts must have the exact same type, so cast.

```sql
WITH sciezki AS (SELECT imie AS korzen, szef, CAST(imie AS VARCHAR(200)) AS sciezka FROM kocury WHERE funkcja = 'KOT' UNION ALL SELECT S.korzen, K.szef, CAST(S.sciezka + ' | ' + K.imie AS VARCHAR(200)) FROM sciezki S JOIN kocury K ON K.pseudo = S.szef) SELECT korzen, sciezka FROM sciezki WHERE szef IS NULL;
```

### 14.5 Leaf check

A row is a leaf when nobody points to it.

```sql
SELECT K.pseudo FROM kocury K WHERE NOT EXISTS (SELECT 1 FROM kocury P WHERE P.szef = K.pseudo);
```

### 14.6 Tree order

Sort by the path built from the root down (Oracle's `ORDER SIBLINGS BY`).

```sql
WITH drzewo AS (SELECT pseudo, CAST(pseudo AS VARCHAR(200)) AS sciezka FROM kocury WHERE szef IS NULL UNION ALL SELECT K.pseudo, CAST(D.sciezka + '/' + K.pseudo AS VARCHAR(200)) FROM kocury K JOIN drzewo D ON K.szef = D.pseudo) SELECT pseudo FROM drzewo ORDER BY sciezka;
```

### 14.7 MAXRECURSION

Recursion depth limit (default 100, 0 = none).

```sql
WITH liczby AS (SELECT 1 AS n UNION ALL SELECT n + 1 FROM liczby WHERE n < 500) SELECT n FROM liczby OPTION (MAXRECURSION 0);
```

### 14.8 GENERATE_SERIES

Generates numbers 1..n (since 2022).

```sql
SELECT value FROM GENERATE_SERIES(1, 12);
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
SELECT pseudo, ROUND(100.0 * przydzial_myszy / SUM(przydzial_myszy) OVER (PARTITION BY nr_bandy), 0) AS proc FROM kocury;
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

### 15.9 Top-N per group

Window functions aren't allowed in `WHERE`, so filter in an outer query.

```sql
SELECT * FROM (SELECT pseudo, nr_bandy, RANK() OVER (PARTITION BY nr_bandy ORDER BY przydzial_myszy DESC) AS rnk FROM kocury) AS ranking WHERE rnk = 1;
```

## 16. Pivot

### 16.1 PIVOT

Turns row values into columns; values go in `[ ]`, only one aggregate.

```sql
SELECT nr_bandy, [M] AS samce, [D] AS samice FROM (SELECT nr_bandy, plec, przydzial_myszy FROM kocury) AS zrodlo PIVOT (SUM(przydzial_myszy) FOR plec IN ([M], [D])) AS wynik;
```

### 16.2 UNPIVOT

Turns columns into rows; the columns must have the same type, `NULL`s are skipped.

```sql
SELECT pseudo, rodzaj, ile FROM (SELECT pseudo, przydzial_myszy, myszy_extra FROM kocury) AS zrodlo UNPIVOT (ile FOR rodzaj IN (przydzial_myszy, myszy_extra)) AS wynik;
```

### 16.3 Unpivot with APPLY

Columns into rows with your own labels, keeping `NULL`s.

```sql
SELECT K.pseudo, U.rodzaj, U.ile FROM kocury K CROSS APPLY (VALUES ('PRZYDZIAL', K.przydzial_myszy), ('EXTRA', K.myszy_extra)) AS U(rodzaj, ile);
```

### 16.4 Pivot with CASE

Portable pivot: one conditional aggregate per column.

```sql
SELECT nr_bandy, SUM(CASE WHEN plec = 'M' THEN przydzial_myszy ELSE 0 END) AS samce, SUM(CASE WHEN plec = 'D' THEN przydzial_myszy ELSE 0 END) AS samice FROM kocury GROUP BY nr_bandy;
```

## 17. sqlcmd

### 17.1 GO

Sends the batch typed so far to the server (not SQL, a sqlcmd command).

```sql
SELECT * FROM kocury;
GO
```

### 17.2 :r

Runs a script file.

```sql
:r lista3/zad1.sql
```

### 17.3 -I flag

Turns on `QUOTED_IDENTIFIER`, required for filtered indexes (used in `db.sh`).

```sql
sqlcmd -S localhost -U sa -P Admin_123 -C -I
```

### 17.4 sp_help

Shows a table's columns and constraints.

```sql
EXEC sp_help 'kocury';
```

### 17.5 sys.tables

Lists tables.

```sql
SELECT name FROM sys.tables;
```

### 17.6 EXIT

Quits sqlcmd.

```sql
EXIT
```
