Summary:	An application server and portal toolkit for building Web sites
Summary(es):	Un servidor de aplicaciones y un conjunto de herramientas para la construcción de sitios Web
Summary(pl):	Serwer aplikacji i toolkit portalowy do tworzenia serwisów WWW
Summary(pt_BR):	Um servidor de aplicações e um conjunto de ferramentas para construção de sites Web
Name:		Zope
Version:	2.6.0
Release:	3
License:	Zope Public License (ZPL)
Group:		Networking/Daemons
Source0:	http://www.zope.org/Products/%{name}/%{version}/%{name}-%{version}-src.tgz
Source1:	http://www.zope.org/Documentation/Guides/ZCMG/ZCMG.html.tgz
Source2:	http://www.zope.org/Documentation/Guides/DTML/DTML.html.tgz
Source3:	http://www.zope.org/Documentation/Guides/ZSQL/ZSQL.html.tgz
Source4:	http://www.zope.org/Documentation/Guides/%{name}-ProductTutorial.tar.gz
Source5:	http://www.zope.org/Documentation/Guides/ZDG/ZDG.html.tgz
Source6:	http://www.zope.org/Documentation/Guides/ZAG/ZAG.html.tgz
# note: above documentation is deprecated, zope.org suggests using ZopeBook:
#Source1:	http://www.zope.org/Members/michel/ZB/ZopeBook.tgz
Source7:	%{name}.init
Source8:	%{name}-zserver.sh
URL:		http://www.zope.org/
Prereq:		rc-scripts
Prereq:		/sbin/chkconfig
Prereq:		/usr/sbin/useradd
Requires:	python >= 2.2
Requires:	python-modules >= 2.2
BuildRequires:	python-devel >= 2.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define python_prefix      %(echo `python -c "import sys; print sys.prefix"`)
%define python_version     %(echo `python -c "import sys; print sys.version[:3]"`)
%define python_libdir      %{python_prefix}/lib/python%{python_version}
%define python_includedir  %{python_prefix}/include/python%{python_version}
%define python_sitedir     %{python_libdir}/site-packages
%define python_configdir   %{python_libdir}/config

%define python_compile     python -c "import compileall; compileall.compile_dir('.')"
%define python_compile_opt python -O -c "import compileall; compileall.compile_dir('.')"

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
%setup -q -n %{name}-%{version}-src -a4
mkdir ZopeContentManagersGuide GuideToDTML GuideToZSQL ZopeDevelopersGuide ZopeAdminGuide
tar xzf %{SOURCE1} -C ZopeContentManagersGuide
tar xzf %{SOURCE2} -C GuideToDTML
tar xzf %{SOURCE3} -C GuideToZSQL
tar xzf %{SOURCE5} -C ZopeDevelopersGuide
tar xzf %{SOURCE6} -C ZopeAdminGuide

%build
perl -pi -e "s|data_dir\s+=\s+.*?join\(INSTANCE_HOME, 'var'\)|data_dir=INSTANCE_HOME|" lib/python/Globals.py
python wo_pcgi.py

find lib/python -type f -and \( -name 'Setup' -or -name '.cvsignore' \) -exec rm -f \{\} \;
find -type f -and \( -name '*.c' -or -name '*.h' -or -name 'Makefile*' \) -exec rm -f \{\} \;
rm -f ZServer/medusa/monitor_client_win32.py

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_libdir}/zope} \
	    $RPM_BUILD_ROOT{/etc/rc.d/init.d,/var/log,/var/lib/zope}

cp -a lib/python/* $RPM_BUILD_ROOT%{_libdir}/zope
cp -a ZServer/ utilities/ import/ $RPM_BUILD_ROOT%{_libdir}/zope
find $RPM_BUILD_ROOT%{_libdir}/zope -type f -name '*.py' -or -name '*.txt' | xargs -r rm -f
cp -a ZServer/medusa/test/* $RPM_BUILD_ROOT%{_libdir}/zope/ZServer/medusa/test/

install zpasswd.py $RPM_BUILD_ROOT%{_bindir}/zpasswd
install z2.py $RPM_BUILD_ROOT%{_libdir}/zope
install %{SOURCE8} $RPM_BUILD_ROOT%{_sbindir}/zope-zserver
install %{SOURCE7} $RPM_BUILD_ROOT/etc/rc.d/init.d/zope
install var/Data.fs $RPM_BUILD_ROOT/var/lib/zope/Data.fs

touch $RPM_BUILD_ROOT/var/log/zope

python $RPM_BUILD_ROOT%{_bindir}/zpasswd -u zope -p zope -d localhost $RPM_BUILD_ROOT/var/lib/zope/access

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
if [ -f /var/lock/subsys/zope ]; then
	/etc/rc.d/init.d/zope restart >&2
else
	echo "Run \"/etc/rc.d/init.d/zope start\" to start Zope." >&2
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
%attr(755,root,root) /etc/rc.d/init.d/zope
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%{_libdir}/zope
%attr(1771,root,zope) %dir /var/lib/zope
%attr(660,root,zope) %config(noreplace) %verify(not md5 size mtime) /var/lib/zope/*
%doc *.txt doc/*.txt ZopeContentManagersGuide GuideToZSQL Tutorial ZopeDevelopersGuide ZopeAdminGuide
