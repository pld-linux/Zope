%include        /usr/lib/rpm/macros.python

# TODO:
# - no/more secure initial user/password settings (currently: zope/zope)
# - ZEO support (mkzeoinstance is not tested and probably doesn't work)
# - perl support?

Summary:	An application server and portal toolkit for building Web sites
Summary(es):	Un servidor de aplicaciones y un conjunto de herramientas para la construcción de sitios Web
Summary(pl):	Serwer aplikacji i toolkit portalowy do tworzenia serwisów WWW
Summary(pt_BR):	Um servidor de aplicações e um conjunto de ferramentas para construção de sites Web
Name:		Zope
Version:	2.7.0
%define		sub_ver b4
Release:	3.%{sub_ver}.1
License:	Zope Public License (ZPL)
Group:		Networking/Daemons
Source0:	http://www.zope.org/Products/%{name}/%{version}%{sub_ver}/%{version}%{sub_ver}/%{name}-%{version}-%{sub_ver}.tgz
# Source0-md5:	97f5ec08f943de8e933936c05368af0d
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.logrotate
Source4:	%{name}-mkzopeinstance
Source5:	%{name}-mkzeoinstance
Source6:	%{name}-runzope
Source7:	%{name}-zopectl
Source8:	%{name}-installzopeproduct
Patch0:		%{name}-default_config.patch
Patch1:		%{name}-instance_paths.patch
Patch2:		%{name}-pld_makefile_fix.patch
URL:		http://www.zope.org/
BuildRequires:	python-devel >= 2.3.3
BuildRequires:	perl-base
PreReq:		rc-scripts
Requires(pre):	/usr/bin/getgid
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(postun):	/usr/sbin/userdel
Requires(postun):	/usr/sbin/groupdel
Requires(post,preun):	/sbin/chkconfig
Requires:	logrotate
Requires:	python >= 2.3.3
Requires:	python-modules >= 2.3.3
Requires:	python-libs >= 2.3.3
Requires:	expat >= 1.95.7
Requires:	python-PyXML >= 0.8.3
%pyrequires_eq  python
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		zope_dir /usr/lib/zope

%description
The Z Object Programming Environment (Zope) is a free, Open Source
Python-based application server for building high-performance, dynamic
web sites, using a powerful and simple scripting object model and
high-performance, integrated object database.

%description -l es
Zope es una aplicación basada en Python, Open Source[tm], para la
construcción de sitios dinámicos, usa un modelo de escritura de
guiones poderoso y sencillo. Para instalar la aplicación Zope, instale
ese paquete y después, Zope-server, para un servidor HTTP integrado
simple, Zope-pcgi, para uso con el servidor Apache. Si desea instalar
solamente algunas partes de la aplicación Zope, están diponibles otros
subpaquetes, usted debe instalar éstos en vez de ese RPM.

%description -l pl
Zope (Z Object Programming Environment - Obiektowe ¦rodowisko
Programistyczne Z) jest opartym o Pythona serwerem aplikacji do
tworzenia wysoko wydajnych, dynamicznych serwisów WWW, przy u¿yciu
u¿ytecznego i prostego modelu obiektowego skryptów oraz wysoko
wydajnej zintegrowanej obiektowej bazy danych.

%description -l pt_BR
Zope é uma aplicação baseada em Python, Open Source[tm], para
construção de sites dinâmicos, usando um modelo de scripting poderoso
e simples Para instalar o Zope, instale esse pacote e depois, ou o
Zope-server, para um servidor HTTP integrado simples, ou Zope-pcgi,
para uso com o Apache. Se você quiser instalar apenas algumas partes
do Zope, outros sub-pacotes estão disponíveis, e você deveria instalar
eles ao invés desse RPM.

%prep

%setup -q -n %{name}-%{version}-%{sub_ver}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
perl -pi -e "s|data_dir\s+=\s+.*?join\(INSTANCE_HOME, 'var'\)|data_dir=INSTANCE_HOME|" lib/python/Globals.py

./configure \
	--prefix=%{zope_dir}
#	--with-python=/usr/bin/python

%{__make}

perl -pi -e "s|data_dir\s+=\s+.*?join\(INSTANCE_HOME, 'var'\)|data_dir=INSTANCE_HOME|" lib/python/Globals.py
# python wo_pcgi.py

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{/var/lib/zope/main,/var/run/zope,/var/log/zope/main} \
	$RPM_BUILD_ROOT{/etc/logrotate.d,/etc/sysconfig,/etc/rc.d/init.d} \
	$RPM_BUILD_ROOT{%{_sysconfdir}/zope/main,%{_sbindir}} \
	$RPM_BUILD_ROOT%{zope_dir}/bin

ln -sfn /usr/bin/python $RPM_BUILD_ROOT%{zope_dir}/bin/python

%{__make} install \
	INSTALL_FLAGS="--root $RPM_BUILD_ROOT"

mv $RPM_BUILD_ROOT%{zope_dir}/bin/zpasswd.py $RPM_BUILD_ROOT%{_sbindir}/zpasswd
mv $RPM_BUILD_ROOT%{zope_dir}/skel $RPM_BUILD_ROOT%{_sysconfdir}/zope
mv $RPM_BUILD_ROOT{%{zope_dir}/import/*,%{_sysconfdir}/zope/skel/import}

rm -rf $RPM_BUILD_ROOT%{zope_dir}/doc
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/zope/skel/log
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/zope/skel/bin/{runzope.bat,zopeservice.py}.in

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/zope
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/zope
install %{SOURCE3} $RPM_BUILD_ROOT/etc/logrotate.d/zope
install %{SOURCE4} $RPM_BUILD_ROOT%{_sbindir}/mkzopeinstance
install %{SOURCE5} $RPM_BUILD_ROOT%{_sbindir}/mkzeoinstance
install %{SOURCE6} $RPM_BUILD_ROOT%{_sbindir}/runzope
install %{SOURCE7} $RPM_BUILD_ROOT%{_sbindir}/zopectl
install %{SOURCE8} $RPM_BUILD_ROOT%{_sbindir}/installzopeproduct

touch $RPM_BUILD_ROOT/var/log/zope/main/event.log
touch $RPM_BUILD_ROOT/var/log/zope/main/Z2.log

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
if [ ! -f /etc/zope/main/zope.conf ] ; then
	echo "Creating initial 'main' instance..."
	/usr/sbin/mkzopeinstance main zope:zope
	echo "Instance created. Listening on 127.0.0.1:8080, initial user: 'zope' with password: 'zope'"
else
	echo "old /etc/zope/zope.conf detected - look at changes about upgrade!" >&2
fi
was_stopped=0
for dir in /var/lib/zope/main /var/lib/zope ; do
	if [ -f $dir/Data.fs ]; then
		echo "Found the database in old location. Migrating..."
		if [ -f /var/lock/subsys/zope ]; then
		    /etc/rc.d/init.d/zope stop >&2
		    was_stopped=1
		fi
		umask 022
		[ -d /var/lib/zope/main ] && cd $dir && mv -f Data* /var/lib/zope/main/var 2>/dev/null
		if [ "x$was_stopped" = "x1" ]; then
		    /etc/rc.d/init.d/zope start >&2
		fi
		echo "Migration completed (new db location is /var/lib/zope/main/var)"
		break
	fi
done
if [ -f /var/lock/subsys/zope ]; then
	if [ "x$was_stopped" != "x1" ]; then
	    /etc/rc.d/init.d/zope restart >&2
	fi
else
	echo "look at /etc/zope/main/zope.conf" >&2
	echo "Run then \"/etc/rc.d/init.d/zope start\" to start Zope." >&2
	echo "you may create new Zope instances with mkzopeinstance" >&2
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
%doc doc/*
%attr(754,root,root) /etc/rc.d/init.d/zope
%attr(755,root,root) %{_sbindir}/*
%{zope_dir}
%attr(775,zope,zope) %dir /var/run/zope
%attr(775,zope,zope) %dir /var/lib/zope
%attr(775,zope,zope) %dir /var/lib/zope/main
%attr(775,zope,zope) %dir /var/log/zope
%attr(775,zope,zope) %dir /var/log/zope/main
%attr(640,root,root) %dir /etc/zope
%attr(640,root,root) %dir /etc/zope/skel
%attr(640,root,root) %dir /etc/zope/main
%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) /etc/zope/skel/*
%attr(640,root,root) /etc/logrotate.d/zope
%attr(640,root,root) /etc/sysconfig/zope
%ghost /var/log/zope/main/event.log
%ghost /var/log/zope/main/Z2.log
