# gitgif

USE AT YOUR OWN RISK! USE ONLY ON A LOCAL COPY OF A GIT REPOSITORY YOU ARE READY TO ABANDON!  
A python script that produces a gif of the evolution of an image whos changes have been tracked by git.  
Checks out every commit of a local git repository, saves a specific image file at that commit and strings them  
together in an animated .gif file

1. Clone a git repository (don't use this on a repo you're working on. No guarantees for any harm done!)
2. Set the variable "file_relpath" below to the relative path & filename of the figure in the repo you want
3. Run this script within the main directory of the repository
4. A subdirectory "gitgif" will be created in the parent directory containing all versions of this figure
5. If everything works, an animated gif file "git.gif" will be created in the "gitgif" directory

Example gif created with gitgif:

![Example .gif](https://github.com/nortonph/gitgif/blob/main/example.gif)
