#!/usr/bin/env bash
# A subshell also isolates settings when the image sources this script.
(
    set -eu

    sqlplus -s /nolog <<SQL
WHENEVER OSERROR EXIT FAILURE
WHENEVER SQLERROR EXIT SQL.SQLCODE ROLLBACK
SET DEFINE OFF
CONNECT ${APP_USER}/"${APP_USER_PASSWORD}"@//localhost:1521/FREEPDB1
@/pbd/sql/oracle-01_schema.sql
@/pbd/sql/oracle-02_seed.sql
@/pbd/sql/oracle-03_verify.sql
EXIT SUCCESS
SQL
)
