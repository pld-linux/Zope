Summary:	An application server and portal toolkit for building Web sites
Summary(es):	Un servidor de aplicaciones y un conjunto de herramientas para la construcción de sitios Web
Summary(pl):	Serwer aplikacji i toolkit portalowy do tworzenia serwisów WWW
Summary(pt_BR):	Um servidor de aplicações e um conjunto de ferramentas para construção de sites Web
Name:		Zope
Version:	2.6.3
Release:	1
License:	Zope Public License (ZPL)
Group:		Networking/Daemons
Source0:	http://www.zope.org/Products/%{name}/%{version}/%{version}/%{name}-%{version}-src.tgz
# Source0-md5:	904cf97757401fd353275d0807685460
Source1:	%{name}.init
Source2:	%{name}.logrotate
Source3:	%{name}.sysconfig
Source4:	%{name}-zserver.sh
Source5:	%{name}.instance
Source6:	%{name}-mkzopeinstance
Source7:	%{name}-installzopeproduct
Source8:	http://zope.org/Documentation/Guides/ZCMG/Tarred%20HTML%202.1.1/ZCMG.html.tgz
# Source8-md5:	4c52eebc2e874a0590ac9c04e222e9f1
Source9:	http://www.zope.org/Documentation/Guides/DTML/Compressed%20html%202.1.1/DTML.html.tgz
# Source9-md5:	10f363dd061a1af8d472c51c32fa0a0e
Source10:	http://www.zope.org/Documentation/Guides/ZSQL/2.1.1/ZSQL.html.tgz
# Source10-md5:	0cddb5688fc0f886db468da08251fb81
Source11:	http://www.zope.org/Documentation/Guides/ZDG/HTML%201.2/ZDG.html.tgz
# Source11-md5:	0344ca88acb8a71688d2925975a55443
Source12:	http://www.zope.org/Documentation/Guides/ZAG/HTML%201.0/ZAG.html.tgz
# Source12-md5:	b28bfc4ba4bee880767fcf89d79532d2
Source13:	http://openbsd.secsup.org/distfiles/zopebook-2.5/ZopeBook.tgz
# Source13-md5:	268c38a4c7d9f7334cdc98b0a152f8da
URL:		http://www.zope.org/
BuildRequires:	python-devel >= 2.1
BuildRequires:	perl-base
PreReq:		rc-scripts
Requires(pre): /usr/bin/getgid
Requires(pre): /bin/id
Requires(pre): /usr/sbin/groupadd
Requires(pre): /usr/sbin/useradd
Requires(postun):      /usr/sbin/userdel
Requires(postun):      /usr/sbin/groupdel
Requires(post,preun):	/sbin/chkconfig
Requires:	logrotate
Requires:	python >= 2.2
Requires:	python-modules >= 2.2
Requires:	python-libs >= 2.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		python_prefix		%(echo `python -c "import sys; print sys.prefix"`)
%define		python_version		%(echo `python -c "import sys; print sys.version[:3]"`)
%define		python_libdir		%{python_prefix}/lib/python%{python_version}
%define		python_includedir	%{python_prefix}/include/python%{python_version}
%define		python_sitedir		%{python_libdir}/site-packages
%define		python_configdir	%{python_libdir}/config

%define		python_compile		python -c "import compileall; compileall.compile_dir('.')"
%define		python_compile_opt	python -O -c "import compileall; compileall.compile_dir('.')"

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
%setup -q -n %{name}-%{version}-src
mkdir ZopeContentManagersGuide GuideToDTML GuideToZSQL ZopeDevelopersGuide ZopeAdminGuide
mkdir ZopeBook
tar xzf %{SOURCE8} -C ZopeContentManagersGuide
tar xzf %{SOURCE9} -C GuideToDTML
tar xzf %{SOURCE10} -C GuideToZSQL
tar xzf %{SOURCE11} -C ZopeDevelopersGuide
tar xzf %{SOURCE12} -C ZopeAdminGuide
tar xzf %{SOURCE13} -C ZopeBook

%build
python wo_pcgi.py

find . -type f -and \( -name 'Setup' -or -name '.cvsignore' \) -exec rm -f \{\} \;
find -type f -and \( -name '*.c' -or -name '*.h' -or -name 'Makefile*' \) -exec rm -f \{\} \;
rm -f ZServer/medusa/monitor_client_win32.py

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_libdir}/zope} \
	$RPM_BUILD_ROOT%{_sysconfdir}/zope/{skel/{Products,etc},main} \
	$RPM_BUILD_ROOT{/etc/rc.d/init.d,/etc/logrotate.d,/etc/sysconfig} \
	$RPM_BUILD_ROOT{/var/log/zope/main,/var/lib/zope/main}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/zope
install %{SOURCE2} $RPM_BUILD_ROOT/etc/logrotate.d/zope
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/zope
install %{SOURCE4} $RPM_BUILD_ROOT%{_sbindir}/zope-zserver
install %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/zope/skel/etc/instance
install %{SOURCE6} $RPM_BUILD_ROOT%{_sbindir}/mkzopeinstance
install %{SOURCE7} $RPM_BUILD_ROOT%{_sbindir}/installzopeproduct

cp -a lib/python/* $RPM_BUILD_ROOT%{_libdir}/zope
cp -a ZServer/ utilities/ $RPM_BUILD_ROOT%{_libdir}/zope
cp -a import/ Extensions/ var/ $RPM_BUILD_ROOT%{_sysconfdir}/zope/skel
find $RPM_BUILD_ROOT%{_libdir}/zope -type f -name '*.py' | xargs -r rm -f
cp -a ZServer/medusa/test/* $RPM_BUILD_ROOT%{_libdir}/zope/ZServer/medusa/test/

install zpasswd.py $RPM_BUILD_ROOT%{_bindir}/zpasswd
install z2.py $RPM_BUILD_ROOT%{_libdir}/zope

touch $RPM_BUILD_ROOT/var/log/zope/main/zope.log
touch $RPM_BUILD_ROOT/var/log/zope/main/zope-startup.log

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ -z "`getgid zope`" ]; then
       echo "Making group zope"
       /usr/sbin/groupadd -r -f zope
fi
if [ -z "`id -u zope 2>/dev/null`" ]; then
       echo "Making user zope"
       /usr/sbin/useradd -r -d /var/lib/zope -s /bin/false -c "Zope User" -g zope zope
fi

%post
/sbin/chkconfig --add zope
if [ ! -f /etc/zope/main/instance ] ; then
	echo "Creating initial 'main' instance..."
	/usr/sbin/mkzopeinstance main
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
	echo "look at /etc/zope/main/instance" >&2
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
%doc doc/*.txt *.txt ZopeContentManagersGuide GuideToZSQL ZopeDevelopersGuide ZopeAdminGuide ZopeBook
%attr(755,root,root) /etc/rc.d/init.d/zope
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%{_libdir}/zope
%attr(751,root,root) %dir /var/lib/zope
%attr(1771,root,zope) %dir /var/lib/zope/main
%attr(771,root,root) %dir /var/log/zope
%attr(771,root,zope) %dir /var/log/zope/main
%attr(640,root,root) %dir /etc/zope
%attr(640,root,root) %dir /etc/zope/skel
%attr(640,root,root) %dir /etc/zope/main
%config(noreplace) %verify(not md5 size mtime) /etc/zope/skel/*
%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) /etc/logrotate.d/zope
%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) /etc/sysconfig/zope
%ghost /var/log/zope/main/*.log
