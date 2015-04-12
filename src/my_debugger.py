'''
Created on Feb 21, 2015

@author: A
'''

from ctypes import *
from my_debugger_defines import *
from _msi import PID_APPNAME

kernel32 = windll.kernel32

class debugger():
    def __init__(self):
        pass
    
    def load(self, path_to_exe):
        
        # dwCreation flag determines how to create the Process
        # set the creation_flags = CREATE_NEW_CONSOLE if you WANT THE GUI
        
        creation_flags = DEBUG_PROCESS
        # creation_flags = CREATE_NEW_CONSOLE # for the GUI
        
        
        # instantiate structs for the Process
        startupinfo = STARTUPINFO()
        process_information = PROCESS_INFORMATION()
        
        
        # the next two flags let us see the process in a separte window. illustrates how the settings
        # in the startup info can affect the debuggee (whatever it is we're exploring)
        
        startupinfo.dwFlags = 0x1
        startupinfo.wShowWindow = 0x0
        
        
        # instantiate the cb variable, in the STARTUPINFO struct, gives SIZE
        
        startupinfo.cb = sizeof(startupinfo)
        
        
        if kernel32.CreateProcessA(path_to_exe,
                                   None,
                                   None,
                                   None,
                                   None,
                                   creation_flags,
                                   None,
                                   None,
                                   byref(startupinfo),
                                   byref(process_information)):
            print "[*] We have successfully launched the process!"
            print "[*] PID %d" % process_information.dwProcessID
            
        else:
            print "[*] Error: 0x%o8x." % kernel32.GetLastError()
    
    def open_process(self, pid):
        h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, pid, False)
        return h_process
    
    def attach(self, pid):
        self.h_process = self.open_process(pid)
        # attempt to attach the process, and if it fails, exit the call to the Process
        
        if kernel32.DebugActiveProcess(pid):
            self.debugger_active = True
            self.pid = int(pid)
            self.run()
        else:
            print "[*] Unable to attach to the process"
            
    def run(self):
        # polling the debuggee for debugging events
        while self.debugger_active == True:
            self.get_debug_event()
            
    def get_debug_event(self):
        debug_event = DEBUG_EVENT()
        continue_status = DBG_CONTINUE
        
        if kernel32.WaitForDebugEvent(byref(debug_event), INFINITE):
            #no event handlers yet here, just resuming process after printing
            raw_input("Press a key to continue... ")
            self.debugger_active = False
            kernel32.ContinueDebugEvent(\
                                        debug_event.dwProcessId,\
                                        debug_event.dwThreadId, \
                                        continue_status)
            
    
    def detach(self):
        if kernel32.DebugActiveProcessStop(self.pid):
            print "[*] Finished debugging. Exiting ..... "
            return True
        else:
            print "There was a problem yo"
            return False