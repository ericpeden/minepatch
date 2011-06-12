#!/usr/bin/env python

import atexit
import contextlib
import os
import shutil
import tempfile
import zipfile

@contextlib.contextmanager
def cd(path):
    cwd = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(cwd)

class Error(Exception):
    pass

class MissingModDirectory(Error):
    pass

CLEAN = "../minecraft_clean.jar"
PATCHED = "../minecraft.jar"
MOD_DIR = "../ModLibrary"

if not os.path.exists(MOD_DIR):
    raise MissingModDirectory(os.path.abspath(MOD_DIR))

if not os.path.exists(CLEAN):
    raise MissingJar(os.path.abspath(CLEAN))

# Extract the clean jar to a temp directory
extract_dir = tempfile.mkdtemp()
atexit.register(shutil.rmtree, extract_dir)

print "Extracting %s..." % CLEAN
clean_jar = zipfile.ZipFile(CLEAN)
clean_jar.extractall(path=extract_dir)

# blow the META-INF directory away
shutil.rmtree(os.path.join(extract_dir, "META-INF"))

# extract mods
for mod in sorted(os.listdir(MOD_DIR)):
    if mod.endswith('zip'):
        print "Installing mod '%s'..." % os.path.splitext(mod)[0]
        mod_zip = zipfile.ZipFile(os.path.join(MOD_DIR, mod))
        mod_zip.extractall(path=extract_dir)
    else:
        raise Error("unrecognized type of mod for '%s'" % mod)

# repackage the jar
print "Re-packaging patched Minecraft to %s..." % PATCHED
patched_jar = zipfile.ZipFile(PATCHED, 'w')
with cd(extract_dir):
    for dirpath, dirnames, filenames in os.walk(extract_dir):
        for f in filenames:
            relpath = os.path.relpath(os.path.join(dirpath, f), extract_dir)
            patched_jar.write(relpath)
patched_jar.close()
