#!/usr/bin/env bash
# HostInfo - provides info about this Mac host

if command -v defaults >/dev/null 2>&1 ; then
  # hostname
  [ -z "${HOST++}" ] && echo "${HOSTNAME}" || echo "${HOST}"
  # when was model released
  when=$(defaults read  ~/Library/Preferences/com.apple.SystemProfiler.plist 'CPU Names' | cut -sd '"' -f 4 | uniq)
  echo "${when}"
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
  # echo "memory = ${mem}"
  kernel=$(sysctl -n kern.version)
  echo ${kernel} | cut -f1 -d":"
  osproductversion=$(sysctl -n kern.osproductversion)
  echo "Mac OS X ${osproductversion}"
fi

if command -v system_profiler >/dev/null 2>&1 ; then
  # SPHardwareDataType
  system_profiler SPHardwareDataType | sed -e '/^\s*$/d' -e 's/^[ \t]*//' | tail +3
fi

