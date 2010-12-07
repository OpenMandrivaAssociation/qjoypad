%define	longname  QJoyPad

Summary:	%{longname} - Emulate keyboard or mouse actions with a joystick
Name:		qjoypad
Version:	4.1.0
Release:	%mkrel 3
Source0:	http://downloads.sourceforge.net/project/qjoypad/qjoypad/%{name}-4.1/%{name}-%{version}.tar.gz
Group:		System/Kernel and hardware
License:	GPLv2
URL:		http://qjoypad.sourceforge.net/
BuildRoot:	%_tmppath/%{name}-build
BuildRequires:	qt4-devel
BuildRequires:	libxtst-devel

%description
QJoyPad converts input from a gamepad or joystick into key-presses or mouse 
actions, letting you control any X program with your game controller.
It comes with a convenient and easy-to-use interface.

%prep

%setup -q

perl -pi -e 's,^doc\.extra,#doc\.extra,' src/qjoypad.pro
sed -i '/icons\.extra/s,\$\${icons\.path},\$\(INSTALL_ROOT\)\$\${icons\.path},g' src/qjoypad.pro

%build
cd src
./config --prefix=%{_prefix}

%make

%install
rm -rf %{buildroot}

%makeinstall INSTALL_ROOT=%{buildroot} -C src

#icons for the menu
pushd icons
	convert gamepad4-64x64.png -resize 48x48 %{name}-48x48.png
	install -D -m 644 %{name}-48x48.png %{buildroot}%{_liconsdir}/%{name}.png

	convert gamepad4-64x64.png -resize 32x32 %{name}-32x32.png
	install -D -m 644 %{name}-32x32.png %{buildroot}%{_iconsdir}/%{name}.png

	convert gamepad4-64x64.png -resize 16x16 %{name}-16x16.png
	install -D -m 644 %{name}-16x16.png %{buildroot}%{_miconsdir}/%{name}.png
popd

install -d -m 755 %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=%{longname}
Comment=Emulate keyboard or mouse actions with a joystick
Exec=%{_bindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=Qt;Settings;X-MandrivaLinux-System-Configuration-Other;
EOF

%if %mdkversion < 200900
%post
%{update_menus}
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README.txt LICENSE.txt
%{_bindir}/%{name}
%{_liconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_datadir}/pixmaps/%{name}
%{_datadir}/applications/mandriva-%{name}.desktop
