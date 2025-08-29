# Backup Flame Clip Library and Projects

The scripts backup either Flame's clip library or the project folder (pre-2026) `/opt/Autodesk/project`. Archives are placed in a sub-folder based on hostname and are rotated based on the number of days you specify. The amount of duplicated data is kept to a minimum if your filesystem supports hardlinks by using the `--link-dest` option in rsync.

### Setup:
1. Modify `backup_dir` to where you want to place the archive.
2. Modify `num_backups_to_keep` to set your desired retention.

### How To Use:
`/bin/bash /path/to/backup_flame_cliplib.sh`
`/bin/bash /path/to/backup_flame_project.sh`

It's best to add this to your crontab so it is run every night at your desired time.

### What It Does:
1. Creates a dated folder.
2. Runs an rsync linking to the current folder to only update changes.
3. Sets the current folder to the latest archive.