
#!usr/bin/python3
import subprocess
import time
import sys
sshKeyName = 'ec2-key'
extendedKeyName = sshKeyName+".pem"
instanceIPAddress="34.227.151.185"
command="sudo pwd"
fileName = 'check_webserver.py'
filePath = '.'

def connectToInstance():
    # appending the file extension to the filename
    extendedKeyName = sshKeyName+".pem"
    # the hardcoded command to
    command="sudo pwd"
    fileName = "check_webserver.py" # hard code this for now, can be changed later
    filePath = '.' # this is the home folder

    print("Connecting to instance using key: " + str(extendedKeyName))

    # test an SSH connection to the instance
    commands = ['ssh', '-t', '-o', 'StrictHostKeyChecking=no', '-i', extendedKeyName, 'ec2-user@' + str(instanceIPAddress), command]
    commandString = ' '.join(commands) # convert the list of commands to a string so the command works. The ' ' keeps the spaces between the arguments
    (status, output) = subprocess.getstatusoutput(commandString)
    print(output)

    # scp a file up to the server
    cpToInstance = ['scp','-i', extendedKeyName, fileName, 'ec2-user@' + str(instanceIPAddress+':'+filePath)]
    commandString2 = ' '.join(cpToInstance) # convert the list of commands to a string so the command works
    print(commandString2)
    (status, output) = subprocess.getstatusoutput(commandString2)
    print(output)
    print(status)

    # change the permissions of the file
    chmodFile = ['ssh', '-i',extendedKeyName, 'ec2-user@' + str(instanceIPAddress), 'sudo chmod a+x',fileName]
    chmodCommand = ' '.join(chmodFile) # convert the list of commands to a string so the command works
    print(chmodCommand)
    (status, output) = subprocess.getstatusoutput(chmodCommand)
    print(output)
    print(status)

    # execute the  file
    executeFile = ['ssh', '-i',extendedKeyName, 'ec2-user@' + str(instanceIPAddress + ' ./'+fileName)]
    executeCommand = ' '.join(executeFile) # convert the list of commands to a string so the command works
    print(executeCommand)
    (status, output) = subprocess.getstatusoutput(executeCommand)
    print(output)
    print(status)


	#cmd = 'ssh -t -o StrictHostKeyChecking=no -i ec2-key.pem ec2-user@54.167.229.203' 

def main():
	print("Starting script")

	connectToInstance()
	sys.exit()



if __name__ == '__main__':
	main()