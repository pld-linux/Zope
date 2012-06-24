Summary:	An application server and portal toolkit for building Web sites
Summary(es):	Un servidor de aplicaciones y un conjunto de herramientas para la construcci�n de sitios Web
Summary(pl):	Serwer aplikacji i toolkit portalowy do tworzenia serwis�w WWW
Summary(pt_BR):	Um servidor de aplica��es e um conjunto de ferramentas para constru��o de sites Web
Name:		Zope
Version:	2.6.1
Release:	1
License:	Zope Public License (ZPL)
Group:		Networking/Daemons
Source0:	http://www.zope.org/Products/%{name}/%{version}/%{name}-%{version}-src.tgz
# Source0-md5:	a17f36b86b6e489797d8e52f1ba48efe
Source1:	%{name}.init
Source2:	%{name}.logrotate
Source3:	%{name}-zserver.sh
Source4:	http://www.zope.org/Documentation/Guides/ZCMG/ZCMG.html.tgz
# Source4-md5:	4c52eebc2e874a0590ac9c04e222e9f1
Source5:	http://www.zope.org/Documentation/Guides/DTML/DTML.html.tgz
# Source5-md5:	10f363dd061a1af8d472c51c32fa0a0e
Source6:	http://www.zope.org/Documentation/Guides/ZSQL/ZSQL.html.tgz
# Source6-md5:	0cddb5688fc0f886db468da08251fb81
Source8:	http://www.zope.org/Documentation/Guides/ZDG/ZDG.html.tgz
# Source8-md5:	0344ca88acb8a71688d2925975a55443
Source9:	http://www.zope.org/Documentation/Guides/ZAG/ZAG.html.tgz
# Source9-md5:	b28bfc4ba4bee880767fcf89d79532d2
Source10:	http://www.zope.org/Documentation/Books/ZopeBook/current/ZopeBook.tgz
# Source10-md5:	268c38a4c7d9f7334cdc98b0a152f8da
URL:		http://www.zope.org/
BuildRequires:	python-devel >= 2.2
BuildRequires:	perl
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
%setup -q -n %{name}-%{version}-src -a4
mkdir ZopeContentManagersGuide GuideToDTML GuideToZSQL ZopeDevelopersGuide ZopeAdminGuide
mkdir ZopeBook
tar xzf %{SOURCE4} -C ZopeContentManagersGuide
tar xzf %{SOURCE5} -C GuideToDTML
tar xzf %{SOURCE6} -C GuideToZSQL
tar xzf %{SOURCE8} -C ZopeAdminGuide
tar xzf %{SOURCE9} -C ZopeBook

%build
perl -pi -e "s|data_dir\s+=\s+.*?join\(INSTANCE_HOME, 'var'\)|data_dir=INSTANCE_HOME|" lib/python/Globals.py
python wo_pcgi.py

find lib/python -type f -and \( -name 'Setup' -or -name '.cvsignore' \) -exec rm -f \{\} \;
find -type f -and \( -name '*.c' -or -name '*.h' -or -name 'Makefile*' \) -exec rm -f \{\} \;
rm -f ZServer/medusa/monitor_client_win32.py

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_libdir}/zope} \
	$RPM_BUILD_ROOT{/etc/{rc.d/init.d,logrotate.d},/var/log,/var/lib/zope}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/zope
install %{SOURCE2} $RPM_BUILD_ROOT/etc/logrotate.d/zope
install %{SOURCE3} $RPM_BUILD_ROOT%{_sbindir}/zope-zserver

cp -a lib/python/* $RPM_BUILD_ROOT%{_libdir}/zope
cp -a ZServer/ utilities/ import/ $RPM_BUILD_ROOT%{_libdir}/zope
find $RPM_BUILD_ROOT%{_libdir}/zope -type f -name '*.py' -or -name '*.txt' | xargs -r rm -f
cp -a ZServer/medusa/test/* $RPM_BUILD_ROOT%{_libdir}/zope/ZServer/medusa/test/

install zpasswd.py $RPM_BUILD_ROOT%{_bindir}/zpasswd
install z2.py $RPM_BUILD_ROOT%{_libdir}/zope
install var/Data.fs $RPM_BUILD_ROOT/var/lib/zope/Data.fs

python $RPM_BUILD_ROOT%{_bindir}/zpasswd -u zope -p zope -d localhost \
	$RPM_BUILD_ROOT/var/lib/zope/access

touch $RPM_BUILD_ROOT/var/log/zope

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
	echo "Create inituser using \"zpasswd inituser\" in directory \"/var/lib/zope\"" >&2
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
%doc doc/*.txt *.txt ZopeContentManagersGuide GuideToZSQL ZopeDevelopersGuide ZopeAdminGuide ZopeBook
%attr(755,root,root) /etc/rc.d/init.d/zope
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%{_libdir}/zope
%attr(1771,root,zope) %dir /var/lib/zope
%attr(660,root,zope) %config(noreplace) %verify(not md5 size mtime) /var/lib/zope/*
%attr(640,root,root) /etc/logrotate.d/zope
# ghost /var/log/zope
%attr(640,root,root) /var/log/zope
