import paramiko
import colored
from colored import stylize

# Variables
username = "root"
password = "aristo1"
directories = ["/usr/local/forescout/rollback/*", "/usr/local/forescout/cores/*", "/usr/local/forescout/backup/*", "/usr/src/rollback/*", "/usr/src/UPGRADES/*", "/usr/local/forescout/plugin/ms/backup/*", "/usr/src/fssetup.zip", "/usr/local/forescout/stats/2020*",  "/usr/local/forescout/webapps/portal/wsusscn2.cab" ,"/root/*"]
menu_list = ["machine cleaner before upgrade", "tech-support health check", "install log errors"]
ssh = paramiko.SSHClient()

# -----------------------------------MENU-----------------------------------------------------------


def format_menu(menu_lists):
    for s in menu_lists:
        return f"{menu_lists.title()}"

def print_menu(menu_list_is):

    import colored
    from colored import stylize

    print(stylize("<<< Welcome to QA Tool >>>", colored.fg("blue")))
    print("-------------------------------------------------------")
    print(stylize("Our available options are: ", colored.fg("green")))
    #print(" ")
    i = 0
    for menu in menu_list_is:
        i = i + 1
        print(str(i) + " - " + format_menu(menu))
    print(" ")

def user_menu_selection():
    user_choice = input("Please enter your choice: ")
    print(" ")
    if user_choice == "1":
        list_of_hosts()
    elif user_choice == "2":
        em_ip()
    elif user_choice == "3":
        print("This option under construction by Rafael M")
    else:
        print(stylize("<<< Your choice is wrong  >>>", colored.fg("red")))
        print(stylize("      PLEASE TRY AGAIN", colored.fg("red")))
        print(" ")
        print_menu(menu_list)
        user_menu_selection()

# -----------------------------------SET EM IP------------------------------------------------------------------
def em_ip():

    host = input("Please enter the IP address of the EM server you wish to connect with: ")
    create_ssh(host, username, password)
    exec_command_tech_support()
    close_ssh(host)
    return host

# -----------------------------------CREATE SSH CONNECTION-------------------------------------------------------
def create_ssh(host, username, password):

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print(stylize("Creating connection...to the following IP: " + host, colored.fg("blue")))
    ssh.connect(host, username=username, password=password)
    print(stylize("Connected!", colored.fg("blue")))
    print("----------------------------------------------------------------------------------")

# -----------------------------------OUTPUT FUNCTION-------------------------------------------------------------
def print_stdout(stdout):
    import colored
    from colored import stylize

    output = ""
    lines = stdout.readlines()
    for line in lines:
        output = output+line
    if output!="":
        print(output)
    else:
        print(stylize("Warning: There was no files to delete!", colored.fg("green")))

# -----------------------------------TECH-SUPPORT COMMAND EXECUTION----------------------------------------------
def exec_command_tech_support():
    # for folder in directories:
    print(stylize("Please wait for the Tech-Support Health Check output ... ", colored.fg("cyan")))
    stdin, stdout, stderr = ssh.exec_command(f"fstool tech-support --health-check --oneach-all", get_pty=True)
    print_stdout(stdout)
    print("----------------------------------------------------------------------------------")

# -----------------------------------FREE SPACE COMMAND EXECUTION----------------------------------------------
# delete directories before upgrade and print df -h after so you can check free space on disk
def exec_commands_to_free_space():
    for folder in directories:
        print(folder)
        stdin, stdout, stderr = ssh.exec_command(f"rm -rfv {folder}", get_pty=True)
        print_stdout(stdout)

    print("----------------------------------------------------------------------------------")
    stdin, stdout, stderr = ssh.exec_command("df -h", get_pty=True)
    print_stdout(stdout)

# -----------------------------------CLOSE SSH CONNECTION--------------------------------------------------------
def close_ssh(x):
    import colored
    from colored import stylize

    print("----------------------------------------------------------------------------------")
    print(stylize("Closing connection... for the following host IP: " + x, colored.fg("cyan")))
    ssh.close()
    print(stylize("Closed!", colored.fg("cyan")))

# -----------------------------------CREATE LIST OF MACHINES FOR CLEANUP------------------------------------------
def list_of_hosts():
    hosts = []
    # number of elements as input
    n = int(input("Enter number of machines that you want to cleanup before the upgrade: "))

    # Iterating till the range
    for i in range(0, n):
        ele = input("Please enter the IP Address of the server you wish to connect with: ")
        # adding the element
        hosts.append(ele)
    print(stylize("Host collection was done!", colored.fg("magenta")))
    print(" ")

    for ip in hosts:
        create_ssh(ip, username, password)
        exec_commands_to_free_space()
        close_ssh(ip)
        print(stylize("----------------------------------------------------------------------------------", colored.fg("yellow")))
        print(stylize("##################################################################################", colored.fg("cyan")))
        print(stylize("----------------------------------------------------------------------------------", colored.fg("yellow")))
    return hosts

# -----------------------------------MAIN------------------------------------------
print_menu(menu_list)
user_menu_selection()

