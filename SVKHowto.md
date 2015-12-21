Even though code.google uses subversion for source code control, anyone who submits changes to CAIRN must use [svk](http://svk.bestpractical.com) instead of subversion. There a few reasons as to why svk is used.

From [SVK's website](http://svk.bestpractical.com):
> svk is a decentralized version control system built with the robust Subversion filesystem.
> It supports repository mirroring, disconnected operation, history-sensitive merging, and
> integrates with other version control systems, as well as popular visual merge tools.

## Why SVK ##

SVK is designed to be a decentralized version control system but the usage for the CAIRN project is mainly local mirrors of the central repository. SVK allows you to mirror a repository, make a series of local changes and commits, then push those commits back up onto the repository. It also has a smart merging tool akin to GNUArch and svnmerge.py.

Another great feature of SVK is that someone who does not have commit access can download the code and do a series of changes and commits. Then they can ask SVK to generate a patch file containing those changes and commits and submit that patch file for review. A secondary reason is that since every developer will be mirroring the central repository on google we get that many backups of the full repository.

The general usage pattern is:
  * mirror the CAIRN subversion repository to your local machine with svk
  * create a local branch for your work
  * edit and commit changes in your local branch
  * submit the set of changes once you are ready

## Getting setup ##

First SVK must be installed. See SVK's [installation instructions](http://svk.bestpractical.com/view/InstallingSVK) for more information on this.

From there you must initialize your SVK depotmap which is its local repository.
```
svk depotmap --init
```

Then mirror the CAIRN repository. As a developer with commit access.
```
svk mirror https://cairn.googlecode.com/svn/trunk //cairn/code.google/trunk
```
Or as read only access.
```
svk mirror http://cairn.googlecode.com/svn/trunk //cairn/code.google/trunk
```

The newly created mirror must then be synced.
```
svk sync //cairn/code.google/trunk
```

After its synced you should create a local branch for your edits.
```
svk cp //cairn/code.google/trunk //cairn/mybranch/trunk
```

Then checkout a working copy from this branch.
```
svk co //cairn/mybranch/trunk cairn
```

## Normal use of SVK ##

Now do any edits and commits as you would with subversion, only use svk instead of svn. The svk command syntax largely maps to svn's syntax.

To push any changes back to the central repository run from within your working copy:
```
svk push
```
Or specify the local repository path:
```
svk push //cairn/mybranch/trunk
```

To sync up and retrieve any changes from the central repository run from within your working copy:
```
svk pull
```
Or specify the local repository path:
```
svk pull //cairn/mybranch/trunk
```

See also [SVKUsage](http://svk.bestpractical.com/view/SVKUsage).

## Generating Patches ##

The svk push command can generate a patch instead of trying to directly commit the changes. To do this run from your working copy:
```
svk push -P
```

This patch file can then be submitted as an issue ticket with the type label of 'patch'. It will then be reviewed for inclusion to the source tree.