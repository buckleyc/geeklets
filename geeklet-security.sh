#!/usr/bin/env zsh

# Check security on this Mac

# set colors
if tput setaf 1 &> /dev/null; then
	tput sgr0; # reset colors
	bold=$(tput bold);
	reset=$(tput sgr0);
	# Solarized colors, taken from http://git.io/solarized-colors.
	black=$(tput setaf 0);
	blue=$(tput setaf 33);
	cyan=$(tput setaf 37);
	green=$(tput setaf 64);
	orange=$(tput setaf 166);
	purple=$(tput setaf 125);
	red=$(tput setaf 124);
	violet=$(tput setaf 61);
	white=$(tput setaf 15);
	yellow=$(tput setaf 136);
else
	bold='';
	reset="\e[0m";
	black="\e[1;30m";
	blue="\e[1;34m";
	cyan="\e[1;36m";
	green="\e[1;32m";
	orange="\e[1;33m";
	purple="\e[1;35m";
	red="\e[1;31m";
	violet="\e[1;35m";
	white="\e[1;37m";
	yellow="\e[1;33m";
fi;

# reporting
function fatal() {
	printf "${red}%s${reset}\n" "$@"
}
function warning() {
	printf "${yellow}%s${reset}\n" "$@"
}
function info() {
	printf "${green}%s${reset}\n" "$@"
}
function heading() {
	echo "# $@ ..."
}
# System Integrity Protection status
cmd="csrutil"
if (( $+commands[${cmd}] )); then
	heading "System Integrity Protection"
	cmdcheck=$(${cmd} status)
	if [[ "${(U)cmdcheck}" != *"ENABLED"* ]]; then
		warning "WARNING: ${cmdcheck}\n"
		echo "  Suggest you enable System Integrity Protection by entering \"${bold}${cmd} enable${reset}\""
	else
		info "${cmdcheck}"
	fi
fi


# Filevault
# fdesetup status
cmd="fdesetup"
if (( $+commands[${cmd}] )); then
	heading "Filevault"
	cmdcheck=$(${cmd} status)
	if [[ "${(U)cmdcheck}" != *"IS ON"* ]]; then
		fatal "WARNING: ${cmdcheck}\n"
		echo "  Suggest you enable Filevault by entering \"$(warning "${bold}${cmd} enable${reset}")\""
	else
		info "${cmdcheck}"
	fi
fi


# Firewall
heading "Firewall"
cmdcheck=$(/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate)
if [[ "${(U)cmdcheck}" != *"ENABLED"* ]]; then
	fatal "WARNING: ${cmdcheck}\n"
	warning "  Suggest you enable Firewall by entering \"$(warning "/usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on")\""
else
	info "${cmdcheck}"
fi
cmdcheck=$(/usr/libexec/ApplicationFirewall/socketfilterfw --getstealthmode)
if [[ "${(U)cmdcheck}" != *"ENABLED"* ]]; then
	warning "WARNING: ${cmdcheck}\n"
	echo "  Suggest you enable Firewall Stealth Mode by entering \"/usr/libexec/ApplicationFirewall/socketfilterfw --getstealthmode on\""
else
	echo "${cmdcheck}"
fi


# Users
heading "Users"
# admin users
warning "'admin' $(dscl . -read /Groups/admin GroupMembership)"
# all users
info "All users: ${yellow}${$(dscl . list /Users | grep -v "_" | awk 'BEGIN{ORS=","}1')%,}${reset}"
