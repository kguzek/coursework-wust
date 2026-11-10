-- Run as KONRAD in FREEPDB1 on the database from lista 1; produces results/oracle.txt.
WHENEVER OSERROR EXIT FAILURE
WHENEVER SQLERROR EXIT SQL.SQLCODE
SET FEEDBACK ON
SET PAGESIZE 1000
SET LINESIZE 120
SET TRIMSPOOL ON
SET TRIMOUT ON
SET TAB OFF

COLUMN banner_full FORMAT A90
COLUMN "W stadku przed szefem lub bez incydentu" FORMAT A40
COLUMN "Przed Jackiem" FORMAT A13
COLUMN "Nie sa niczyim szefem" FORMAT A21
COLUMN "Miesiac" FORMAT A10
COLUMN "Droga sluzbowa" FORMAT A30
COLUMN "Imiona kolejnych szefow" FORMAT A40

SELECT banner_full FROM v$version;
SELECT TO_CHAR(SYSDATE, 'YYYY-MM-DD') AS data_wykonania FROM dual;

SET ECHO ON
@@oracle-01_queries.sql
SET ECHO OFF
EXIT SUCCESS
