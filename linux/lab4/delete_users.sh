#!/bin/bash

{
  # skip header
  read -r _
  while IFS=, read -r EmployeeID Department DistinguishedName Enabled GivenName mail Manager Name ObjectClass ObjectGUID OfficePhone SamAccountName SID sn Surname Title UserPrincipalName; do
    login="$SamAccountName"
    userdel "$login"
  done 
} < "$1"

