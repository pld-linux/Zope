#! /bin/sh
# $Id$

. /etc/rc.d/init.d/functions

if [ "$1" = "-D" ] ; then
	Z_flag="-Z 0"
	shift
else
	Z_flag="-Z 1"
fi

if [ -z "$1" -o '!' -f "/etc/zope/$1/instance" ] ; then
	echo "Usage: "
	echo "  $0 [-D] instance_name"
	exit 1
fi

INSTANCE_NAME="$1"

ZOPE_HOME=/usr/lib/zope
INSTANCE_HOME="/var/lib/zope/$INSTANCE_NAME"
ZOPE_USER=zope
LOG_FILE="/var/log/zope/$INSTANCE_NAME/zope.log"
STARTUP_LOG_FILE="/var/log/zope/$INSTANCE_NAME/startup.log"
DETAILED_LOG_FILE="/var/log/zope/$INSTANCE_NAME/zope-detailed.log"

. "/etc/zope/$INSTANCE_NAME/instance"

if [ -n "$IP_ADDRESS" ] ; then
	a_flag="-a $IP_ADDRESS"
else
	a_flag=""
fi
if [ -n "$HTTP_PORT" ] ; then
	w_flag="-w $HTTP_PORT"
else
	w_flag=""
fi
if [ -n "$FTP_PORT" ] ; then
	f_flag="-f $FTP_PORT"
else
	f_flag=""
fi
if [ -n "$ICP_PORT" ] ; then
	icp_flag="--icp $ICP_PORT"
else
	icp_flag=""
fi
if [ -n "$WEBDAV_PORT" ] ; then
	W_flag="-W $WEBDAV_PORT"
else
	W_flag=""
fi
if [ -n "$NUMBNER_OF_THREADS" ] ; then
	t_flag="-t $NUMBER_OF_THREADS"
else
	t_flag=""
fi
if [ -n "$CGIBIN_FILE" ] ; then
	p_flag="-p $CGIBIN_FILE"
else
	p_flag=""
fi
if [ -n "$LOC" ] ; then
	L_flag="-L $LOC"
else
	L_flag=""
fi
if [ -n "LOG_FILE" ] ; then
	l_flag="-l $LOG_FILE"
else
	l_flag=""
fi
if [ -n "DETAILED_LOG_FILE" ] ; then
	M_flag="-M $DETAILED_LOG_FILE"
else
	M_flag=""
fi

PATH="/bin:/usr/bin:/usr/sbin:/sbin"
INST_HOME="${INSTANCE_HOME}"
CLIENT_HOME="${INSTANCE_HOME}/var"
export INST_HOME INSTANCE_HOME ZOPE_HOME PATH CLIENT_HOME

exec /usr/bin/python \
	$ZOPE_HOME/z2.py -z "$INSTANCE_HOME" -u $ZOPE_USER \
	$a_flag $w_flag $f_flag $icp_flag $W_flag \
	$t_flag $p_flag $L_flag $Z_flag $l_flag $M_flag
