__author__ = 'fuzzynop'

import os
import sys


apps = os.listdir('/Applications/')
app_choices = []
target_app = ''
dialog1 = ''
predefine_osa = ['''osascript -e 'tell app "System Preferences" to display dialog "System Preferences requires your password to finish applying updates." & return & return  default answer "" with icon 1 with hidden answer' ''']

def get_terminal_size(fd=1):
    """
    Returns height and width of current terminal. First tries to get
    size via termios.TIOCGWINSZ, then from environment. Defaults to 25
    lines x 80 columns if both methods fail.

    :param fd: file descriptor (default: 1=stdout)
    """
    try:
        import fcntl, termios, struct
        hw = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
    except:
        try:
            hw = (os.environ['LINES'], os.environ['COLUMNS'])
        except:
            hw = (25, 80)

    return hw

def get_terminal_height(fd=1):
    """
    Returns height of terminal if it is a tty, 999 otherwise

    :param fd: file descriptor (default: 1=stdout)
    """
    if os.isatty(fd):
        height = get_terminal_size(fd)[0]
    else:
        height = 999

    return height

def menu(input='nothing',stage='0'):
    #STAGE 0
    if input == "nothing" and stage=='0':
        print "[1]: Define Application."
        print "[2]: Pick Local Application from /Applications/."
        print "[3]: Use predefined script."
        choice = raw_input(">> ")
        menu(choice,stage="1")
    #####################################################################
    #STAGE 1
    #####################################################################
    th = get_terminal_height()-3
    if input == "1" and stage=="1":
        print "--Enter Application name--"
        target_app = raw_input(">> ")
        menu(target_app,"2")
    elif input == "2" and stage=="1":
        for app in apps:
            if "app" in app:
                app_choices.append(app.split('.app')[0])
        for i in range(0,len(app_choices)-1):
            if i < th:
                print '['+str(i)+']: '+app_choices[i]
            elif i == th:
                print '['+str(i)+']: '+app_choices[i]
                print "--Enter Number or press enter to see more--"
                con = raw_input(">> ")
                if con == '':
                    pass
                else:
                    app_choice = con
                    break
            if i > th:
                print '['+str(i)+']: '+app_choices[i]
                con = raw_input(">> ")
                if con == '':
                    pass
                else:
                    app_choice = con
                    break
        while con=='':
            print "--Enter Number for app you would like to target--"
            con = raw_input('>> ')
        try:
            app_choice = int(con)
            target_app = app_choices[app_choice]
            menu(target_app,"2")
        except:
            print "Invalid Entry."
            sys.exit(1)
        ###################################################################
        #Stage 2
        ############# put the osa script togehter more
    elif input=="3" and stage=="1":
        for i in range(0,len(predefine_osa)-1):
            print '['+i+']'+predefine_osa[i]
        print '--Enter number for osascript you want to use--'
        choice = raw_input('>> ')
        try:
            print predefine_osa[choice]
            os.system("echo "+predefine_osa[choice])
        except:
            print "Error"
    elif stage=="2":
        print "--Enter text you want to prompt the user with, press enter for a generic prompt--"
        dialog1 = raw_input(">> ")
        if dialog1=='':
            dialog1=input+' requires your password to continue.'
        print "--Enter the text you want for the dialog box title, press enter for a generic title--"
        title = raw_input(">> ")
        if title=='':
            title=input+' Alert'
        osascript1 = '''osascript -e 'tell app "'''+input+'''" to activate' -e 'tell app "'''+input+'''" to activate' -e 'tell app "'''+input+'''" to display dialog "'''+dialog1+'''" & return & return  default answer "" with icon 1 with hidden answer with title "'''+title+'''"\''''
        print osascript1
        f = open('tmposascript','w')
        f.write(osascript1)
        f.close()
        os.system('''cat tmposascript |pbcopy''')
        os.system('rm tmposascript')




menu()