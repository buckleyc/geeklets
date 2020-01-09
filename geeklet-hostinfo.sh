#!/usr/bin/env bash
# HostInfo - provides info about this Mac host

if command -v defaults >/dev/null 2>&1 ; then
  when=$(defaults read  ~/Library/Preferences/com.apple.SystemProfiler.plist 'CPU Names' | cut -sd '"' -f 4 | uniq)
  echo "$HOSTNAME = ${when}"
fi
if command -v sysctl >/dev/null 2>&1 ; then
  model=$(sysctl -n hw.model)
  cpu_brand_string=$(sysctl -n machdep.cpu.brand_string)
  memsize=$(sysctl -n hw.memsize)
  if (( memsize > 1024**3 )); then
    mem="$(( memsize/1024**3 )) GB"
  else
    mem="$(( memsize/1024**2 )) MB"
  fi
  echo "memory = ${mem}"
  kernel=$(sysctl -n kern.version)
  echo ${kernel} | cut -f1 -d":"
  osproductversion=$(sysctl -n kern.osproductversion)
  echo "Mac OS X ${osproductversion}"

fi
