-- Run as KONRAD in FREEPDB1 after schema creation and seeding.
WHENEVER OSERROR EXIT FAILURE
WHENEVER SQLERROR EXIT SQL.SQLCODE ROLLBACK
SET ECHO OFF
SET FEEDBACK ON
SET PAGESIZE 1000
SET LINESIZE 240
SET TRIMSPOOL ON
SET TAB OFF
ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS';

COLUMN banner_full FORMAT A100
COLUMN schema_name FORMAT A15
COLUMN database_name FORMAT A15
COLUMN relacja FORMAT A20
COLUMN imie FORMAT A15
COLUMN plec FORMAT A4
COLUMN pseudo FORMAT A15
COLUMN funkcja FORMAT A10
COLUMN szef FORMAT A15
COLUMN nazwa FORMAT A20
COLUMN teren FORMAT A15
COLUMN szef_bandy FORMAT A15
COLUMN imie_wroga FORMAT A15
COLUMN gatunek FORMAT A15
COLUMN lapowka FORMAT A20
COLUMN opis_incydentu FORMAT A50
COLUMN table_name FORMAT A20
COLUMN constraint_type FORMAT A15
COLUMN status FORMAT A10
COLUMN validated FORMAT A15
COLUMN deferrable FORMAT A15

PROMPT === Oracle version and application schema ===
SELECT banner_full FROM v$version;
SELECT SYS_CONTEXT('USERENV','CURRENT_SCHEMA') AS schema_name,
       SYS_CONTEXT('USERENV','CON_NAME') AS database_name FROM dual;

PROMPT === Row counts and missing references ===
@@oracle-03_verify.sql

PROMPT === Funkcje ===
SELECT * FROM funkcje ORDER BY funkcja;
PROMPT === Bandy ===
SELECT * FROM bandy ORDER BY nr_bandy;
PROMPT === Kocury ===
SELECT * FROM kocury ORDER BY pseudo;
PROMPT === Wrogowie ===
SELECT * FROM wrogowie ORDER BY imie_wroga;
PROMPT === Wrogowie_kocurow ===
SELECT * FROM wrogowie_kocurow ORDER BY pseudo, imie_wroga;

PROMPT === Constraint status (C includes NOT NULL) ===
SELECT table_name, constraint_type, status, validated, deferrable,
       COUNT(*) AS constraint_count
FROM user_constraints
WHERE table_name IN ('FUNKCJE','BANDY','KOCURY','WROGOWIE','WROGOWIE_KOCUROW')
GROUP BY table_name, constraint_type, status, validated, deferrable
ORDER BY table_name, constraint_type;

PROMPT === Constraint and default tests ===
@@oracle-04_test.sql
PROMPT === Final row counts after rollback ===
@@oracle-03_verify.sql
EXIT SUCCESS
