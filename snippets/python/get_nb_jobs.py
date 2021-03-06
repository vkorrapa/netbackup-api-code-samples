import sys
import api_requests
import json
import texttable as tt

protocol = "https"
nbmaster = ""
username = ""
password = ""
domainname = ""
domaintype = ""

port = 1556

def print_job_details(data):
	tab = tt.Texttable()
	headings = ['Job ID','Type','State','Status']
	tab.header(headings)

	for data_item in data:
		tuple_value = (data_item['attributes']['jobId'], data_item['attributes']['jobType'], data_item['attributes']['state'], data_item['attributes']['status'])
		tab.add_row(tuple_value)

	print(tab.draw())


def print_disclaimer():
	print("-------------------------------------------------------------------------------------------------")
	print("--                          This script requires Python3.5 or higher.                          --")
	print("--    If your current system does not have Python3.5 or higher installed, this will not work.  --")
	print("-------------------------------------------------------------------------------------------------\n")
	print("Executing this library requires some additional python3.5 libraries like \n\t'requests' \n\t'texttable'.\n\n")
	print("'texttable' library is just used to show the 'pretty' version of the API response,\nyou might not need it for your netbackup automation.\n")
	print("You will, however, require 'requests' library to make the API calls.\n")
	print("You can install the dependent libraries using the following commands: ")
	print("pip install requests texttable")
	print("-------------------------------------------------------------------------------------------------\n\n\n")
	print("You can specify the 'nbmaster', 'username' and 'password' as command-line parameters\n")
	print_usage()

def print_usage():
	print("Example:")
	print("python -W ignore get_nb_jobs.py -nbmaster <master_server> -username <username> -password <password> [-domainname <domain_name>] [-domaintype <domain_type>]\n\n\n")

def read_command_line_arguments():
	if len(sys.argv)%2 == 0:
		print_usage()
		exit()

	global nbmaster
	global username
	global password
	global domainname
	global domaintype

	for i in range(1, len(sys.argv), 2):
		if sys.argv[i] == "-nbmaster":
			nbmaster = sys.argv[i + 1]
		elif sys.argv[i] == "-username":
			username = sys.argv[i + 1]
		elif sys.argv[i] == "-password":
			password = sys.argv[i + 1]
		elif sys.argv[i] == "-domainname":
			domainname = sys.argv[i + 1]
		elif sys.argv[i] == "-domaintype":
			domaintype = sys.argv[i + 1]
		else:
			print_usage()
			exit()

	if nbmaster == "":
		print("Please provide the value for 'nbmaster'")
		exit()
	elif username == "":
		print("Please provide the value for 'username'")
		exit()
	elif password == "":
		print("Please provide the value for 'password'")
		exit()

print_disclaimer()

read_command_line_arguments()

base_url = protocol + "://" + nbmaster + ":" + str(port) + "/netbackup"

jwt = api_requests.perform_login(username, password, base_url, domainname, domaintype)

jobs = api_requests.get_netbackup_jobs(jwt, base_url)

data = jobs['data']

if len(data) > 0:
	print_job_details(data)
