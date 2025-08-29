#!/bin/bash

# Define the paths
backup_dir="/SHVFX/backup/$(hostname)/flame_cliplib"
source_dir="/opt/Autodesk/clip/stonefs"

# Number of backup copies to retain
num_backups_to_keep=14

# Ensure the backup directory exists
mkdir -p "$backup_dir"

# Backup the folder with timestamp and link to current
date=`date "+%Y-%m-%dT%H_%M_%S"`
rsync -rtlDc -v --progress --link-dest=$backup_dir/current \
   $source_dir $backup_dir/backup-$date

rm -f $backup_dir/current
ln -s backup-$date $backup_dir/current
echo " "

echo "Backup Done."

echo "Rotating backups..."

# Remove old backups exceeding the specified limit
num_backups=$(ls -1 "$backup_dir" | grep -c '^backup-')
num_backups_to_remove=$((num_backups - num_backups_to_keep))

if [ $num_backups_to_remove -gt 0 ]; then
    # List old backups, sort by timestamp, and remove the excess    
    old_backups=$(ls -1 "$backup_dir" | grep '^backup-' | sort | head -n $num_backups_to_remove)
    
    for old_backup in $old_backups; do
        rm -rf "$backup_dir/$old_backup"
        echo "Removed old backup: $old_backup"
    done
fi
