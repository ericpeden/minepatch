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
    mod_relpath = os.path.join(MOD_DIR, mod)

    if mod.startswith('_'):
        # skip mods prefixed with an underscore
        continue

    if mod.endswith('zip'):
        print "Installing zipped mod '%s'..." % os.path.splitext(mod)[0]
        mod_zip = zipfile.ZipFile(mod_relpath)
        mod_zip.extractall(path=extract_dir)
    elif os.path.isdir(mod_relpath):
        print "Installing extracted mod '%s'..." % mod
        for dirpath, dirnames, filenames in os.walk(mod_relpath):
            # get the path relative to the mod directory
            reldir = os.path.relpath(dirpath, mod_relpath)
            # make any required parent directories underneath the extracted dir
            install_dir = os.path.join(extract_dir, reldir)
            if not os.path.exists(install_dir):
                os.makedirs(install_dir)
            for f in filenames:
                shutil.copy2(os.path.join(dirpath, f), install_dir)
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
