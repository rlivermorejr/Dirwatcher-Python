import logging
import time
import signal
import argparse
import os
import sys

__author__ = """Russell Livermore"""

start_time = time.time()
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s:%(msecs)d %(name)s %(levelname)s \
                        %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)
starting_banner = ('\n' + '-' * 70 + '\n' +
                   f"\n\tDirwatcher.py started at {time.ctime()}"
                   + '\n\n' + '-' * 70 + '\n')

exit_flag = False
previous_files = {}


def search_for_magic(file_dict, magic_string):
    """Searches the files that get passed in from the watch_directory
    along with the magic_string. If the magic string is in one of the files
    it will log to the terminal."""
    for k, v in file_dict.items():
        with open(k) as f:
            lines = f.readlines()
        for e, line in enumerate(lines):
            if e >= v:
                if magic_string in line:
                    logger.info(
                        f"""Magic String: \"{magic_string}\"
                        found in {k} at line {e+1}""")
                    previous_files[k] += 1
    return


def check_added_files(old_dict, new_dict):
    """Checks dictonary for any files added"""
    new_files = []
    for x in new_dict.keys():
        if x not in old_dict:
            new_files.append(x)
    return new_files


def check_deleted_files(old_dict, new_dict):
    """Checks dictonary for any files deleted"""
    deleted_files = []
    for x in old_dict.keys():
        if x not in new_dict:
            deleted_files.append(x)
    return deleted_files


def search_for_files(path, extension):
    """Searches the directory that was passed in from the
    watch_directory function for files with correct extension"""
    files_dict = {}
    for x in os.listdir(path):
        if not extension and os.path.join(path, x) not in files_dict:
            files_dict[os.path.join(path, x)] = 0
        elif (os.path.splitext(x)[1][1:] == extension
              and os.path.join(path, x) not in files_dict):
            files_dict[os.path.join(path, x)] = 0
    return files_dict


def watch_directory(path, magic_string, extension):
    """Takes arguments from __main__ and passes them to other
    functions. Will log the output from added/deleted files function
    and essentially acts as a main function for the search and check functions"""
    global previous_file
    file_dict = search_for_files(os.path.abspath(path), extension)
    added_files = check_added_files(previous_files, file_dict)
    for x in added_files:
        logger.info(f'File {x} added')
        previous_files[x] = 0
    deleted_files = check_deleted_files(previous_files, file_dict)
    for x in deleted_files:
        logger.info(f'File {x} deleted')
        del previous_files[x]
    search_for_magic(previous_files, magic_string)
    return


def create_parser():
    """Creates and argument parser object"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--interval',
                        help='controls the polling interval',
                        type=int, nargs='?', const=1)
    parser.add_argument('-d', '--todir',
                        help='the directory to search in')
    parser.add_argument('-t', '--text',
                        help='the text to search for')
    parser.add_argument('-e', '--extension',
                        help='the extension of the file to search')
    return parser


def get_uptime():
    """Calculates the runtime of program and returns
    it in a readable clock format HH:MM:SS"""
    uptime = time.time() - start_time
    hrs = uptime // 3600 % 24
    minutes = uptime // 60 % 60
    seconds = uptime // 1 % 60
    return f"{int(hrs)}:{int(minutes)}:{int(seconds)}"


def signal_handler(sig_num, frame):
    """Handles SIGTERM/SIGINT signals and logs the program runtime
    from the get_uptime function."""
    logger.warning(f'Received {signal.Signals(sig_num).name}')
    logger.info('\n' + '-' * 70 + '\n' + '\tStopped Dirwatcher.py'
                f"""\n\tUptime: {get_uptime()}""" +
                '\n\n' + '-' * 70 + '\n')
    raise SystemExit()


def main(args):
    """Main function that starts off the loop by passing
    parser args to the watch_directory function"""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    ns = parser.parse_args(args)
    logger.info(starting_banner)
    message = 'Missing arguments!'
    if ns.todir == None:
        print('Missing a directory to look in!')
        sys.exit(1)
    if ns.text == None:
        print('Missing text argument!')
        sys.exit(1)
    if ns.extension == None:
        print('Missing extension argument!')
        sys.exit(1)
    while not exit_flag:
        try:
            watch_directory(ns.todir,
                            ns.text,
                            ns.extension)
        except Exception:
            logger.error(
                f"Directory {ns.todir} does not exist\n'ctrl + c' to quit")
        try:
            time.sleep(ns.interval)
        except TypeError:
            time.sleep(1)
    return


if __name__ == '__main__':
    main(sys.argv[1:])
