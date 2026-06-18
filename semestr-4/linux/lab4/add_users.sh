#!/bin/bash

if ! command -v gtr >/dev/null 2>&1; then
  # Ensure GNU `tr` implementation is used
  gtr=tr
fi

{
  # skip header
  read -r _
  while IFS=, read -r EmployeeID Department DistinguishedName Enabled GivenName mail Manager Name ObjectClass ObjectGUID OfficePhone SamAccountName SID sn Surname Title UserPrincipalName; do
    login="$SamAccountName"
    password=$(cat /dev/urandom | gtr -dc 'A-Za-z0-9' | head -c 13)
    display_name="$Name"
    useradd --create-home --comment "$display_name" "$login"
    echo "$login:$password" | chpasswd
  done 
} < "$1"

