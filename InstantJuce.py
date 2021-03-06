#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

import sys, time, logging, os, subprocess, signal, time
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

timestamp = datetime(1970, 1, 1)
pro = None

class EventHandler(LoggingEventHandler):
    def dispatch(self, event):
        filename, extension = os.path.splitext(event.src_path)
        print("Changes made to file: " + filename + extension)

        global timestamp

        time_difference = (datetime.now() - timestamp).total_seconds()
        print("Time difference: " + str(time_difference))

        if os.path.basename(filename) == "Context" and extension == ".h" and time_difference > 5.0:
            timestamp = datetime.now()
            print("Recompiling")
            build()
            print("Run")
            stop()
            start()

def build():
    subprocess.call("xcodebuild -project bin/InstantJuce/Builds/MacOSX/Runtime.xcodeproj -scheme \"Runtime - ConsoleApp\" -configuration Debug -sdk macosx -jobs 8", shell=True)

def start():
    global pro
    # The os.setsid() is passed in the argument preexec_fn so
    # it's run after the fork() and before  exec() to run the shell.
    cmd = "./bin/InstantJuce/Builds/MacOSX/build/Debug/Runtime"
    pro = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                           shell=True, preexec_fn=os.setsid) 

def stop():
    global pro

    if pro is not None:
        os.killpg(os.getpgid(pro.pid), signal.SIGTERM)  # Send the signal to all the process groups
        pro = None

if __name__ == "__main__":

    jucePathFile = ".jucepath"

    # Get path to user's JUCE installation
    if not os.path.exists(jucePathFile):
        with open(jucePathFile, 'w') as fp: 
            path = input("Enter path to Projucer.app: ")
            path = path.strip()
            print(path)
            if not os.path.isdir(path):
                print("Error: Path does not exist. Exiting")
                os.stat(path)
                os.remove(jucePathFile)
                exit()

            fp.write(path)
    
    # Read stored Projucer.app path 
    projucerPath = ""
    with open(jucePathFile, 'r') as file:
        projucerPath = file.read().replace('\n', '')

    print("Projucer.app installed at: ", projucerPath)
    
    # Check if Projucer is found
    projucerBinaryPath = os.path.join(projucerPath, "Contents", "MacOS", "Projucer")
    
    print("Looking for Projucer binary at: ", projucerBinaryPath)

    if not os.path.exists(projucerBinaryPath):
        print("Error: Projucer binary not found. Exiting")
        os.remove(jucePathFile)
        exit()

    # Generate Xcode Project
    print("Generating Xcode project")
    cmd = projucerBinaryPath + " --resave bin/InstantJuce/Runtime.jucer"
    print(cmd)
    subprocess.call(cmd, shell=True)

    build()
    start()

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = EventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()

        stop()