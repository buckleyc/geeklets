#!/usr/bin/env bash
# Calendar - provides info about calendar events
# requires gcalcli (pip install gcalcli)

if command -v gcalcli >/dev/null 2>&1 ; then
  # hostname
  gcalcli --lineart fancy agenda
fi
