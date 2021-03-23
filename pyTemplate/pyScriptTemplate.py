'''
    @name
        pyScriptTemplate.py

    @description
        Python Script Template
'''

''' Import Section '''
import os, sys, pathlib, subprocess, argparse, configparser
from datetime import datetime

''' Files paths '''
configFilePath = os.path.join(pathlib.Path(__file__).parent, 'scriptConfig.ini')
securityScriptPath = os.path.join(pathlib.Path(__file__).parent, 'securityScriptChecker.py')

''' Config parser '''
configParser = configparser.ConfigParser()
configParser.read(configFilePath)
configSections = configParser.sections()

''' Argument parser '''
def argParse():
    scriptTemplate = argparse.ArgumentParser(description='Default help message for Python Script Template')

    scriptTemplate.add_argument('--verbose',
                            '-v',
                            action='store_true',
                            help="Set script logging to verbose mode")

    scriptTemplate.add_argument('--quiet',
                            '-q',
                            action='store_true',
                            help="Set script logging to quiet mode")

    return scriptTemplate.parse_args()

''' Functions Section '''
def enableQuietMode():
    sys.stdout = open(os.devnull, 'w')

''' Main function '''
def main():
    # Get current date and time
    currentDateAndTime = datetime.now().strftime('%d-%B-%Y %H:%M:%S')

    ''' Execute parse_args() '''
    args = argParse()

    ''' Enable quiet mode if flag is set '''
    if args.quiet:
        enableQuietMode()

    logsDir = configParser['Directories']['logsDir']
    cronDir = configParser['Directories']['cronDir']
    
    print('Hi User, current date and time: {} \nLogs are located in: {} \nCron directory is: {}'.format(currentDateAndTime, logsDir, cronDir))

    print('Performing variables check for security purposes...')
    securityCheck = subprocess.Popen(['python3', securityScriptPath, '--script', pathlib.Path(__file__), '--config', configFilePath, '-ni'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    stdout, stderr = securityCheck.communicate()

    if securityCheck.returncode == False:
        print('Security variables check failed, your script has some undefined variables.')
        while True:
                ans = str(input('Do you want to continue and run script anyway?'))
                if not ans.lower() in ('y', 'n'):
                    print("Answer should be y or n")
                    continue
                else:
                    break
            
        if ans == 'y':
            pass
        if ans == 'n':
            print('Aborting...')
            sys.exit(1)

    elif securityCheck.returncode == True:
        print('Security variables check succeed, script will execute')

''' Main function execution '''
if __name__ == '__main__':
    main()
