#import os
import platform

def check_os():
        if platform.system() == 'Linux':
                #print('linux')
                return 'linux'
	
        elif platform.system() == 'Windows':
                #print('windows')
                return 'windows'
	
        else:
                #print('0')
                return 0
