Summary:	Cross S/390 GNU binary utility development utilities - gcc
Summary(es):	Utilitarios para desarrollo de binarios de la GNU - S/390 gcc
Summary(fr):	Utilitaires de développement binaire de GNU - S/390 gcc
Summary(pl):	Skro¶ne narzêdzia programistyczne GNU dla S/390 - gcc
Summary(pt_BR):	Utilitários para desenvolvimento de binários da GNU - S/390 gcc
Summary(tr):	GNU geliþtirme araçlarý - S/390 gcc
Name:		crosss390x-gcc
Version:	4.0.2
Release:	1
Epoch:		1
License:	GPL
Group:		Development/Languages
Source0:	ftp://gcc.gnu.org/pub/gcc/releases/gcc-%{version}/gcc-%{version}.tar.bz2
# Source0-md5:	a659b8388cac9db2b13e056e574ceeb0
URL:		http://gcc.gnu.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	crosss390x-binutils
BuildRequires:	fileutils >= 4.1.41
BuildRequires:	flex
BuildRequires:	rpmbuild(macros) >= 1.211
BuildRequires:	texinfo >= 4.1
Requires:	crosss390x-binutils
Requires:	gcc-dirs
ExcludeArch:	s390x
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		target		s390x-pld-linux
%define		arch		%{_prefix}/%{target}
%define		gccarch		%{_libdir}/gcc/%{target}
%define		gcclib		%{gccarch}/%{version}

%define		_noautostrip	.*/libgc.*\\.a

%description
This package contains a cross-gcc which allows the creation of
binaries to be run on S/390 Linux on other machines.

%description -l de
Dieses Paket enthält einen Cross-gcc, der es erlaubt, auf einem
anderem Rechner Code für S/390 Linux zu generieren.

%description -l pl
Ten pakiet zawiera skro¶ny gcc pozwalaj±cy na robienie na innych
maszynach binariów do uruchamiania na Linuksie S/390.

%package c++
Summary:	C++ support for crosss390x-gcc
Summary(pl):	Obs³uga C++ dla crosss390x-gcc
Group:		Development/Languages
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description c++
This package adds C++ support to the GNU Compiler Collection for
S/390.

%description c++ -l pl
Ten pakiet dodaje obs³ugê C++ do kompilatora gcc dla S/390.

%prep
%setup -q -n gcc-%{version}

%build
cp -f /usr/share/automake/config.* .
rm -rf obj-%{target}
install -d obj-%{target}
cd obj-%{target}

CFLAGS="%{rpmcflags}" \
CXXFLAGS="%{rpmcflags}" \
TEXCONFIG=false \
../configure \
	--prefix=%{_prefix} \
	--infodir=%{_infodir} \
	--mandir=%{_mandir} \
	--bindir=%{_bindir} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libdir} \
	--disable-shared \
	--disable-threads \
	--enable-languages="c,c++" \
	--enable-c99 \
	--enable-long-long \
	--disable-nls \
	--with-gnu-as \
	--with-gnu-ld \
	--with-mangler-in-ld \
	--with-system-zlib \
	--enable-multilib \
	--without-headers \
	--without-x \
	--target=%{target} \
	--host=%{_target_platform} \
	--build=%{_target_platform}

%{__make} all-gcc

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C obj-%{target} install-gcc \
	DESTDIR=$RPM_BUILD_ROOT

install obj-%{target}/gcc/specs $RPM_BUILD_ROOT%{gcclib}

# don't want this here
rm -f $RPM_BUILD_ROOT%{_libdir}/libiberty.a

# include/ contains install-tools/include/* and headers that were fixed up
# by fixincludes, we don't want former
gccdir=$RPM_BUILD_ROOT%{gcclib}
mkdir	$gccdir/tmp
# we have to save these however
mv -f	$gccdir/include/syslimits.h $gccdir/tmp
rm -rf	$gccdir/include
mv -f	$gccdir/tmp $gccdir/include
cp -f	$gccdir/install-tools/include/*.h $gccdir/include
# but we don't want anything more from install-tools
rm -rf	$gccdir/install-tools

%if 0%{!?debug:1}
%{target}-strip -g -R.note -R.comment $RPM_BUILD_ROOT%{gcclib}/32/libgcc.a
%{target}-strip -g -R.note -R.comment $RPM_BUILD_ROOT%{gcclib}/32/libgcov.a
%{target}-strip -g -R.note -R.comment $RPM_BUILD_ROOT%{gcclib}/libgcc.a
%{target}-strip -g -R.note -R.comment $RPM_BUILD_ROOT%{gcclib}/libgcov.a
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{target}-cpp
%attr(755,root,root) %{_bindir}/%{target}-gcc
%dir %{gccarch}
%dir %{gcclib}
%attr(755,root,root) %{gcclib}/cc1
%attr(755,root,root) %{gcclib}/collect2
%dir %{gcclib}/32
%{gcclib}/32/crt*.o
%{gcclib}/32/libgcc.a
%{gcclib}/crt*.o
%{gcclib}/libgcc.a
%{gcclib}/specs*
%dir %{gcclib}/include
%{gcclib}/include/*.h
%{_mandir}/man1/%{target}-cpp.1*
%{_mandir}/man1/%{target}-gcc.1*

%files c++
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{target}-g++
%attr(755,root,root) %{gcclib}/cc1plus
%{_mandir}/man1/%{target}-g++.1*
