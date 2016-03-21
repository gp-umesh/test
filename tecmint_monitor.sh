#! /bin/bash
# unset any variable which system may be using

# clear the screen
#clear

unset tecreset os architecture kernelrelease internalip externalip nameserver loadaverage

while getopts iv name
do
        case $name in
          i)iopt=1;;
          v)vopt=1;;
          *)echo "Invalid arg";;
        esac
done

if [[ ! -z $iopt ]]
then
{
wd=$(pwd)
basename "$(test -L "$0" && readlink "$0" || echo "$0")" > /tmp/scriptname
scriptname=$(echo -e -n $wd/ && cat /tmp/scriptname)
su -c "cp $scriptname /usr/bin/monitor" root && echo "Congratulations! Script Installed, now run monitor Command" || echo "Installation failed"
}
fi

if [[ ! -z $vopt ]]
then
{
echo -e "tecmint_monitor version 0.1\nDesigned by Tecmint.com\nReleased Under Apache 2.0 License"
}
fi

if [[ $# -eq 0 ]]
then
{


# Define Variable tecreset
tecreset=$1

# Check if connected to Internet or not
ping -c 1 google.com &> /dev/null && echo -e "Internet: $tecreset Connected" || echo -e "Internet: $tecreset Disconnected"

# Check OS Type
os=$(uname -o)
echo -e "Operating System Type :" $tecreset $os

# Check OS Release Version and Name
cat /etc/os-release | grep 'NAME\|VERSION' | grep -v 'VERSION_ID' | grep -v 'PRETTY_NAME' > /tmp/osrelease
echo -n -e "OS Name :" $tecreset  && cat /tmp/osrelease | grep -v "VERSION" | cut -f2 -d\"
echo -n -e "OS Version :" $tecreset && cat /tmp/osrelease | grep -v "NAME" | cut -f2 -d\"

# Check Architecture
architecture=$(uname -m)
echo -e "Architecture :" $tecreset $architecture

# Check Kernel Release
kernelrelease=$(uname -r)
echo -e "Kernel Release :" $tecreset $kernelrelease

# Check hostname
echo -e "Hostname :" $tecreset $HOSTNAME

# Check Internal IP
internalip=$(hostname -I)
echo -e "Internal IP :" $tecreset $internalip

# Check External IP
externalip=$(curl -s ipecho.net/plain;echo)
echo -e "External IP : "$tecreset $externalip

# Check DNS
nameservers=$(cat /etc/resolv.conf | sed '1 d' | awk '{print $2}')
echo -e "Name Servers :" $tecreset $nameservers 

# Check Logged In Users
who>/tmp/who
echo -e "Logged In users :" $tecreset && cat /tmp/who 

# Check RAM and SWAP Usages
free -m | grep -v + > /tmp/ramcache
echo -e "Ram Usages :" $tecreset
cat /tmp/ramcache | grep -v "Swap"
echo -e "Swap Usages :" $tecreset
cat /tmp/ramcache | grep -v "Mem"

# Check Disk Usages
df -h| grep 'Filesystem\|/dev/sda*' > /tmp/diskusage
echo -e "Disk Usages :"  $tecreset
cat /tmp/diskusage

# Check Load Average
loadaverage=$(top -n 1 -b | grep "top" | cut -f1 -d'
')
echo -e "Load Average :" $tecreset $loadaverage

# Check Task and CPU Usage
taskusage=$(top -n 1 -b | grep "Tasks:")
cpuusage=$(top -n 1 -b | grep "Cpu(s):")
echo -e "Task Usage :" $tecreset $taskusage
echo -e "CPU Usage :" $tecreset $cpuusage

# Check CPU Temperature
cputemp=$(sensors)
echo -e "CPU Temperature :" $tecreset $cputemp

# Check Last Start Time
teclaststarttime=$(who -b)
echo -e "Last Start Time/(HH:MM) :" $tecreset $teclaststarttime

# Check System Uptime
tecuptime=$(uptime | awk '{print $3,$4}' | cut -f1 -d,)
echo -e "System Uptime Days/(HH:MM) :" $tecreset $tecuptime

# Last Login IP addr.
ipaddr=$(last $user -n 1 | awk '{print $3}' | cut -f1 -d'
')
echo -e "Last Login IP Address:" $tecreset $ipaddr

# Unset Variables
unset tecreset os architecture kernelrelease internalip externalip nameserver loadaverage tecuptime teclaststarttime taskusage cputemp ipaddr

# Remove Temporary Files
rm /tmp/osrelease /tmp/who /tmp/ramcache /tmp/diskusage
}
fi
shift $(($OPTIND -1))
