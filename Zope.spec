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
Source1:	%{name}.init
Source2:	%{name}.logrotate
Source3:	%{name}-zserver.sh
Source4:	http://www.zope.org/Documentation/Guides/ZCMG/ZCMG.html.tgz
Source5:	http://www.zope.org/Documentation/Guides/DTML/DTML.html.tgz
Source6:	http://www.zope.org/Documentation/Guides/ZSQL/ZSQL.html.tgz
Source7:	http://www.zope.org/Documentation/Guides/%{name}-ProductTutorial.tar.gz
Source8:	http://www.zope.org/Documentation/Guides/ZDG/ZDG.html.tgz
Source9:	http://www.zope.org/Documentation/Guides/ZAG/ZAG.html.tgz
Source10:	http://www.zope.org/Documentation/Books/ZopeBook/current/ZopeBook.tgz
URL:		http://www.zope.org/
BuildRequires:	python-devel >= 2.2
PreReq:		rc-scripts
Requires(pre):	user-zope
Requires(post,preun):	/sbin/chkconfig
Requires:	logrotate
Requires:	python-modules >= 2.2
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
tar xzf %{SOURCE7} -C ZopeDevelopersGuide
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
	$RPM_BUILD_ROOT{/etc/{rc.d/init.d,logrotate},/var/log,/var/lib/zope}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/zope
install %{SOURCE2} $RPM_BUILD_ROOT/etc/logrotate/zope
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

%files
%defattr(644,root,root,755)
%doc doc/*.txt *.txt ZopeContentManagersGuide GuideToZSQL Tutorial ZopeDevelopersGuide ZopeAdminGuide ZopeBook
%attr(755,root,root) /etc/rc.d/init.d/zope
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%{_libdir}/zope
%attr(1771,root,zope) %dir /var/lib/zope
%attr(660,root,zope) %config(noreplace) %verify(not md5 size mtime) /var/lib/zope/*
%ghost /var/log/zope
