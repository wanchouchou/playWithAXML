#!/bin/sh

#APK=$1
#TEMP_DIR="${APK}_temp"
#rm -rf $TEMP_DIR *new
#mkdir -p $TEMP_DIR
#unzip $APK -d $TEMP_DIR

echo "zip apk"
cd out/
#do your job
rm -r META-INF/
zip -9 -r ../new.apk ./*
cd ..
echo "sig apk"
jarsigner -keystore "./clientkeystore" -sigalg SHA1withRSA -digestalg SHA1 new.apk  CLIENT
