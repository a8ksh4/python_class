# Index:
* [Opening Files](#opening-files)
  * modes, read, write, append
* [shutil module](./README.md#shutil-module---high-level-file-operations)
* [glob module](#glob-module)
* [os module](#os-module)
  * [Basic Operations](#basic-operations)
    * os.getcwd, chdir, listdir, mkdir, remove
    * os.rmdir, symlink, umask
    * os.walk
  * [Permissions and stat](#permissions-and-stat)
    * os.chroot, os.chown, os.cmod, os.stat
  * [os.path](#ospath)
    * os.path.join, realpath, basename
    * Tests:
      * os.pth.isfile, isdir, islink, ismount
  * [tar and gzip](#tar-and-gzip)
  
  
https://docs.python.org/2/library/filesys.html  
  
# Opening Files
**Reading a file**
```python
In [31]: f = open('foo.yaml', 'r')

In [36]: print f.read()
- module: "python basics"
  content:
  - name: "prob1"
    desc: "foo"
  - name: "prob2"
    desc: "foo2"
- module: "python advanced"
  content:
  - name: "prob 1"
    desc: "foo3"

In [37]: f.close()
```
The "with" convention is more pythonic than opening and closing files as above.  This will ensure that files are only open in the context that they need to be and that they are closed.  Leaving files open is poor form... 
```python
In [38]: with open('blah.csv', 'r') as f:
   ....:     print f.read()
   ....:     
l0c0,l0c1,l0c2
l1c0,l1c1,l1c2
l2c0,l2c1,l2c2

In [39]: 
```  
**Modes**
* r - Open file for reading  
* w - Open file for writing; puts cursor at start of file (truncates file).  
* a - Open file for writing with cursor at end of file (appends file).  
* + - Open file for reading and writing.  
  
**Writing to a file**
```python
In [39]: animals = ('dog', 'moose', 'squirrel', 'cow')

In [40]: with open('the_animals.txt', 'w') as f:
   ....:     for animal in animals:
   ....:         f.write(animal + '\n')
   ....:         

In [42]: print open('the_animals.txt', 'r').readlines()
['dog\n', 'moose\n', 'squirrel\n', 'cow\n']

In [43]: print open('the_animals.txt', 'r').read()
dog
moose
squirrel
cow
```
And with append:
```python
In [44]: with open('the_animals.txt', 'a') as f:
   ....:     for city in ('sac', 'lax', 'slc', 'nyc'):
   ....:         f.write(city + '\n')
   ....:         

In [45]: print open('the_animals.txt', 'r').read()
dog
moose
squirrel
cow
sac
lax
slc
nyc
```

**Create empty file or truncate file**
```python
In [47]: open('newfile.out', 'w').close()
```

# shutil module - High-level file operations
https://docs.python.org/2/library/shutil.html

**Move a file**
```python
import shutil
src_path = '/tmp/my_file.foo'
dst_path = '/opt/my_file.bar'
shutils.move(src_path, dst_path)
```

**Copy a file**
```python
shutils.copy(src_path, dst_path)
```
# glob module
Provides unix-style pathname matching!
```python
In [146]: os.listdir('.')
Out[146]: ['foo.txt', 'b', 'a', 'c', 'foo.out']

In [150]: from glob import *

In [151]: glob('[a-c]')
Out[151]: ['b', 'a', 'c']

In [152]: glob('foo*')
Out[152]: ['foo.txt', 'foo.out']
```
**iglob** - returns in iterator instead of a list  
  
# os module
One of the core modules needed for any sysadmin to interact with the local environment and filesystem!  This stuff is frequenly done with system calls and really shouldn't be.  Your code will be much more reliable and maintainable if you os the proper modules and calls for this kind of stuff.  
  
*There are a bunch of useful os._ commands! Do dir(os), or type os and press \<tab\> in your ipython terminal*  
  
## Basic Operations
**os.getcwd** - get the current working directory  
**os.chdir** - change directory  
```python
In [66]: os.getcwd()
Out[66]: '/tmp'

In [67]: os.chdir('/tmp/foobar')

In [68]: os.getcwd()
Out[68]: '/tmp/foobar'
```
If a path does not exist, an "OSError" exception is raised:  
```python
try:
    os.chdir(path)
except OSError:
    print "path does not exist: {}".format(path)
```  
**os.listdir** - list contents of a directory. os.walk is more comprehensive alternative to this.  
```python
In [108]: os.listdir('.')
Out[108]: ['a.out', 'afile.txt']
```
**os.mkdir** - create a directory  
```python
In [109]: os.mkdir('new_directory')
```
**os.remove** - remove a file  
```python
In [110]: os.remove('afile.txt')

In [111]: os.listdir('.')
Out[111]: ['a.out', 'new_directory']
```
**os.rmdir** - remove a directory  
```python
In [112]: os.rmdir('new_directory')

In [111]: os.listdir('.')
Out[111]: ['a.out']
```
**os.symlnik** - create a symlink  
```python
In [104]: os.symlink('a.out', 'foo.out')
```
**os.readlink** - see where a symlink points  
```python
In [105]: os.readlink('foo.out')
Out[105]: 'a.out'
```
  
### os.walk
os.walk is useful enough that it deserves its own mini-section.  It lets' you "walk" through a directory structure either from top-down or from bottom-up an see all of the files at each point in the process.  
  
You can adapt the code below to, rather than printing names of files, actually do thigns to the files.  Change permissions; remove stuff; edit them; ...  
  
**Recursively list contents of a directory**
```python
In [139]: for root, dirs, files in os.walk('.'):
   .....:     print "where we are:", root
   .....:     print "whats here:"
   .....:     for f in files:
   .....:         print "    {}/{}".format(root, f)
   .....:     print "and any dirs:", dirs
   .....:     print ""
   .....:     
where we are: .
whats here:
    ./foo.txt
    ./foo.out
and any dirs: ['b', 'a', 'c']

where we are: ./b
whats here:
    ./b/b.txt
    ./b/b.foobar
and any dirs: []

where we are: ./a
whats here:
    ./a/a.txt
and any dirs: []

where we are: ./c
whats here:
    ./c/c.foobar
    ./c/c.txt
and any dirs: []
```

## Permissions and stat
**os.chown** - change file/dir ownership  
**os.chmod** - change file/dir permissions.  
**os.stat** - get filesystem data for some path  
```python
In [48]: os.stat('server_utility.py')
Out[48]: os.stat_result(st_mode=33204, st_ino=18221199, st_dev=2051, st_nlink=1, st_uid=1000, st_gid=1000, st_size=3060, st_atime=1509072922, st_mtime=1509072863, st_ctime=1509072863)
```
Each property available in stat is accessible directly.  E.g. to get the size of a file:
```python
In [49]: os.stat('server_utility.py').st_size
Out[49]: 3060
```
st_nlink => number of hard links to a file; st_uid => user id of file owner; st_gid => group id of group owner, st_mtime => modified time of file (in seconds since epoch), etc.   
  
**os.umask** - set the umask: set permissions that are removed from newly created filesystem objects  

  
## os.path
**os.path.join**  
os.path.join(path, *paths)  
  
**os.path.realpath** - Real path of a file - resolve relative path or traverse symlinks and find the actual path.  
```python
In [57]: p = '/home/thedude/Games/'

In [58]: os.path.realpath(p)
Out[58]: '/media/md0/thedude-extra/Games'
```
**os.path.basename** - name of file at end of a given path
**os.path.dirname** - all of a given path except for the file name at the end

**Real path of running script**
I use this all the time since my scripts are usually run from other directories and I can't count on the current working directory to be the same as the directory my script is in.  So get the script directory and then append it to access any other content/utilities that are in subdirectories, etc.  

```
desktop:~/git/python_class$ cat script_paths_example.py 
#!/usr/bin/env python

import doctest
import os

MY_PATH = os.path.realpath(__file__)
MY_FILENAME = os.path.basename(MY_PATH)
MY_DIR = os.path.dirname(MY_PATH)

if __name__ == '__main__':
    print "My path is:", MY_PATH
    print "My filename is:", MY_FILENAME
    
desktop:~/git/python_class$ ./script_paths_example.py 
My path is: /home/thedude/git/python_class/script_path_example.py
My filename is: script_path_example.py
My dir is: /home/thedude/git/python_class
desktop:~/git/python_class$ 

```

**Tests**
`os.path.isfile(my_path)` - True if it path is a file
`os.path.isdir(my_path)` - True if path is a directory
`os.path.islink(my_path)` - True if path is a symlink
`os.path.ismount(my_path)` - True if path is a mount point

```python
def cdToSymlinkDir(sym_path):
    '''given a symlink path to a file or directory,
    identify the real path to that object and cd
    to it. Raise exception if given pth is not a symlink'''
    if not os.path.islink(sym_path):
        raise IOError('symlink expected: {}'.format(sym_path))
    target_file = os.path.realpath(sym_path)
    target_dir = os.path.dirname(target_file)
    os.path.cd(target_dir)
    return target_file
```

create/destroy
shutil
shutil.copyfile(src, dst)
shutil.movefile(src, dst)


filecmp
os
os.chdir
os.path.isfile
os.path.isdir
os.makedirs
os.path.exists
os.access
    if not ( os.access('/tmp', os.R_OK) and
             os.access('/tmp', os.W_OK) and
             os.access('/tmp', os.X_OK)):
        raise IOError("/tmp permissions err!")
os.chown(os.path.join(root, momo), make_uid, -1)
CWF = os.path.realpath(__file__)
CWD = os.path.dirname(CWF)

## Misc
**os.chroot** - this has to be done as root; it's useful for sandboxing a process into some area of the filesystem by telling it that the root directory is actually some aribtrary path.  You can call chroot and then launch a subprocess in the altered env.  NOTE:  ipython barfs a little bit when this is used.  Still works, though. 
```python
In [4]: os.getcwd()
Out[4]: '/home/drnorris/tmp/sample'

In [5]: os.listdir('.')
Out[5]: ['foo.txt', 'b', 'a', 'c', 'foo.out']

In [6]: os.chroot('.')

In [7]: The history saving thread hit an unexpected error (OperationalError('attempt to write a readonly database',)).History will not be written to the database.


In [7]: os.getcwd()
Out[7]: '/'

In [8]: os.listdir('.')
Out[8]: ['foo.txt', 'b', 'a', 'c', 'foo.out']
```

# tar and gzip
## tar
**creating and adding files**
```python
In [39]: os.listdir('.')
Out[39]: ['d', 'e', 'b', 'a', 'c']

In [40]: with tarfile.open('myjunk.tar', 'w') as t:
   ....:     for fname in os.listdir('.'):
   ....:         t.add(fname)
   ....:         
```  
**list contents**
```python
In [41]: with tarfile.open('myjunk.tar', 'r') as t:
   ....:     contents = t.getmembers()
   ....:     t.list()
   ....:     
-rw-rw-r-- fred/fred          0 2017-10-12 17:43:40 d
-rw-rw-r-- fred/fred          0 2017-10-12 17:43:40 e
-rw-rw-r-- fred/fred          0 2017-10-12 17:43:40 b
-rw-rw-r-- fred/fred          0 2017-10-12 17:43:40 a
-rw-rw-r-- fred/fred          0 2017-10-12 17:43:40 c

In [52]: for c in contents:
   ....:     print c
   ....:     
<TarInfo 'd' at 0x7fc1c6e3bd90>
<TarInfo 'e' at 0x7fc1c6e3b0d0>
<TarInfo 'b' at 0x7fc1c6e3bed0>
<TarInfo 'a' at 0x7fc1c6e3bd50>
<TarInfo 'c' at 0x7fc1c6e3be50>
```  
**extracting**
```python
In [43]: os.mkdir('extract_here')

In [44]: os.chdir('./extract_here/')

In [45]: os.listdir('.')
Out[45]: [ ]
In [46]: with tarfile.open('../myjunk.tar', 'r') as t:
   ....:     t.extractall()
   ....:     

In [47]: os.listdir('.')
Out[47]: ['d', 'e', 'b', 'a', 'c']
```
  
## gzip
gzip is a file handling wrapper for zlib, which can be used to compress arbitrary data (very conveniently)!
```python
In [62]: import zlib

In [63]: foo = '''<TarInfo 'd' at 0x7fc1c6e3bd90>
   ....: <TarInfo 'e' at 0x7fc1c6e3b0d0>
   ....: <TarInfo 'b' at 0x7fc1c6e3bed0>
   ....: <TarInfo 'a' at 0x7fc1c6e3bd50>
   ....: <TarInfo 'c' at 0x7fc1c6e3be50>
   ....: '''

In [64]: len(foo)
Out[64]: 160
In [66]: zfoo = zlib.compress(foo)

In [67]: print zfoo
x��	I,��K�WPOQWH,Q0�0OK6L6K5NJ�4�㲁˧�����'�˧��'b�o�"���$�@.�

In [68]: len(zfoo)
Out[68]: 67

In [69]: print zlib.decompress(zfoo)
<TarInfo 'd' at 0x7fc1c6e3bd90>
<TarInfo 'e' at 0x7fc1c6e3b0d0>
<TarInfo 'b' at 0x7fc1c6e3bed0>
<TarInfo 'a' at 0x7fc1c6e3bd50>
<TarInfo 'c' at 0x7fc1c6e3be50>

```
**gzipping a file**
_We have to read it to write it out with gzip..._
```python
In [69]: import gzip

In [83]: os.stat('./somdata.txt').st_size
Out[83]: 160

In [82]: with open('somdata.txt', 'r') as f:
   ....:     content = f.read()
   ....:     

In [85]: with gzip.open('somdata.txt.gz', 'wb') as f:
   ....:     f.write(content)
   ....:     

In [86]: os.stat('./somdata.txt.gz').st_size
Out[86]: 91
```

**read a gzipped file**
```python
In [95]: with gzip.open('somdata.txt.gz', 'rb') as f:
   ....:     new_content = f.read()
   ....: print new_content
   ....: 
<TarInfo 'd' at 0x7fc1c6e3bd90>
<TarInfo 'e' at 0x7fc1c6e3b0d0>
<TarInfo 'b' at 0x7fc1c6e3bed0>
<TarInfo 'a' at 0x7fc1c6e3bd50>
<TarInfo 'c' at 0x7fc1c6e3be50>

```
