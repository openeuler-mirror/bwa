Name:                bwa
Version:             0.7.17
Release:             2
Summary:             Burrows-Wheeler Alignment tool
License:             GPLv3 and MIT
URL:                 https://github.com/lh3/bwa
Source0:             https://github.com/lh3/bwa/releases/download/v%{version}/%{name}-%{version}.tar.bz2
Patch0:              bwa-fix-build-gcc10.patch
Patch1:              bwa-simde.patch
Patch2:              support-specify-cc.patch
BuildRequires:       gcc perl-generators
BuildRequires:       clang
%ifnarch x86_64
BuildRequires:       simde-devel
%endif
BuildRequires:       zlib-devel

%description
BWA is a program for aligning sequencing reads against a large
reference genome (e.g. human genome). It has two major components, one
for read shorter than 150bp and the other for longer reads.

%prep
%autosetup -p1

%build
CFLAGS="%{optflags} -O3"
%ifnarch x86_64
CFLAGS="${CFLAGS} -DUSE_SIMDE -DSIMDE_ENABLE_NATIVE_ALIASES -fopenmp-simd -DSIMDE_ENABLE_OPENMP"
%endif
%make_build CFLAGS="${CFLAGS}"

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_datadir}/%{name}/bwakit
mkdir -p %{buildroot}/%{_mandir}/man1
install -m 0755 bwa %{buildroot}/%{_bindir}
install -m 0755 qualfa2fq.pl %{buildroot}/%{_bindir}
install -m 0755 xa2multi.pl %{buildroot}/%{_bindir}
install -m 0755 bwakit/* %{buildroot}/%{_datadir}/%{name}/bwakit
install -m 0644 bwa.1 %{buildroot}/%{_mandir}/man1/bwa.1

%check
./bwa 2>&1 | grep '^Version: %{version}'

%files
%doc COPYING NEWS.md README.md README-alt.md
%{_bindir}/bwa
%{_bindir}/qualfa2fq.pl
%{_bindir}/xa2multi.pl
%{_datadir}/%{name}/*
%{_mandir}/man1/%{name}.1*

%changelog
* Fri Apr 14 2023 jammyjellyfish <jammyjellyfish255@outlook.com> - 0.7.17-2
- Support specify CC

* Fri Jan 8 2021 chengzihan <chengzihan2@huawei.com> - 0.7.17-1
- Package init
