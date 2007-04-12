%define	name   qjoypad
%define	longname  QJoyPad
%define	version 3.4.1
%define rel	1
%define	release %mkrel %rel

Summary:	%{longname} - Emulate keyboard or mouse actions with a joystick
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	http://prdownloads.sourceforge.net/qjoypad/%{name}-%{version}.tar.bz2
Source1:	%{name}-16x16.png.bz2
Source2:	%{name}-32x32.png.bz2
Source3:	%{name}-48x48.png.bz2
Group:		System/Kernel and hardware
License:	GPL
URL:		http://qjoypad.sourceforge.net/
BuildRoot:	%_tmppath/%{name}-build
BuildRequires:	qt3-devel
BuildRequires:	libxtst-devel

%description
QJoyPad converts input from a gamepad or joystick into keypresses or mouse 
actions, letting you control any X program with your game controller.
It comes with a convenient and easy-to-use interface.

%prep

%setup -q
bzcat %{SOURCE1} > %{name}-16x16.png
bzcat %{SOURCE2} > %{name}-32x32.png
bzcat %{SOURCE3} > %{name}-48x48.png

perl -pi -e 's,^doc\.extra,#doc\.extra,' src/qjoypad.pro
sed -i '/icons\.extra/s,\$\${icons\.path},\$\(INSTALL_ROOT\)\$\${icons\.path},g' src/qjoypad.pro

%build
cd src
./config --prefix=%{_prefix}

%make

%install
rm -rf %{buildroot}

cd src
%makeinstall INSTALL_ROOT=%{buildroot}
cd ..

#icons for the menu
install -D -m 644 %{name}-48x48.png $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png
install -D -m 644 %{name}-32x32.png $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
install -D -m 644 %{name}-16x16.png $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png

install -d -m 755 $RPM_BUILD_ROOT%{_menudir}
cat >$RPM_BUILD_ROOT%{_menudir}/%{name} <<EOF
?package(%{name}): \
	command="%{_bindir}/%{name}" \
	needs="X11" \
	section="System/Configuration/Other" \
	icon="%{name}.png" \
	title="%{longname}" \
	longtitle="%{summary}" \
	xdg="true"
EOF

install -d -m 755 %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=%{longname}
Comment=Emulate keyboard or mouse actions with a joystick
Exec=%{_bindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=Qt;TrayIcon;Settings;X-MandrivaLinux-System-Configuration-Other;
Encoding=UTF-8
EOF

%files
%defattr(-,root,root)
%doc README.txt LICENSE.txt
%{_bindir}/%{name}
%{_liconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_menudir}/%{name}
%{_datadir}/pixmaps/%{name}
%{_datadir}/applications/mandriva-%{name}.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{update_menus}

%postun
%{clean_menus}


