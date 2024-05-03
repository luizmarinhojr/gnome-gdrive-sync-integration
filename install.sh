#!/bin/bash

# 1. Crie a pasta, caso não existir, "~/.local/share/GDriveSync"
mkdir -p ~/.local/share/GDriveSync

# 2. Copie o diretório recursivamente de "./build" para "~/.local/share/GDriveSync"
cp -r ./build ~/.local/share/GDriveSync

# 3. Crie o arquivo gdrivesync.desktop em "~/.local/share/applications/GDriveSync"
desktop_file=~/.local/share/applications/gdrivesync.desktop
mkdir -p $(dirname $desktop_file)
cat <<EOT > $desktop_file
[Desktop Entry]
Name=GDriveSync
Comment=Sync with google drive
Exec=/home/$(logname)/.local/share/GDriveSync/build/linux/google_drive_fedora
Icon=/home/$(logname)/.local/share/GDriveSync/assets/icon.png
Terminal=false
Type=Application
Categories=Utilities;
EOT

echo "Success! The app is on apps menu!"
