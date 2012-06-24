%include        /usr/lib/rpm/macros.python

Summary:	An application server and portal toolkit for building Web sites
Summary(es):	Un servidor de aplicaciones y un conjunto de herramientas para la construcci�n de sitios Web
Summary(pl):	Serwer aplikacji i toolkit portalowy do tworzenia serwis�w WWW
Summary(pt_BR):	Um servidor de aplica��es e um conjunto de ferramentas para constru��o de sites Web
Name:		Zope
Version:	2.7.0
%define		sub_ver b2
Release:	1.%{sub_ver}
License:	Zope Public License (ZPL)
Group:		Networking/Daemons
Source0:	http://www.zope.org/Products/%{name}/%{version}%{sub_ver}/%{version}%{sub_ver}/%{name}-%{version}-%{sub_ver}.tgz
# Source0-md5:	a8f7f3ba81c4f50dc2d3b61e02f0fb45
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.logrotate
Source4:	%{name}-start.sh
Source5:	%{name}.instance
Patch0:		%{name}-python-2.3.2.patch
URL:		http://www.zope.org/
BuildRequires:	python-devel >= 2.2.3
BuildRequires:	perl
PreReq:		rc-scripts
Requires(pre):	/usr/bin/getgid
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(postun):	/usr/sbin/userdel
Requires(postun):	/usr/sbin/groupdel
Requires(post,preun):	/sbin/chkconfig
Requires:	logrotate
Requires:	python >= 2.2.3
Requires:	python-modules >= 2.2.3
Requires:	python-libs >= 2.2.3
%pyrequires_eq  python
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Z Object Programming Environment (Zope) is a free, Open Source
Python-based application server for building high-performance, dynamic
web sites, using a powerful and simple scripting object model and
high-performance, integrated object database.

%description -l es
Zope es una aplicaci�n basada en Python, Open Source[tm], para la
construcci�n de sitios din�micos, usa un modelo de escritura de
guiones poderoso y sencillo. Para instalar la aplicaci�n Zope, instale
ese paquete y despu�s, Zope-server, para un servidor HTTP integrado
simple, Zope-pcgi, para uso con el servidor Apache. Si desea instalar
solamente algunas partes de la aplicaci�n Zope, est�n diponibles otros
subpaquetes, usted debe instalar �stos en vez de ese RPM.

%description -l pl
Zope (Z Object Programming Environment - Obiektowe �rodowisko
Programistyczne Z) jest opartym o Pythona serwerem aplikacji do
tworzenia wysoko wydajnych, dynamicznych serwis�w WWW, przy u�yciu
u�ytecznego i prostego modelu obiektowego skrypt�w oraz wysoko
wydajnej zintegrowanej obiektowej bazy danych.

%description -l pt_BR
Zope � uma aplica��o baseada em Python, Open Source[tm], para
constru��o de sites din�micos, usando um modelo de scripting poderoso
e simples Para instalar o Zope, instale esse pacote e depois, ou o
Zope-server, para um servidor HTTP integrado simples, ou Zope-pcgi,
para uso com o Apache. Se voc� quiser instalar apenas algumas partes
do Zope, outros sub-pacotes est�o dispon�veis, e voc� deveria instalar
eles ao inv�s desse RPM.

%prep

%setup -q -n %{name}-%{version}-%{sub_ver}
%patch0 -p1

%build
perl -pi -e "s|data_dir\s+=\s+.*?join\(INSTANCE_HOME, 'var'\)|data_dir=INSTANCE_HOME|" lib/python/Globals.py

./configure \
	--prefix=/usr \
	--optimize

%{__make}

perl -pi -e "s|data_dir\s+=\s+.*?join\(INSTANCE_HOME, 'var'\)|data_dir=INSTANCE_HOME|" lib/python/Globals.py
# python wo_pcgi.py

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{/var/lib/zope/main,/var/run/zope,/var/log/zope,%{_examplesdir}} \
	$RPM_BUILD_ROOT{/etc/logrotate.d,/etc/sysconfig,/etc/rc.d/init.d} \
	$RPM_BUILD_ROOT{%{_sysconfdir}/zope/instances,%{_sbindir}}

%{__make} install INSTALL_FLAGS="--optimize=1 --root $RPM_BUILD_ROOT"

mv $RPM_BUILD_ROOT%{_libdir}{/python,/zope}
mv $RPM_BUILD_ROOT%{_bindir}{/zpasswd.py,/zpasswd}
mv $RPM_BUILD_ROOT{%{_prefix}/import,%{_examplesdir}/%{name}-%{version}}
rm -f $RPM_BUILD_ROOT%{_bindir}/*.py
rm -rf $RPM_BUILD_ROOT/usr/doc/
rm -rf $RPM_BUILD_ROOT/usr/skel/

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/zope
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/zope
install %{SOURCE3} $RPM_BUILD_ROOT/etc/logrotate.d/zope
install %{SOURCE4} $RPM_BUILD_ROOT%{_sbindir}/zope-start
install %{SOURCE5} $RPM_BUILD_ROOT/etc/zope/instances/main

#install utilities/zpasswd.py $RPM_BUILD_ROOT%{_bindir}/zpasswd
#install z2.py $RPM_BUILD_ROOT%{_libdir}/zope
#install var/Data.fs $RPM_BUILD_ROOT/var/lib/zope/main/Data.fs

python $RPM_BUILD_ROOT%{_bindir}/zpasswd -u zope -p zope -d localhost \
	$RPM_BUILD_ROOT/var/lib/zope/main/access

touch $RPM_BUILD_ROOT/var/log/zope/main.log
touch $RPM_BUILD_ROOT/var/log/zope/main-detailed.log

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ -z "`getgid zope`" ]; then
       echo "Making group zope"
       /usr/sbin/groupadd -r -f zope
fi
if [ -z "`id -u zope 2>/dev/null`" ]; then
       echo "Making user zope"
       /usr/sbin/useradd -r -d /var/lib/zope/main -s /bin/false -c "Zope User" -g zope zope
fi

%post
/sbin/chkconfig --add zope
was_stopped=0
if [ -f /var/lib/zope/Data.fs ]; then
	echo "Found the database in old location. Migrating..."
	if [ -f /var/lock/subsys/zope ]; then
	    /etc/rc.d/init.d/zope stop >&2
	    was_stopped=1
	fi
	umask 022
	[ -d /var/lib/zope/main ] && cd /var/lib/zope && mv -f * ./main 2>/dev/null
	touch /var/lib/zope/access
	if [ "x$was_stopped" = "x1" ]; then
	    /etc/rc.d/init.d/zope start >&2
	fi
	echo "Migration completed (new db location is /var/lib/zope/main)"
fi
if [ -f /var/lock/subsys/zope ]; then
	if [ "x$was_stopped" != "x1" ]; then
	    /etc/rc.d/init.d/zope restart >&2
	fi
else
	echo "Create inituser using \"zpasswd inituser\" in directory \"/var/lib/zope/main\"" >&2
	echo "look at /etc/zope/instances/main" >&2
	echo "Run then \"/etc/rc.d/init.d/zope start\" to start Zope." >&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/zope ]; then
		/etc/rc.d/init.d/zope stop
	fi
	/sbin/chkconfig --del zope
fi

%postun
if [ "$1" = "0" ] ; then
       echo "Removing user zope"
       /usr/sbin/userdel zope >/dev/null 2>&1 || :
       echo "Removing group zope"
       /usr/sbin/groupdel zope >/dev/null 2>&1 || :
fi

%files
%defattr(644,root,root,755)
%doc doc
%attr(754,root,root) /etc/rc.d/init.d/zope
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%{_libdir}/zope
%attr(640,root,root) %dir /var/lib/zope
%attr(1771,root,zope) %dir /var/lib/zope/main
%attr(640,root,root) %dir /etc/zope
%attr(640,root,root) %dir /etc/zope/instances
%attr(660,root,zope) %config(noreplace) %verify(not md5 size mtime) /var/lib/zope/main/*
%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) /etc/zope/instances/*
%attr(640,root,root) /etc/logrotate.d/zope
%attr(640,root,root) /etc/sysconfig/zope
%{_examplesdir}/*
%ghost /var/log/zope/main.log
%ghost /var/log/zope/main-detailed.log
