#! /bin/sh

PATH="/bin:/usr/bin:/usr/sbin:/sbin"

# Zope root folder
ZOPE_HOME=/usr/lib/zope

# product instalation location
INSTANCE_HOME=/var/lib/zope
INST_HOME=${INSTANCE_HOME}

# lacalization of pid and log files for ZOE
CLIENT_HOME=/var/lib/zope

export INST_HOME INSTANCE_HOME ZOPE_HOME PATH CLIENT_HOME

# user to run Zope
ZOPE_USER=zope

# put !0 to create separate management process
CREATE_MANAGEMENT=yes

# initial NUMBER_OF_THREADS
NUMBER_OF_THREADS=4

# DEBUG_MODE
DEBUG_MODE=0

# ip address
IP_ADDRESS=''

# HTTP_PORT
HTTP_PORT=18080

# FTP_PORT
FTP_PORT=18021

# MONITOR_PORT... if equals '-' then monitor server is disabled
MONITOR_PORT='-'

# LOG_FILE
LOG_FILE=/var/log/zope

# DET_LOG_FILE... detailed log file
DET_LOG_FILE=/var/log/zope.detailed

# internationalization
LOC='pl_PL'

exec python $ZOPE_HOME/z2.py            \
	-u      $ZOPE_USER              \
	-z      $ZOPE_HOME              \
	-w      $HTTP_PORT              \
	-f      $FTP_PORT               \
	-m      $MONITOR_PORT           \
	-L	$LOC                    \
	-Z      $CREATE_MANAGEMENT      \
	-a	$IP_ADDRESS		\
	-t 	$NUMBER_OF_THREADS	\
	-D	$DEBUG_MODE		\
	-M	$DET_LOG_FILE           \
	-l      $LOG_FILE               \
	>>      $LOG_FILE 2>&1          \
	&
