""" Jaldh Logger

Goal : to log with timestamps into a file.

"""
import datetime
import os

import cyboidef


# Global module variables
logfile = "jaldh.log"
logbuf = []
bufcount:int = 0
bufsize:int = 1

def logIt(logstr:str) -> None:
    """ Log a message to buffer with a timestamp.
    Args:
        logstr (str): Text to log.
    """
    global bufcount
    global bufsize
    global logbuf
    tmpstr = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "  " + logstr + "\n"
    logbuf.append(tmpstr)
    bufcount += 1
    if bufcount>=bufsize:
        log2File()


def log2File() -> None:
    """ Just a file logger, writes the buffer to file and clears it
    Args: None
    Returns: None
    """
    global logbuf
    global bufcount
    global logfile
    try:
        with open(logfile, "a+") as fh:
            # write the buffer to file
            fh.writelines(logbuf)
            logbuf.clear()  # Clear the buffer after writing
            bufcount = 0
    except Exception as e:
        print(f"Error while logging to file: {e}")


def remlogfile() -> None:
    """ Deletes the logfile. """
    global logfile
    if os.path.exists(logfile):
        os.remove(logfile)