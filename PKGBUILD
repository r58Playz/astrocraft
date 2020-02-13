# Maintainer: Toshit Chawda <toshit307@gmail.com>
pkgname=astrocraft-python-git
pkgver=r237.b17848c
pkgrel=1
pkgdesc="astrocraft-python: a clone of Minecraft writen in Python"
arch=('any')
url="https://github.com/r58Playz/astrocraft-python"
license=('GPL')
groups=()
depends=('python' 'python-pip' 'cython' 'python-msgpack' 'ffmpeg' 'python-pyglet' 'qt5-tools' 'qt5-x11extras' 'qt5-script' 'libimagequant' 'qt5-speech' 'qt5-webkit' 'qt5-webengine' 'lapack' 'qt5-networkauth' 'tk' 'qt5-svg' 'pyside2' 'cblas' 'qt5-xmlpatterns')
makedepends=('python-cx_freeze')
provides=("astrocraft-python-git")
conflicts=("astrocraft-python-stable")
replaces=()
backup=()
options=()
install=astrocraft-python-git.install
source=('astrocraft-python::git+https://github.com/r58Playz/astrocraft-python.git#branch=master')
noextract=()
md5sums=('SKIP')

# Please refer to the 'USING VCS SOURCES' section of the PKGBUILD man page for
# a description of each element in the source array.

pkgver() {
	cd "$srcdir/astrocraft-python"

# Git, no tags available
	printf "r%s.%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short HEAD)"
}

prepare() {
	cd "$srcdir/astrocraft-python"
	pip install plyer
}

build() {
	cd "$srcdir/astrocraft-python"
	python setup.py build
	chmod +x build/exe.*/AstroCraft
}

package() {
	cd "$srcdir/astrocraft-python"
	mkdir --parents "$pkgdir/usr/bin/AstroCraft"
	mkdir --parents "$pkgdir/usr/lib"
	cp -r $srcdir/astrocraft-python/build/exe.*/* "$pkgdir/usr/bin/AstroCraft/"
	cp -r $srcdir/astrocraft-python/build/exe.*/lib/* "$pkgdir/usr/lib"
}
