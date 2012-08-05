#!/bin/bash

PROGNAME=pyrocket
VERSION=0.7
RELEASE_NAME=$PROGNAME-$VERSION

svn export src $RELEASE_NAME.orig
cd $RELEASE_NAME.orig
rm -r icons
rm -r debian
cd ..
svn export src $RELEASE_NAME
cd $RELEASE_NAME
rm -r icons
debuild
cd ..
rm -r $RELEASE_NAME

echo -n "Do you want to install the new .deb? [Y/n]: "
read character
case $character in
    [Yy] | "" ) echo "You responded in the affirmative."
	sudo gdebi *.deb
        ;;
    * ) echo "Fine, then."
esac
