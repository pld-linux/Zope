#! /bin/sh
# $Id$

PATH="/bin:/usr/bin:/usr/sbin:/sbin"
ZOPE_HOME=/usr/lib/zope
INSTANCE_HOME=/var/lib/zope
INST_HOME=${INSTANCE_HOME}
CLIENT_HOME=/var/lib/zope

export INST_HOME INSTANCE_HOME ZOPE_HOME PATH CLIENT_HOME

exec python $ZOPE_HOME/z2.py            \
	-u      zope                    \
	-z      /usr/lib/zope           \
	-Z      /var/run/zwatchdog.pid  \
	-w      8080                    \
	-f      8021                    \
	-m      ''                      \
	-l      /var/log/zope           \
	>>      /var/log/zope 2>&1      \
	&
