import os
import math
import re
import sys
from time import perf_counter, process_time
from contextlib import contextmanager

sep = os.sep
timer = perf_counter

version = 7
revision = 4
vdate = "260425"
ctime = None
versionstring = "ufuncts v"+str(version)+"-"+vdate+"R"+str(revision)

default_encoding = "UTF-8"
listlikes = (list, set, tuple, frozenset)

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
        
def printr(s:str) -> str:
    """ Print string as an r-string, which will render escape sequences canonically. """
    print(r""+s)
        
def raws(s:object):
    """ Returns the raw (canonical) representation of a string or obj, including escape characters. """
    if isinstance(s, str):
        return repr(s)[1:-1]
    return repr(s)
        
def formatNum(num, separator=","):
    """ Transform a number into it's colloquial string representation including a separator. """
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

def get_mag(x, base=1024):
    """ Return base integer magnitude of a number. """
    return int(math.log(x, base)) if x > 0 else 0

def strbool(v:str)->bool:
    """ If v is empty or a false-like string, return False, otherwise True. """
    return not v or v not in {"False","0"}

def fileslist(path, aspath=True, sort=False, sortkey=None):
    """ Walk given path and return a list of all files within that directory, or None if path is invalid. """
    path = os.path.normpath(path)
    resultlist = []
    if not os.path.isdir(path): return
    for walk in os.walk(path):
        resultlist.extend(walk[2])
        break
    if aspath:
        path = path.rstrip(sep)
        resultlist = [path + sep + fn for fn in resultlist]
    return sorted(resultlist, key=sortkey) if sort else resultlist

def subfileslist(path, sort=True):
    """ Returns the full path of all files in specified directory, including subdirectories. """
    path = os.path.normpath(path)
    fileslist = list()
    for subdir in os.walk(path):
        path = subdir[0]
        for fn in subdir[2]:
            fileslist.append(path+sep+fn)
    return sorted(fileslist, key=lambda s: s.split(sep)[-1].lower()) if sort else fileslist

def generate_file_structure(destination, seek_directory, flist=None):
    """ In the directory name given by <destination> and a list of file paths with nested directory structure originating from a common <seek_directory>, recreate the same directory structure. """
    #incomplete; incorporate os.mkdirs instead
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
        
def construct_path(path, mode=511):
    """ Constructs a full directory path, including subpaths. Does nothing if path already exists. """
    os.makedirs(path, mode=mode, exist_ok=True)
                
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
        
def calc_bytes(b, suffixes=(" bytes"," Kbytes"," Mbytes"," Gbytes", " Tbytes"), base=1024):
    """For a given number of bytes, return a string representing its colloquial expression, rounded to 2 minor digits."""
    if not b: return str(0)+suffixes[0]
    mag = int(math.log(b, base))
    mag = min(mag, len(suffixes)-1)
    b /= base**mag
    suffix = suffixes[mag]
    return str(round(b,2))+suffix
    
def bench(fun, n=1):
    """ Quickly determine the runtime of a function. """
    from timeit import timeit
    return timeit(fun, globals=globals(), number=n)

def default(val, _default):
    """ Returns val if it is a True-like value, otherwise default."""
    try: return val if val else _default
    except Exception: return _default
    
def peek(data, i, lookahead=1, default=None, back=False):
    """ Simple lookahead. Returns the next element from a given index <i>, or <default=None> if there is no next element."""
    try: return data[i-lookahead] if back else data[i+lookahead]
    except Exception: return default
    
lookahead = peek

def concat(L, R) -> list:
    """ Returns the concatenation of two list-like objects. """
    return [*L, *R]

def combine(LD, RD) -> dict:
    """ Returns the combination of two dictionaries. When identical keys are contained, the second dictionary is given priority. """
    return {**LD, **RD}

def intersect(L, R) -> list:
    """ Returns the intersection (common elements) of two list-like objects. """
    Lx, Rx = list(L), set(R)
    return [x for x in Lx if x in Rx]

def flatten(L) -> list:
    """ Returns flattened (un-nested) version of a list-like object. """
    if is_listlike(L):
        return [item for sub in L for item in flatten(sub)]
    else:
        return [L]
        
def print_self():
    """ Print code of the currently active file to the console. """
    with open(__file__, "r", encoding=default_encoding) as this:
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
    """ Turn a path to a file into the corresponding basic filename. Returns input as-is if no path separator is found. """
    if sep in filename: return filename.split(sep)[-1]
    elif '/' in filename: return filename.split('/')[-1]
    return filename

def basenames(fileslist):
    """ Apply ufuncts.basename to a list of inputs. """
    return [basename(x) for x in fileslist]

def extension(filename, lower=True, dot=False):
    """ Returns the extension/file type of a file. """
    if not "." in filename: return None
    res = filename.split(".")[-1].lower() if lower else filename.split(".")[-1]
    if dot: res = "." + res
    return res

def split_ext(filename):
    """ Returns tuple of (basename, extensions*) """
    filename = basename(filename)
    if not "." in filename: return (filename, "")
    return filename.split(".")
    
def match_pattern(x, M:list, default=None):
    for pat, res in list(M):
        if x == pat:
            return res
    return default

def readf(file, mode="r", encoding=default_encoding, split=True, strip=True, condense=False, splitter="\n"):
    """ Open a file, read its contents and return them, then close the file. """
    with open(file, mode, encoding=encoding) as infile:
        if not split:
            return infile.read()
        else:
            if strip and not condense:
                data = []
                for line in infile:
                    data.append(line.strip())
                return data
            if not strip and not condense:
                return infile.readlines()
            if strip and condense:
                data = []
                for line in infile:
                    line = line.strip()
                    if line: data.append(line)
                return data
            if not strip and condense:
                data = []
                for line in infile:
                    if line.strip(): data.append(line)
                return data
            
def writef(data, file, mode="a", encoding=default_encoding, strip=True, raw=False, flush=False):
    """ Open a file, write a line or multiple lines of data, then close it.
        data: string or list of input data
        file: filename or path
        strip: strip starting and trailing whitespaces
        raw: Write strings as-is (including escape characters).    
    """
    if isinstance(data, str):
        data = [data]
    with open(file, mode, encoding=encoding) as outfile:
        for line in data:
            if strip: line = line.strip()
            if raw: line = raws(line)
            outfile.write(line)
            outfile.write("\n")
        if flush:
            outfile.flush()

def atoi(text):
    """ Helper function. Return input as number if it is a number-like, otherwise return input. """
    return int(text) if text.isdigit() else text

def natural_key(text):
    """ Sorting key function. Sort a list by its natural ordering, i.e. alpha first, ordered numbers second. """
    return [atoi(c.lower()) for c in re.split(r'(\d+)',text)]

def natural_sort(L, **kwargs):
    """ Sort a list by its natural ordering, i.e. alpha first, ordered numbers second. """
    return sorted(L, key=natural_key, **kwargs)

canon_sort = canonical_sort = natural_sort

def get_duplicates(array, set_test=True):
    """ Efficiently retrieve duplicate items from an input array. Returns set of items with >1 occurences. """
    res = set()
    #set_test - set this if you expect no duplicates for most inputs
    if set_test and (isinstance(array, set) or isinstance(array, dict) or len(set(array)) == len(array)): return res
    seen = set()
    for item in array:
        if item in seen: res.add(item)
        else: seen.add(item)
    return res

def map(array, func):
    """ Given a function and input array, return list where the function has been applied to each item in the array. """
    return [func(i) for i in array]

def fold(array, func):
    """ Fold the array using func, where func is a function of the shape f(a,b)=c. """
    try: acc = array.pop(0)
    except: return []
    for item in array:
        acc = func(acc, item)
    return acc    

def is_listlike(item):
    """ Returns true if item is an iterable non-string object, false otherwise. """
    return hasattr(item, "__iter__") and not isinstance(item, str)

#tbd: test with binary data
def safe_write(filename, data, mode="w", encoding=default_encoding, temp_extension=".temp", cast_str=True, sep="\n", keep_temp=False, verbose=True):
    """ Write data into a temp file and verify contents before replacing original file.
        Data can be a list-like -each item representing a line-, a string, or binary data.
        cast_str (True): Cast all items to str before writing. If set to False, may fail if encountering non-string types in list.
        sep ('\\n'): Append separator character at the end of each item.
        keep_temp (False): Do not delete the temporary file in case of failure.
        verbose (True): Print debug information to stdout.
    """
    filename = filename.strip()
    temp_extension = temp_extension.strip()
    encoding = None if "b" in mode else encoding
    if not temp_extension.startswith("."):
        temp_extension = "." + temp_extension
    temp_filename = filename + temp_extension
    try:
        stage = 1
        with open(temp_filename, mode, encoding=encoding) as tempfile:
            if "b" in mode or not is_listlike(data):
                tempfile.write(data)
            else: #is listlike                   
                for item in data:
                    if cast_str and not isinstance(item, str): item = str(item)
                    if sep and not item.endswith(sep): item += sep
                    tempfile.write(item)
        #print(temp_filename) ###testing
        stage = 2
        os.replace(temp_filename, filename)
        stage = 3
        return True
    except Exception as e:
        if verbose:
            print(f"Warning: Stage {stage} error when writing file {filename}.\n", e, file=sys.stderr)
        if os.path.exists(temp_filename) and not keep_temp: os.unlink(temp_filename)
        return False
        
def _install():
    """ Install itself into main python directory, enabling global use. """
    import sys
    main_dir = os.path.dirname(sys.executable) + os.sep + "Lib" + os.sep + basename(__file__)
    choice = "y"
    if os.path.exists(main_dir):
        choice = input("%s\nalready exists. Overwrite? (Y/N)\n>>> " % main_dir).lower()
    if choice in ["y","yes","ok"]:
        with open(main_dir, "w", encoding=default_encoding) as newfile:
            with open(__file__, "r", encoding=default_encoding) as this:
                for line in this:
                    newfile.write(line)
        print("%s has been successfully installed to\n%s" % (versionstring, main_dir))
    else:
        print("Aborted.")