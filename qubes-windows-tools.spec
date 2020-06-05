Name:		qubes-windows-tools
Version:	4.1
Release:	1
Summary:	Qubes Tools for Windows VMs
Group:		Qubes
License:	GPL
Obsoletes:	qubes-core-dom0-pvdrivers
BuildRequires:	genisoimage
BuildRequires:	mingw64-gcc
BuildRequires:	mingw64-winpthreads-static
BuildRequires:	mingw64-gcc-c++
BuildRequires:	wine
BuildRequires:	svn
BuildArch:	noarch
# Retrieve devcon tool from windows samples
# svn export https://github.com/microsoft/Windows-driver-samples/trunk/setup/devcon | tar -czvf devcon.tar.gz devcon
Source0:	devcon.tar.gz
# Get the latest qwt source tree
Source1:	https://github.com/QubesOS/qubes-core-vchan-xen/archive/mm_f40b71ac.zip#/qubes-core-vchan-xen-mm_f40b71ac.zip
Source2:	https://github.com/QubesOS/qubes-core-agent-windows/archive/mm_a2aea339.zip#/qubes-core-agent-windows-mm_a2aea339.zip
Source3:	https://github.com/QubesOS/qubes-windows-utils/archive/v4.0.0.zip#/qubes-windows-utils-4.0.0.zip
Source4:	https://github.com/QubesOS/qubes-core-qubesdb/archive/v4.1.3.zip#/qubes-core-qubesdb-4.1.3.zip
Source5:	https://github.com/QubesOS/qubes-gui-common/archive/mm_f943945a.zip#/qubes-gui-common-mm_f943945a.zip
Source6:	https://github.com/QubesOS/qubes-gui-agent-windows/archive/v4.0.0.zip#/qubes-gui-agent-windows-4.0.0.zip
Source7:	https://github.com/QubesOS/qubes-installer-qubes-os-windows-tools/archive/v4.0.1-3.zip#/qubes-installer-qubes-os-windows-tools-4.0.1-3.zip
Source8:	https://github.com/QubesOS/qubes-vmm-xen-windows-pvdrivers/archive/v4.0.0.zip#/qubes-vmm-xen-windows-pvdrivers-4.0.0.zip
Source9:	https://github.com/QubesOS/qubes-vmm-xen-win-pvdrivers-xeniface/archive/mm_ff24d3b2.zip#/qubes-vmm-xen-win-pvdrivers-xeniface-mm_ff24d3b2.zip

Source10: 	https://raw.githubusercontent.com/llvm-mirror/compiler-rt/master/lib/builtins/assembly.h

# Add local sources
Source16:	preparation.bat
Source17:	pkihelper.c
Source18:	qubes-tools-combined.wxs
Source19:	diskpart.ps1
Source20:	qnetwork_setup.bat
Source100:	Makefile

# Download the latest stable xen binary drivers
Source21:	http://xenbits.xen.org/pvdrivers/win/8.2.2/xenbus.tar
Source22:	http://xenbits.xen.org/pvdrivers/win/8.2.2/xeniface.tar
Source23:	http://xenbits.xen.org/pvdrivers/win/8.2.2/xenvif.tar
Source24:	http://xenbits.xen.org/pvdrivers/win/8.2.2/xennet.tar
Source25:	http://xenbits.xen.org/pvdrivers/win/8.2.2/xenvbd.tar

Patch0:         devcon-headers.patch

# stalled
Patch1:		qubes-core-vchan-xen-mingw-fragments.patch
Patch2:		qubes-core-agent-windows-mingw-fragments.patch
Patch3:		qubes-windows-utils-mingw-fragments.patch
Patch4:		qubes-core-qubesdb-mingw-fragments.patch
Patch5:		qubes-gui-agent-windows-mingw-fragments.patch
Patch6:		qubes-installer-qubes-os-windows-tools-mingw-fragments.patch
Patch7:		qubes-vmm-xen-windows-pvdrivers-mingw-fragments.patch
Patch8:		qubes-vmm-xen-win-pvdrivers-xeniface-mingw.patch

Patch11:	qubes-core-agent-windows-warn-incompat-proto.patch
Patch12:	qubesdb-daemon-win32-fix.patch

Patch13:	qubes-gui-agent-windows-destroy.patch

# remove CreateEvent from event processing loop
Patch40:        qwt-gui-agent-cpu-usage.patch
# build with inlined __chkstk_ms
Patch41:	qwt-chkstk.patch

#fix wrong relative path when qrexec called with "QUBESRPC qubes.Filecopy+"
Patch42:	qrexec-store-separator-to-fix-relative-path-construct.patch

%prep
%setup -c
for i in $(ls %{_sourcedir}/qubes*.zip);
do unzip $i; done;
cat %{_sourcedir}/xen*.tar | tar -xvf - -i
cp -f %{S:100} ./
cp -f %{S:18} ./
mkdir -p qubes-gui-agent-windows-4.0.0/install-helper/pkihelper/
cp -f %{S:17} qubes-gui-agent-windows-4.0.0/install-helper/pkihelper/
mkdir -p include

cp -f %{S:10} include

patch -d qubes-core-vchan-xen-* -p1 < %{P:1}
patch -d qubes-core-agent-windows-* -p1 < %{P:2}
patch -d qubes-windows-utils-* -p1 < %{P:3}
patch -d qubes-core-qubesdb-* -p1 < %{P:4}
patch -d qubes-gui-agent-windows-* -p1 < %{P:5}
patch -d qubes-installer-qubes-os-windows-tools-* -p1 < %{P:6}
patch -d qubes-vmm-xen-windows-pvdrivers-* -p1 < %{P:7}
patch -d qubes-vmm-xen-win-pvdrivers-xeniface-* -p1 < %{P:8}
patch -d qubes-gui-agent-windows-* -p1 < %{P:13}

%patch0 -p1
%patch11 -p0
%patch12 -p0
%patch40 -p1
%patch41 -p1
%patch42 -p1

%description
PV Drivers and Qubes Tools for Windows AppVMs.

%build

make all

export WINEMU=wine; export WINEPREFIX=/opt/wine; export WINEARCH=win32
export WINEDEBUG=fixme-all; export WIXPATH=/opt/wix; 
export DDK_ARCH=x64
export WIN_BUILD_TYPE=chk; export VERSION=4.0.0.0;
export QUBES_BIN=bin/${DDK_ARCH}
cp -f %{S:19} %{S:20} %{S:16} bin/${DDK_ARCH}
${WINEMU} ${WIXPATH}/candle.exe -arch ${DDK_ARCH} -ext WixDifxAppExtension -ext WixIIsExtension *.wxs;
${WINEMU} ${WIXPATH}/light.exe -sval *.wixobj -ext WixDifxAppExtension -ext WixUIExtension -ext WixIIsExtension -ext WixUtilExtension "Z:/opt/wix/difxapp_${DDK_ARCH}.wixlib" -o qubes-tools-${DDK_ARCH}.msi
mkdir -p iso-content
cp qubes-tools-${DDK_ARCH}.msi iso-content/
genisoimage -o qubes-windows-tools-%{version}.%{release}.iso -m .gitignore -JR iso-content

%install
mkdir -p $RPM_BUILD_ROOT/usr/lib/qubes/
cp qubes-windows-tools-%{version}.%{release}.iso $RPM_BUILD_ROOT/usr/lib/qubes/
ln -s qubes-windows-tools-%{version}.%{release}.iso $RPM_BUILD_ROOT/usr/lib/qubes/qubes-windows-tools.iso

%files
/usr/lib/qubes/qubes-windows-tools-%{version}.%{release}.iso
/usr/lib/qubes/qubes-windows-tools.iso

%changelog

