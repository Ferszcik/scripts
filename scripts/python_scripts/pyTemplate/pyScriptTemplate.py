'''
    @name
        pyScriptTemplate.py

    @description
        Python Script Template

    @date
        25-mar-2021
    
    @author
        Default

    @version
        0.1v
'''

''' Import Section '''
import os, sys, pathlib, subprocess, argparse, configparser, logging
from datetime import datetime

''' Files paths '''
configFilePath = os.path.join(pathlib.Path(__file__).parent, 'scriptConfig.ini')
securityScriptPath = os.path.join(pathlib.Path(__file__).parent, 'securityScriptChecker.py')
logFilePath = os.path.join(pathlib.Path.home(), 'logs', __file__.replace('.py', '.log'))

# Create logs directory if it doesn't exist
os.makedirs(os.path.dirname(logFilePath), exist_ok=True)

''' Config parser

    Eg. usage:
    logsDir = configParser['Directories']['logsDir']
    cronDir = configParser['Directories']['cronDir']
'''
configParser = configparser.ConfigParser()
configParser.read(configFilePath)

''' Logger setup '''
def setupLogger(args):
    '''
    Logging levels from lowest priority:

    DEBUG
    INFO
    WARNING
    ERROR
    CRITICAL
    '''
    fileHandler = logging.FileHandler(filename=logFilePath)
    stdoutHandler = logging.StreamHandler(sys.stdout)
    loggerHandlers = [fileHandler, stdoutHandler]

    # Set logging level depending on mode flag
    if args.verbose or args.testing:
        logging.basicConfig(handlers=loggerHandlers, format='%(asctime)s - %(process)d - %(levelname)s - %(message)s', level=logging.DEBUG, datefmt='%d-%b-%y %H:%M:%S')
    elif args.quiet:
        logging.basicConfig(handlers=loggerHandlers, format='%(asctime)s - %(process)d - %(levelname)s - %(message)s', level=logging.ERROR, datefmt='%d-%b-%y %H:%M:%S')
    else:
        logging.basicConfig(handlers=loggerHandlers, format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO, datefmt='%d-%b-%y %H:%M:%S')

''' Argument parser setup '''
def setupParser():
    scriptTemplate = argparse.ArgumentParser(description=sys.modules[__name__].__doc__,
                                             formatter_class=argparse.RawDescriptionHelpFormatter)

    scriptTemplate.add_argument('--verbose',
                            '-v',
                            action='store_true',
                            help="Set script logging to verbose mode")

    scriptTemplate.add_argument('--quiet',
                            '-q',
                            action='store_true',
                            help="Set script logging to quiet mode")

    scriptTemplate.add_argument('--noCheck',
                            '-nc',
                            action='store_true',
                            help="Disable security variables check at the start of execution")

    # Add your arguments here

    return scriptTemplate.parse_args()

''' Functions Section '''
# Add your functions here

''' Main function 
    @name
        main

    @description
        Main function of the script where all the magic happens, add your code at the end of the function and modify description.
        Add your arguments and functions to dedicated sections.
'''
def main():
    # Get current date and time
    currentDateAndTime = datetime.now().strftime('%d-%B-%Y %H:%M:%S')

    ''' Setup Argument Parser and Logger '''
    args = setupParser()
    setupLogger(args)

    logging.info(f'Hi User, current date and time: {currentDateAndTime}!')

    # Perform variables security check with securityScriptChecker.py
    if not args.noCheck:
        logging.info('Performing variables check for security purposes...')
        securityCheck = subprocess.Popen(['python3', securityScriptPath, '--script', pathlib.Path(__file__), '--config', configFilePath, '-ni'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        stdout, stderr = securityCheck.communicate()

        if securityCheck.returncode == False:
            logging.error('Security variables check failed, your script has some undefined variables.')
            while True:
                    ans = str(input('Do you want to continue and run script anyway?'))
                    if not ans.lower() in ('y', 'n'):
                        logging.error("Answer should be y or n")
                        continue
                    else:
                        break
                
            if ans == 'y':
                pass
            if ans == 'n':
                logging.error('Ok, aborting execution...')
                sys.exit(1)

        elif securityCheck.returncode == True:
            logging.info('Security variables check succeed, script will execute')

    # Add your code here

''' Main function execution '''
if __name__ == '__main__':
    main()
