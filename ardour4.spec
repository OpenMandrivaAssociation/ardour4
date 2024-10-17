%define oname	Ardour
%define debug_package	%{nil}

Name:		ardour4
Version:	4.7.0
Release:	1
Summary:	Professional multi-track audio recording application
Group:		Sound
License:	GPLv2+
URL:		https://ardour.org/
# NB to receive a free (as beer) source tarball you need to give your e-mail address here:
# "http://community.ardour.org/download_process_selection_and_amount" to get a download link
Source0:	%{oname}-%{version}.tar.bz2
Source1:	%{name}.desktop
Source100:	ardour4.rpmlintrc

BuildRequires:	boost-devel
BuildRequires:	dmalloc
BuildRequires:	doxygen
BuildRequires:	gettext
BuildRequires:	graphviz
BuildRequires:	gtk+2.0-devel >= 2.12.1
BuildRequires:	gtkmm2.4-devel >= 2.8
BuildRequires:	shared-mime-info
BuildRequires:	xdg-utils
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(aubio) >= 0.3.2
BuildRequires:	pkgconfig(cppunit) >= 1.12.0
BuildRequires:	pkgconfig(cwiid)
BuildRequires:	pkgconfig(fftw3)
BuildRequires:	pkgconfig(flac) >= 1.2.1
BuildRequires:	pkgconfig(glib-2.0) >= 2.2
BuildRequires:	pkgconfig(libart-2.0)
BuildRequires:	pkgconfig(libcurl) >= 7.0.0
BuildRequires:	pkgconfig(libgnomecanvas-2.0) >= 2.30
BuildRequires:	pkgconfig(libgnomecanvasmm-2.6) >= 2.16
BuildRequires:	pkgconfig(liblo) >= 0.24
BuildRequires:	pkgconfig(libusb)
BuildRequires:	pkgconfig(libusb-1.0)
BuildRequires:	pkgconfig(libxslt)
BuildRequires:	pkgconfig(lilv-0) >= 0.14
BuildRequires:	pkgconfig(lrdf) >= 0.4.0
BuildRequires:	pkgconfig(ltc) >= 1.1.0
BuildRequires:	pkgconfig(lv2) >= 1.0.15
BuildRequires:	pkgconfig(ogg) >= 1.1.2
BuildRequires:	pkgconfig(raptor2)
BuildRequires:	pkgconfig(redland)
BuildRequires:	pkgconfig(rubberband)
BuildRequires:	pkgconfig(samplerate)
BuildRequires:	pkgconfig(serd-0) >= 0.14.0
BuildRequires:	pkgconfig(sndfile) >= 1.0.18
BuildRequires:	pkgconfig(sord-0) >= 0.8.0
BuildRequires:	pkgconfig(sndfile)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(sratom-0) >= 0.4.0
BuildRequires:	pkgconfig(suil-0) >= 0.6.0
BuildRequires:	pkgconfig(uuid)
BuildRequires:	pkgconfig(vamp-sdk)
BuildRequires:	pkgconfig(taglib) >= 1.6
BuildRequires:	desktop-file-utils
BuildRequires:	pkgconfig(jack)
BuildRequires:	jackit
BuildRequires:	python2-devel

Requires:	jackit
Requires:	gtk-engines2

Provides:	ardour4 = %{EVRD}
Conflicts:	ardour3

%description
Ardour3 is a digital audio workstation. You can use it to record, edit and mix
multi-track audio. You can produce your own CDs, mix video sound tracks, or
just experiment with new ideas about music and sound.

Ardour3 capabilities include: multi channel recording, non-destructive editing
with unlimited undo/redo, full automation support, a powerful mixer, unlimited
tracks/busses/plugins, time-code synchronization, and hardware control from
surfaces like the Mackie Control Universal.

You must have jackd running and an ALSA sound driver to use Ardour3. If you are
new to jackd, try qjackctl.

See the online user manual at http://en.flossmanuals.net/ardour/index/

%prep
%setup -qn %{oname}-%{version}

%build
export CXX='g++ -std=c++11'

python2 waf configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --configdir=%{_sysconfdir} \
    --program-name=Ardour4 \
    --nls \
    --docs

python2 waf build \
    --nls \
    --docs

python2 waf i18n_mo

%install
python2 waf install --destdir=%{buildroot}

desktop-file-install \
--dir=%{buildroot}%{_datadir}/applications %{SOURCE1}

# Symlink icons and mimetypes into the right folders
install -d -m 0755 %{buildroot}%{_iconsdir}

for i in 16 22 32 48; do
install -d -m 0755 %{buildroot}%{_iconsdir}/hicolor/${i}x${i}/apps
install -d -m 0755 %{buildroot}%{_iconsdir}/hicolor/${i}x${i}/mimetypes
ln -s %{_datadir}/%{name}/icons/application-x-ardour_${i}px.png \
%{buildroot}%{_iconsdir}/hicolor/${i}x${i}/mimetypes/application-x-ardour3.png
ln -s %{_datadir}/%{name}/icons/ardour_icon_${i}px.png \
%{buildroot}%{_iconsdir}/hicolor/${i}x${i}/apps/ardour4.png
done

%files
%doc README
%{_bindir}/%{name}
%{_libdir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/ardour.menus
%config(noreplace) %{_sysconfdir}/%{name}/step_editing.bindings
%config(noreplace) %{_sysconfdir}/%{name}/mnemonic-us.bindings
%config(noreplace) %{_sysconfdir}/%{name}/mixer.bindings
%config(noreplace) %{_sysconfdir}/ardour4/clearlooks.rc
%config(noreplace) %{_sysconfdir}/ardour4/dark.colors
%config(noreplace) %{_sysconfdir}/ardour4/default_ui_config
%config(noreplace) %{_sysconfdir}/ardour4/system_config
%config(noreplace) %{_sysconfdir}/ardour4/trx.menus
%dir %{_sysconfdir}/%{name}/export
%config(noreplace) %{_sysconfdir}/%{name}/export/CD.format
%{_iconsdir}/hicolor/*
