#!/usr/bin/env bash
# Calendar - provides info about calendar events
# requires gcalcli (pip install gcalcli)

if [ -x /usr/local/bin/gcalcli ] ; then # command -v gcalcli >/dev/null 2>&1 ; then
  # get calendar events from Google Calendar
  echo "CALENDAR take 2"
  /usr/local/bin/gcalcli --lineart fancy agenda
fi
