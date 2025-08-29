# Nightly Archive

Creates a bare-bones archive from a list of projects derived from the hook [project_log.py](https://github.com/kmatchbox/PythonHooks/tree/main/log_project). This is meant to be run automatically by cron every night and acts as an emergency archive. No media is cached, all renders are flushed. It's a lean as you can get.

Each hosts creates it's own sub-folder and places the archives there to avoid multiple machines trying to archive the same project at the same time. It will also confirm in the case of group permissions issues.

### Setup:
1. Download, configure and put [project_log.py](https://github.com/kmatchbox/PythonHooks/tree/main/log_project) where your Flame hooks are located.
2. Modify the `log_base` and `archive_base` to where both the log and your archives exists.

### How To Use:
`python3 /path/to/flame_nightly_archive.py`

It's best to add this to your crontab so it is run every night at your desired time.

### What It Does:
1. Goes through the log created by [project_log.py](https://github.com/kmatchbox/PythonHooks/tree/main/log_project).
2. Checks if a folder for the project already exists. If not, it creates one and formats a new archive.
3. Archives the project based on the options within the script which is currently as bare-bones as possible.
4. Clears the log