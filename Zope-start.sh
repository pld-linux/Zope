#! /bin/sh

# This is Zope ZServer startscript for PLD Linux
#

ZOPE_BASE=/usr/lib/zope
CLIENT_HOME=$INSTANCE_HOME/var

# prepare directories

if [ "x$ZOPE_USER" = "x" ]; then
    ZOPE_USER="zope"
fi

ZOPE_GROUP=`id -ng $ZOPE_USER`

if [ ! -d $INSTANCE_HOME ]; then
    mkdir $INSTANCE_HOME
fi

chmod 1701 $INSTANCE_HOME
chown root:$ZOPE_GROUP $INSTANCE_HOME

if [ ! -d $INSTANCE_HOME/var ]; then
    mkdir $INSTANCE_HOME/var
fi

chown root:$ZOPE_GROUP $INSTANCE_HOME/var
chmod 1701 $INSTANCE_HOME/var

if [ ! -d /var/log/zope ]; then
    mkdir /var/log/zope
    chmod o-rwx /var/log/zope
    chown root:root /var/log/zope
fi

# prepare parameters

if [ "$WATCHDOG" = "0" ]; then
    manager=
else
    manager="-Z 1"
fi

if [ "x$CGIBIN_BASE" = "x" ]; then
    p_string=" "
else
    p_string="-p $CGIBIN_FILE"
fi

if [ "x$DEBUG_MODE" = "xyes" -o "x$DEBUG_MODE" = "x1" ]; then
    debugging="-D 1"
else
    debugging=
fi

if [ "x$LOG_FILE" = "x" -o "x$LOG_FILE" = "x0" ]; then
    LOG_FILE=/var/log/zope/$INSTANCE_NAME.log
fi

if [ "x$DETAILED_LOG_FILE" = "x" -o "x$DETAILED_LOG_FILE" = "x0" ]; then
    details=
else
    if [ "x$DETAILED_LOG_FILE" = "xyes" -o "x$DETAILED_LOG_FILE" = "x1" ]; then
	details="-M /var/log/zope/$INSTANCE_NAME-detailed.log"
    else
	details="-M $DETAILED_LOG_FILE"
    fi
fi

if [ "x$LOC" != "x" ]; then
    locale="-L $LOC"
else
    locale=
fi

if [ "x$ICP_PORT" = "x" -o "x$ICP_PORT" = "x0" ]; then
    icpstr=" "
else
    icpstr="--icp $ICP_PORT"
fi

if [ "x$IP_ADDRESS" = "x" -o "x$IP_ADDRESS" = "x0" ]; then
    ipstr=" "
else
    ipstr="-a '$IP_ADDRESS'"
fi

# show what we're going to do

if [ "x$debugging" != "x" ]; then
cat <<EE | ( while read line; do echo "zope-start: $line"; done ) >>$LOG_FILE
`date`
Instance name: $INSTANCE_NAME
Executing:
exec python $ZOPE_BASE/z2.py
    -z $INSTANCE_HOME
    -t $NUMBER_OF_THREADS
    -u $ZOPE_USER 
    -w $HTTP_PORT
    -f $FTP_PORT
    -l $LOG_FILE
    $ipstr
    $icpstr
    $manager
    $locale
    $debugging
    $p_string
    $details
>> $LOG_FILE 2>&1
EE
fi

# call server

exec python $ZOPE_BASE/z2.py \
-z "$INSTANCE_HOME"  \
-t "$NUMBER_OF_THREADS" \
-u "$ZOPE_USER"  \
-w "$HTTP_PORT"  \
-f "$FTP_PORT"   \
-W "$WEBDAV_PORT"   \
-l "$LOG_FILE"   \
$ipstr \
$icpstr  \
$manager \
$locale  \
$debugging \
$p_string  \
$details   \
>> $LOG_FILE 2>&1 \
&
