import subprocess
import sys
import os 
import re
from pathlib import Path
from enum import Enum

class Color(Enum):
    GREEN = '\033[92m'
    BOLD = '\033[1m'
    RED = '\033[91m'
    END = '\033[0m'

class FileTypeError(Exception):
    '''
    Must provide python script.
    '''
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return (repr(self.value))

def install(package, failed, version=None):
    try:
        if version:
            status = subprocess.check_output([sys.executable, "-m", "pip", "install", package + "==" + version], stderr=subprocess.STDOUT)
        else:
            status = subprocess.check_output([sys.executable, "-m", "pip", "install", package], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        error = e.output.decode("utf-8").lstrip()
        tmp = {package: error}
        failed.append(tmp)
    else:
        print(package, Color.GREEN.value + status.decode("utf-8") + Color.END.value)

def read_script(script):
    failed = []

    print(Color.BOLD.value + '-> {0}'.format(script) + Color.END.value)

    with open(script, 'r') as r:
        line = r.readline()
        version = None
        while line != '':
            if 'import' in line or 'from' in line:
                if '#' in line:
                    try:
                        version = re.search('#(.+?)\n', line).group(1)
                    except AttributeError:
                        pass
                    else:
                        line = re.search('(.+?)#', line).group(1)
                _line = line.split('import') if 'import' in line else line.split('format')
                install(_line[1].lstrip(), failed, version)
                version = None
            '''
            for terms in line_starters:
                if terms in line:
                    sys.exit(0)
            '''
            line = r.readline()

    if len(failed) > 0:
        print("Packages failed to install: ")
        border = ["-" for i in range(0,35)]
        for stars in border:
                print(stars, end='')
        print()
        for row in failed:
            for key,items in row.items():
                print(Color.BOLD.value + key + Color.END.value)
                print(Color.RED.value + items + Color.END.value)
                
def main(argv):
   for script in argv:
        ext = script.split('.')
        try:
            if ext[len(ext)-1] != 'py':
                raise(FileTypeError("Invalid extension"))
        except FileTypeError as error:
            print("FileTypeError Exception: {}".format(error.value))
        else:
            #if script in current path
            curr_dir = os.getcwd() + "/"
            file_path = Path(curr_dir + script)
            if not file_path.is_file():
                #if script in provided absolute path
                file_path_abs = Path(script)
                try:
                    file_path_abs_exists = file_path_abs.resolve(strict=True) 
                except FileNotFoundError as e:
                    raise(e)
                else:
                    file_path = script
            else:
                file_path = curr_dir + script
            read_script(script)
        
if __name__=="__main__":
    main(sys.argv[1:])