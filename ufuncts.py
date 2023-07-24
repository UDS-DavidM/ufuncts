import os
import math
import re
from time import perf_counter, process_time

sep = os.sep
timer = perf_counter

version = 4
vdate = "160423"
ctime = None

default_encoding = "UTF-8"

def printl(L, lim=0):
    """ Print a list into the terminal line-by-line, up to a defined limit."""
    if lim > 0: L = L[:0]
    for m in L: print(m)
        
def printd(D, lim=0):
    """ Print a dict into the terminal line-by-line, up to a defined limit."""
    for i, m in enumerate(D):
        print(m,"\t",D[m])
        if lim > 0 and i >= lim:
            break
        
def formatNum(num, separator=","):
    return (("{:"+separator+"}").format(num))

def minmax(_min, _max, val):
    """ Truncates input value between min and max value. """
    return min(_max, max(_min, val))

truncate = minmax

def argmax(d):
    """ Returns the key witht the highest value in the given dictionary. """
    return max(d, key=d.get)

def argmin(d):
    """ Returns the key witht the lowest value in the given dictionary. """
    return min(d, key=d.get)

def avg(L, r=None):
    """ Returns average of a list of numerals. """
    res = sum(L) / max(1, len(L))
    if r: res = round(res, r)
    return res

average = avg
mean = avg

def get_mag(x):
    """ Return base-1024 integer magnitude of a number. """
    return int(math.log(x, 1024)) if x > 0 else 0

def fileslist(path, sort=False, sortkey=None):
    """ Walk given path and return a list of all files within that directory, or None if path is invalid. """
    resultlist = []
    if not os.path.isdir(path): return
    for walk in os.walk(path):
        resultlist.extend(walk[2])
        break
    return sorted(resultlist, key=sortkey) if sort else resultlist

def subfileslist(path, sort=True):
    """ Returns the full path of all files in specified directory, including subdirectories. """
    fileslist = list()
    for subdir in os.walk(path):
        path = subdir[0]
        for fn in subdir[2]:
            fileslist.append(path+sep+fn)
    return sorted(fileslist, key=lambda s: s.split(sep)[-1].lower()) if sort else fileslist

#incomplete, do not use
def generate_file_structure(destination, seek_directory, flist=None):
    """ In the directory name given by <destination> and a list of file paths with nested directory structure originating from a common <seek_directory>, recreate the same directory structure. """
    if flist is None:
        flist = subfileslist(seek_directory)
    if not destination.endswith(sep):
        destination += sep
    outputfileslist = [destination+x.replace(seek_directory, "") for x in fileslist]
    if not os.path.exists(destination):
        os.mkdir(destination)
    for outputfile in outputfileslist: #recreate folder structure in output directory
        fullpath = os.path.dirname(outputfile).split(sep)
        partial_path = []
        for subdir in fullpath:
            partial_path.append(subdir)
            nsubdir = sep.join(partial_path)
            if not os.path.exists(nsubdir):
                os.mkdir(nsubdir)
                
def construct_path(path, sep=sep):
        """ Constructs a full directory path, if it doesn't already exist. """
        if os.path.isdir(path): return
        partial = [x for x in path.strip().split(sep) if x]
        subpath = ""
        for directory in partial:
            subpath += directory + sep
            if not os.path.isdir(subpath): os.mkdir(subpath)
                
def runpy(filepath):
    """ Read and execute given Python program in current environment. """
    if not filepath.endswith(".py") and not filepath.endswith(".pyw"):
        filepath += ".py"
    exec(open(filepath).read())

def reset_time():
    """ Re-initialize timer and set timediff to current point. """
    global ctime
    ctime = None
    track_time()

def track_time(get=False, limit=4):
    """ Calculates time passed since last function call, initializes timer otherwise.
         output: print value to console
         get: return value
    """
    global ctime
    now = timer()
    if not ctime:
        ctime = now
        return
    time = timer() - ctime
    ctime = now
    if limit > 0: time = round(time, limit)
    if get:
        return time
    else:
        print("Time since last call: %s" % str(time))
        
def calc_bytes(b):
    """For a given number of bytes, return a string representing its colloquial expression, rounded to 2 minor digits."""
    suffix = " bytes"
    kb = 1024
    mb = 1024**2
    gb = 1024**3
    if b > gb: suffix = " Gbytes"; b /= gb
    elif b > mb: suffix = " Mbytes"; b /= mb
    elif b > kb: suffix = " Kbytes"; b /= kb
    return str(round(b,2))+suffix
    
def bench(fun, n=1):
    """ Quickly determine the runtime of a function. """
    from timeit import timeit
    return timeit(fun, globals=globals(), number=n)

def default(val, _default):
    """ Returns val if it is a True-like value, otherwise default."""
    try:
        return val if val else _default
    except:
        return _default

def concat(L, R) -> list:
    """ Returns the concatenation of two list-like objects. """
    return [*L, *R]

def combine(LD, RD) -> dict:
    """ Returns the combination of two dictionaries. When identical keys are contained, the second dictionary is given priority. """
    return {**LD, **RD}
        
def print_self():
    """ Print code of the currently active file to the console. """
    with open(__file__, "r") as this:
        for line in this:
            print(line,end="")
    print("\n")
    
def excerpt(inlist, size=10, asdict=False):
    """ Returns a random sample of items from a list-like of given size. Returns: list, dict (if enabled), or single item if size == 1."""
    from random import sample
    res = sample(list(inlist), min(size, len(inlist)))
    if asdict and isinstance(inlist, dict):
        return {entry:inlist[entry] for entry in res}
    return res[0] if size == 1 else res
    
def basename(filename): #note: this is much faster than os.path.basename
    """ Turn a path to a file into the corresponding basic filename. """
    if sep in filename: return filename.split(sep)[-1]
    elif '/' in filename: return filename.split('/')[-1]
    return filename

def basenames(fileslist):
    return [basename(x) for x in fileslist]

def extension(filename):
    """ Returns the extension/file type of a file. """
    if not "." in filename: return None
    return filename.split(".")[-1]

def split_ext(filename):
    """ Returns tuple of (basename, extensions*) """
    filename = basename(filename)
    if not "." in filename: return tuple()
    return filename.split(".")
    
def match_pattern(x, M:list, default=None):
    for pat, res in list(M):
        if x == pat:
            return res
    return default

def readf(file, mode="r"):
    """ Open a file, read its contents and return them, then close the file. """
    with open(file, mode) as infile:
        data = infile.read()
    return data

def atoi(text):
    """ Helper function. Return input as number if it is a number-like, otherwise return input. """
    return int(text) if text.isdigit() else text

def natural_key(text):
    """ Sorting key function. Sort a list by its natural ordering, i.e. alpha first, ordered numbers second. """
    return [atoi(c.lower()) for c in re.split('(\d+)',text)]

def natural_sort(L, **kwargs):
    """ Sort a list by its natural ordering, i.e. alpha first, ordered numbers second. """
    return sorted(L, key=natural_key, **kwargs)

canon_sort = canonical_sort = natural_sort

def safe_overwrite(filename, data, mode="w", encoding=default_encoding, temp_extension=".temp", verbose=True):
    """ Write data into a temp file and verify before overwriting original file. """
    #wip - untested
    filename = filename.strip()
    temp_extension = temp_extension.strip()
    encoding = None if "b" in mode else encoding
    if not temp_extension.startswith("."):
        temp_extension = "." + temp_extension
    temp_filename = filename + temp_extension
    try:
        stage = 1
        with open(temp_filename, mode, encoding=encoding) as tempfile:
            tempfile.write(data)
        stage = 2
        if os.path.exists(filename):
            os.unlink(filename)
        stage = 3
        os.rename(temp_filename, filename)
        stage = 4
    except Exception as e:
        if verbose:
            print(f"Warning: Stage {stage} error when writing file {filename}.\n", e)
        if os.path.exists(tempfile): os.unlink(tempfile)
        
def _install():
    """ Install itself into main python directory, enabling global use. """
    import sys, os
    main_dir = os.path.dirname(sys.executable) + os.sep + "Lib" + os.sep + basename(__file__)
    choice = "y"
    if os.path.exists(main_dir):
        choice = input("%s\nalready exists. Overwrite? (Y/N)\n>>> " % main_dir).lower()
    if choice in ["y","yes","ok"]:
        with open(main_dir,"w") as newfile:
            with open(__file__, "r") as this:
                for line in this:
                    newfile.write(line)
        print("%s has been successfully installed to\n%s" % (__file__, main_dir))
    else:
        print("Aborted.")