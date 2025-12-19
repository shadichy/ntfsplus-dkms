%global dkms_name ntfsplus

Name:           dkms-%{dkms_name}
Version:        2025.11.27_20251219
Release:        1%{?dist}
Summary:        DKMS module for NTFSPLUS
Group:          System Environment/Kernel

License:        GPL-2.0-only
URL:            https://github.com/shadichy/ntfsplus-dkms
BuildArch:  noarch

Source0:        https://git.kernel.org/pub/scm/linux/kernel/git/linkinjeon/ntfs.git/snapshot/ntfs-next.tar.gz#/%{dkms_name}-%{version}.tar.gz
Source1:        dkms.conf
Source2:        90-udev-prefer-ntfsplus.rules
Patch0:         0001-fs-ntfsplus-inode.c-Resolve-import-for-inode_generic.patch
Patch1:         0002-ntfsplus-Resolve-iomap_-arguments-temporarily-for-ke.patch
Patch2:         0003-ntfsplus-Backport-ntfs_iomap.c-functions-to-kernels-.patch
Patch3:         0004-ntfsplus-file.c-Using-mmap-instead-of-mmap_prepare-f.patch
Patch4:         0005-ntfsplus-compress.c-using-page-index-instead-of-page.patch
Patch5:         0006-ntfsplus-Update-iomap_zero_range-iomap_page_mkwrite-.patch
Patch6:         0007-ntfsplus-Backport-ntfs_mkdir-for-kernels-older-than-.patch
Patch7:         0099-fs-ntfsplus-Makefile-DKMS-patch.patch

Provides:   %{dkms_name}-kmod = %{?epoch:%{epoch}:}%{version}
Requires:   dkms

%description
A new NTFS driver for Linux promised to be better than NTFS3. This package provides the DKMS module for ntfsplus.

%package udev
Summary:        udev rules for ntfsplus-dkms
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch
%description udev
This package contains udev rules to prefer ntfsplus over other NTFS drivers.

%prep
%autosetup -n ntfs-next -p1
sed -i "s/@PKGVER@/%{version}/" %{SOURCE1} 

%build

%install

# Install dkms.conf
mkdir -p %{buildroot}%{_usrsrc}/%{dkms_name}-%{version}/include/uapi/linux/
cp %{SOURCE1} %{buildroot}%{_usrsrc}/%{dkms_name}-%{version}/dkms.conf

# Install kernel module sources
cp -frpT %{_builddir}/ntfs-next/fs/ntfsplus %{buildroot}%{_usrsrc}/%{dkms_name}-%{version}
install -Dm644 %{_builddir}/ntfs-next/include/uapi/linux/ntfs.h %{buildroot}%{_usrsrc}/%{dkms_name}-%{version}/include/uapi/linux/ntfs.h

# Install udev rule
install -Dm644 %{SOURCE2} %{buildroot}/usr/lib/udev/rules.d/90-udev-prefer-ntfsplus.rules

%files
%{_usrsrc}/%{dkms_name}-%{version}

%files udev
/usr/lib/udev/rules.d/90-udev-prefer-ntfsplus.rules

%post
dkms add -m %{dkms_name} -v %{version} -q --rpm_safe_upgrade || :
# Rebuild and make available for the currently running kernel:
dkms build -m %{dkms_name} -v %{version} -q --force
dkms install -m %{dkms_name} -v %{version} -q --force

%preun
# Remove all versions from DKMS registry:
dkms remove -m %{dkms_name} -v %{version} -q --all --rpm_safe_upgrade || :

%post udev
udevadm trigger

%postun udev
udevadm trigger

%changelog
* Thu Dec 18 23:18:38 +07 2025 shadichy <shadichy@blisslabs.org>
- Change from `git am` to `git apply` to avoid unkown identification
 
* Wed Dec 17 10:03:14 +07 2025 shadichy <shadichy@blisslabs.org>
- feat: Using version checker instead of definition checker for patch 0001
 
* Mon Dec 1 20:23:36 +07 2025 shadichy <shadichy@blisslabs.org>
- Update make CFLAGS_MODULE for GCC support
 
* Sun Nov 30 18:08:56 +07 2025 shadichy <shadichy@blisslabs.org>
- Update patches to sync source
 
* Thu Nov 6 21:24:18 +07 2025 shadichy <shadichy@blisslabs.org>
- Update patches for Refactor mmap_prepare function of file.c
 
* Thu Nov 6 17:46:33 +07 2025 shadichy <shadichy@blisslabs.org>
- Update patches for Refactored iomap_file_buffered_write, iomap_truncate_page, iomap_zero_range and iomap_page_mkwrite
 
* Wed Nov 5 01:10:59 +07 2025 shadichy <shadichy@blisslabs.org>
- PKGBUILD: update `pkgver()` to show FETCH_HEAD commit date
 
* Wed Nov 5 00:14:25 +07 2025 shadichy <shadichy@blisslabs.org>
- DLAGENTS: Fix verifier git in-progress abortion
 
* Tue Nov 4 18:32:41 +07 2025 shadichy <shadichy@blisslabs.org>
- Using upstream module source
 
* Tue Nov 4 13:24:23 +07 2025 shadichy <shadichy@blisslabs.org>
- Update PKGBUILD info
 
* Mon Nov 3 18:51:15 +07 2025 shadichy <shadichy@blisslabs.org>
- Update patches for Remove optional properties prepare_ioend and discard_folio
 
* Mon Nov 3 18:51:15 +07 2025 shadichy <shadichy@blisslabs.org>
- Updated patches for Backport to 6.12
 
* Mon Nov 3 18:51:14 +07 2025 shadichy <shadichy@blisslabs.org>
- Added 6.15-6.16 patches
 
* Wed Oct 29 10:43:33 +07 2025 shadichy <shadichy@blisslabs.org>
- PKGBUILD: update source file name, checksum and package opt dependencies
 
* Sun Oct 26 12:09:29 +07 2025 shadichy <shadichy@blisslabs.org>
- Replace patches
 
* Sun Oct 26 12:09:29 +07 2025 shadichy <shadichy@blisslabs.org>
- Remove unnecessary git submodule
 
* Sun Oct 26 12:09:29 +07 2025 shadichy <shadichy@blisslabs.org>
- Add some patches to backport the driver to 6.16 or older kernels
 
* Thu Oct 23 13:59:22 +07 2025 shadichy <shadichy@blisslabs.org>
- Remove `epoch` & fix provides/conflicts & fix string typo
 
* Thu Oct 23 02:01:48 +07 2025 shadichy <shadichy@blisslabs.org>
- Initial
