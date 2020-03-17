#!/usr/bin/env zsh

# Check security on this Mac

# System Integrity Protection status
cmd="csrutil"
if (( $+commands[${cmd}] )); then
	cmdcheck=$(${cmd} status)
	# cmdstatus=$(echo ${cmdcheck} | cut -d':' -f 2 | tr -d -c '[:alpha:]')
	if [[ "${(U)cmdcheck}" != *"ENABLED"* ]]; then
		echo "WARNING: ${cmdcheck}"
		echo "  Suggest you enable System Integrity Protection by entering \"${cmd} enable\""
	else
		echo "${cmdcheck}"
	fi
fi


# Filevault
# fdesetup status
cmd="fdesetup"
if (( $+commands[${cmd}] )); then
	cmdcheck=$(${cmd} status)
	# cmdstatus=$(echo ${cmdcheck})
	if [[ "${(U)cmdcheck}" != *"IS ON"* ]]; then
		echo "WARNING: ${cmdcheck}"
		echo "  Suggest you enable Filevault by entering \"${cmd} enable\""
	else
		echo "${cmdcheck}"
	fi
fi


# Firewall
cmdcheck=$(/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate)
# cmdstatus=$(echo ${cmdcheck})
if [[ "${(U)cmdcheck}" != *"ENABLED"* ]]; then
	echo "WARNING: ${cmdcheck}"
	echo "  Suggest you enable Firewall by entering \"/usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on\""
else
	echo "${cmdcheck}"
fi
cmdcheck=$(/usr/libexec/ApplicationFirewall/socketfilterfw --getstealthmode)
# cmdstatus=$(echo ${cmdcheck})
if [[ "${(U)cmdcheck}" != *"ENABLED"* ]]; then
	echo "WARNING: ${cmdcheck}"
	echo "  Suggest you enable Firewall Stealth Mode by entering \"/usr/libexec/ApplicationFirewall/socketfilterfw --getstealthmode on\""
else
	echo "${cmdcheck}"
fi


# Users
# admin users
echo "'admin' $(dscl . -read /Groups/admin GroupMembership)"
# all users
echo "All users: $(dscl . list /Users | grep -v "_" | tr -s "\n" ', ')"
