"""
Script Name: Flame Nightly Archive
Script Version: 1.1

Creation date: 28.08.25
Modified date: 02.09.25

Description:

    Goes through the list of projects launched that day
    and appends to an existing nightly archive or creates
    one if one doesn't exist yet.

Change Log:

	v1.1: Added compatibility for older versions of Python.
	      The subprocess routine added universal_newlines=True in 3.7, changed
	      that to universal_newlines=True for 3.6 support.

    v1.0: Inital release

"""

import os
import sys
import socket
import subprocess

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


hostname = socket.gethostname()

# Define location variables
log_base = "/SHVFX/archives/_nightly/logs/"
archive_base = "/SHVFX/archives/_nightly/archives/"

# Define flame_archive options
init_backup_cmd = "flame_archive --ignore --archive --linked --omit sources,renders,maps,unused -P "
init_format_cmd = "flame_archive -f --capacity 100GB --name "

# Set log location and primary archive dir based on hostname
project_log = os.path.join(log_base,  hostname + ".log")
archive_dir_host = os.path.join(archive_base, hostname)


print (f"\n{bcolors.BOLD}----- Flame Nightly Archive Script -----{bcolors.ENDC}\n")
print (f"Project log:      {project_log}")

if os.path.isdir(archive_base):
        print(f"Archive location: {archive_base}\n")
else:
        print(f"ERROR: Archive location is unavailable: {archive_base}")
        exit()

all_projects = ""

# Is Flame running?
flame_running_check = "ps aux | grep \"opt/Autodesk/flame\" | wc -l"
flame_running_ps_count = subprocess.check_output(flame_running_check, shell=True, universal_newlines=True)
if int(flame_running_ps_count.strip()) > 2:
    print("Flame is running, so not doing anything. Exiting script.")
    sys.exit()
else:
    print("Flame is closed, so continuing to run backup script...")

if os.path.isfile(project_log):
	all_projects = open(project_log).read().splitlines()
if all_projects:

	# Unique list of all projects in log
	all_projects = list(set(all_projects))

	# Get total number of projects to be archived
	total_projects = len(all_projects)
	counter = 1

	if not os.path.exists(archive_dir_host):
		os.makedirs(archive_dir_host)

	print ("Beginning nightly archiving...\n")
	print (f"Found {total_projects} project(s) to be archived.\n")

	for project in all_projects:
		if project:

			project_and_flame = project.split(":")

			current_project = project_and_flame[0]
			current_flame_version = project_and_flame[1]

			print (f"({counter} of {total_projects}) - {bcolors.OKGREEN}{current_project}{bcolors.ENDC} using Flame {current_flame_version}")

			archive_dir = os.path.join(archive_dir_host, current_project)
			archive_file = os.path.join(archive_dir, current_project)

			# Define flame_archive location based on version from log
			flame_archive_bin = os.path.join("/opt/Autodesk/io", current_flame_version, "bin/")

			# Make an empty buffer for the formating and archiving subprocesses
			buffer = ""

			# See if the folder exists. If it doesn't, then we've never run so we need to format the archive.
			if not os.path.exists(archive_dir):
				os.makedirs(archive_dir)
				format_cmd = flame_archive_bin + init_format_cmd + current_project + " -F " + archive_file
				
				p = subprocess.Popen(format_cmd, shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE, universal_newlines=True)
				while True:
				    out = p.stderr.read(1)
				    if out == '' and p.poll() != None:
				        break
				    if out != '':
				        buffer += out
				        sys.stdout.write(out)
				        sys.stdout.flush()
				        
				        # !!!!  SECURITY ISSUE !!!!

				        # Hack because I don't have proper permissions via NFS setup
				        # Check if we've received the confirmation prompt
				        if "Confirm (y,n)?" in buffer:
				            p.stdin.write('y\n')
				            p.stdin.flush()
				            buffer = ""  # Clear buffer after responding
					
			# Back-up project
			backup_cmd = flame_archive_bin + init_backup_cmd + current_project + " -F " + archive_file

			p = subprocess.Popen(backup_cmd, shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE, universal_newlines=True)
			while True:
			    out = p.stderr.read(1)
			    if out == '' and p.poll() != None:
			        break
			    if out != '':
			        sys.stdout.write(out)
			        sys.stdout.flush()

			        # !!!!  SECURITY ISSUE !!!!

			        # Hack because I don't have proper permissions via NFS setup
			        # Check if we've received the confirmation prompt
			        if "Confirm (y,n)?" in buffer:
			            p.stdin.write('y\n')
			            p.stdin.flush()
			            buffer = ""  # Clear buffer after responding
			

			
			print (f"({counter} of {total_projects}) - {bcolors.OKGREEN}{current_project}{bcolors.ENDC} archive complted.")
			print("----------------------------------------\n")

			# Increment Counter
			counter += 1
	
	# Clear daily projects file
	open(project_log, "w").write("")
	print(f"{bcolors.BOLD}All backups have completed for {hostname}{bcolors.ENDC}")
	
else:
	print("No projects to backup.")