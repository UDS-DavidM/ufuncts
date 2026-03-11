**ufuncts** (Universal Functions) is a set of frequently used functions that I found useful for general tasks. It is a lightweight, single-file, pure Python module with no external dependencies.

It bundles a collection of tools for:
- printing and debugging
- string manipulation
- mathematical helpers
- reading and writing files in a single line
- quick benchmarking and timing

Feedback is appreciated.

## Installation

Copy the file _ufuncts.py_ into your project and import it with
`import ufuncts`
or
`from ufuncts import *`.

## Function Overview

### Mathematical Functions

**minmax**(_min, max, val_): Clamp a value between _min_ and _max_. Alias: _truncate_.

**argmax**(_D_): Return the key with the highest value in a dictionary. 

**argmin**(_D_): Return the key with the lowest value in a dictionary.

**avg**(_L, r=None_): Returns average of an iterable _L_ of numerals, rounded to precision _r_ if set. Aliases: _average_, _mean_.

**get_mag**(_x, base=1024_): Return the integer magnitude of a number relative to a base.

**strbool**(_v_): Interpret a string as a bool in a canonical way, i.e. if _v_ is empty or a string that looks falsey (e.g. "0" or "False"), it will return `False`, otherwise `True`.

### File System Utilities

**fileslist**(_path, aspath=True, sort=False, sortkey=None_): Return a list of files in a directory (non-recursive).

**subfileslist**(_path, sort=True_): Return all files in a directory recursively, including subdirectories.

**get_unique_filename**(_basefilename, target_dir=None, startindex=1, sep="\_", aspath=False_): Generate a filename that is unique within the given directory (or the current file directory if not specified) by appending an incrementing index after a separator. If the filename is already unique, it will remain unchanged. 

**construct_path**(_path:str, mode=511_): Constructs a full directory path, including intermediate subpaths.

(wip, to be continued)

