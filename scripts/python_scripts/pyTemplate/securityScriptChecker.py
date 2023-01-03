'''
    @name
        securityScriptChecker.py
    
    @description
        Script is for comparing config file with script contents if all 
        variables used in script are declared in config file.
        Reason for that is to avoid eg. rm -rf ${DIR}/*

        Function can be used individually or as a part of pyScriptTemplate.
        Set interactive flag up to your preferences.

    @parameters
        1) --config Name of config file with variables declarations
        2) --script Name of script which you want to verify

    @date
        25-mar-2021

    @author
        Maciej Ferszt

    @version
        0.1v
'''

''' Import Section '''
import os, sys, pathlib, re, subprocess, argparse

''' Argument parser '''
def argParse():
    scriptChecker = argparse.ArgumentParser(description=sys.modules[__name__].__doc__,
                                            formatter_class=argparse.RawDescriptionHelpFormatter)

    scriptChecker.add_argument('--script',
                            '-s',
                            required=True,
                            action='store',
                            help='Script name which should be in the same directory')
                
    scriptChecker.add_argument('--config',
                            '-c',
                            required=True,
                            action='store',
                            help='Config file name which should be in the same directory')

    scriptChecker.add_argument('--interactive', 
                            '-i',
                            action='store_true',
                            dest='interactive',
                            help='Set script into interactive mode')

    scriptChecker.add_argument('--non-interactive', 
                            '-ni',
                            action='store_false',
                            dest='interactive',
                            help='Set script into non-interactive mode')

    scriptChecker.set_defaults(interactive=True)

    return scriptChecker.parse_args()

'''
    @function
        readVariablesFromConfig()

    @description
        Function takes config file as a parameter.
        Parses contents and saves all variables to variablesList.
'''
def readVariablesFromConfig(configFile):
    variablesList = []
    with open(configFile) as f:
        content = [line.strip() for line in f]

    # Remove all headers
    for line in content:
        if line.endswith(']'):
            content.remove(line)
        
    # Remove empty strings
    content = [i for i in content if i]

    # Save variables names before = sign eq. variable = value
    for index, line in enumerate(content):
        variablesList.append(line.split('=')[0].strip())

    return variablesList

'''
    @function
        readVariablesFromScript()

    @description
        Function takes script as a parameter.
        Parses contents and saves all variables to variablesList.
'''
def readVariablesFromScript(scriptFile):
    variablesList = []
    with open(scriptFile) as f:
        content = [line.rstrip() for line in f]

    # Iterate through lines and look for all occurences of ${variable}
    for line in content:
        regexResult = re.findall('\${(.+?)}', line)
        if regexResult:
            for index, occurence in enumerate(regexResult):
                variablesList.append(regexResult[index])

    return variablesList

'''
    @function
        main()

    @description
        Main function of the script, runs parsing functions for config and script files and compares them.
        Depending on compare result and interactive mode it might prompt user to decide if proceed with errors.
'''
def main():
    ''' Execute parse_args() '''
    args = argParse()

    configFilePath = os.path.join(pathlib.Path(__file__).parent, args.config)
    scriptFilePath = os.path.join(pathlib.Path(__file__).parent, args.script)

    configFileContent = readVariablesFromConfig(configFilePath)
    scriptFileContent = readVariablesFromScript(scriptFilePath)

    # Check if list configFileContent contains every element from scriptFileContent
    variablesCheck =  all(item in configFileContent for item in scriptFileContent)

    if variablesCheck:
        print('Good, your script is safe to run and doesnt contain any not declraed variables!')
        sys.exit(variablesCheck)
    else:
        print('Whoops, your script contains not declraed variables, this might result in some mistakes!')
        print('You can continue at your own risk!')
        if args.interactive:
            while True:
                ans = str(input('Continue?'))
                if not ans.lower() in ('y', 'n'):
                    print("Answer should be y or n")
                    continue
                else:
                    break
            
            if ans == 'y':
                variablesCheck = True
                sys.exit(variablesCheck)
            if ans == 'n':
                sys.exit(variablesCheck)
        else:
            sys.exit(variablesCheck)

''' Main function execution '''
if __name__ == '__main__':
    main()
