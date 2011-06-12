What is minepatch?
==================

`minepatch` is Yet Another Minecraft mod loader. Most loaders require 
making at least an initial modification of the Minecraft jar, and the 
ones that don't I could never get to work consistently. I figure if I 
have to modify the jar anyway, I might as well just put all the mods in 
there while I'm at it. `minepatch` automates this process. 


How do I use it?
================

Requirements
------------
You'll need to have Python 2.6 or 2.7 installed.

Installing
----------
If you'd like to clone the entire repository:

* `git clone` the repo into your `.minecraft/bin` directory.

If you'd rather just copy the `patch.py` file:

* Place `patch.py` directly into your `.minecraft/bin` directory.
* Edit `patch.py` and remove the `../` prefixes from the `CLEAN`, `PATCHED`, 
and `MOD_DIR` constants near the top of the file. 

Regardless of how you "installed" the tool, you should now do the following:

* Make a copy of `minecraft.jar` and rename it to `minecraft_clean.jar`.
* Create a `ModLibrary` directory inside of `.minecraft/bin`.
* Place `.zip` files of the mods you want installed inside of `ModLibrary`.
* Run `patch.py`.

You should now have a `minecraft.jar` that includes the mods you copied 
into `ModLibrary`. Have fun. 


Notes
=====

Mods are installed in alphabetical order. You can rename the zipped mods 
if you need to force a specific ordering. 

Known Issues
============

* Only `.zip` mods can be installed.
* This will (hopefully!) be obsolete once Minecraft 1.7 is released.