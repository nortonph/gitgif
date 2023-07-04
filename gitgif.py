# USE AT YOUR OWN RISK! USE ONLY ON A LOCAL COPY OF A GIT REPOSITORY YOU ARE READY TO ABANDON!
# A python script that produces a gif of the evolution of an image whos changes have been tracked by git.
# Checks out every commit of a local git repository, saves a specific image file at that commit and strings them
# together in an animated .gif
# HOWTO:    1. Clone a git repository (don't use this on a repo you're working on. No guarantees for any harm done!)
#           2. Set the variable "file_relpath" below to the relative path & filename of the figure in the repo you want
#           3. Run this script within the main directory of the repository
#           4. A subdirectory "gitgif" will be created in the parent directory containing all versions of this figure
#           5. If everything works, an animated gif file "git.gif" will be created in the "gitgif" directory
#  Philipp Norton, 2023

import os
import glob
import shutil
import subprocess
from PIL import Image

# filename (relative path) of image file to be loaded across commits
file_relpath = 'fig/fig2.png'

# flags and parameters
b_delete_images = True  # Set this to False to keep the individual images
b_get_images = True  # Set this to False if images already extracted and not deleted, to redo .gif generation faster
n_loops = 0  # number of loops the .gif will go through. 0 means infinitely looping, -1 means no loops
frame_duration_ms = 120  # duration of each .gif frame in milliseconds
scaling_factor = 0.5  # width in pixels of the resulting .gif will be the minimum width of all images times this
b_use_final_img_for_scale = False  # if True, .gif size will be scaled to final image instead of smallest (width) image
b_skip_commits_wo_figure = True  # if False, there will be one frame per commit, otherwise one frame per changed image

# split image filename
file_fullname = file_relpath.split(os.sep)[-1]
file_name = file_fullname.split('.')[0]
file_ext = file_fullname.split('.')[-1]

# create new directory for images
newpath = '..' + os.sep + 'gitgif'
if not os.path.exists(newpath):
    os.makedirs(newpath)

if b_get_images:
    # get list of git commit hashes and store them in a file
    subprocess.run('git --no-pager log --format=%H > ..' + os.sep + 'gitgif' + os.sep + 'gitlog.txt', shell=True)

    # open the log and get a list of commit hashes
    with open('..' + os.sep + 'gitgif' + os.sep + 'gitlog.txt') as file_log:
        commit_hashes = [line.rstrip() for line in file_log]

    # loop through commit hashes, check out each commmit & copy the image to the new directory, appending name with hash
    for i, h in enumerate(commit_hashes):
        rc = subprocess.run('git checkout ' + h + ' -- ' + file_relpath, shell=True)
        if rc.returncode and b_skip_commits_wo_figure:
            # if there is an error (likely because the commit doesn't feature the image, because there were no changes),
            # don't copy the file, unless we want one frame per commit (i.e. b_skip_commits_wo_figure==False),
            # in which case the last successfully saved image will be copied again.
            continue
        else:
            filename_out = file_name + '_' + str(i).zfill(4) + '_' + h + '.' + file_ext
            shutil.copy2(file_relpath, '..' + os.sep + 'gitgif' + os.sep + filename_out)
            print('created file ' + filename_out)

    # reset git repository
    subprocess.run('git reset --hard', shell=True)

# loop through list of image files, open and append to list of frames
print('reading images', end='')
frames = []
img_widths = []
image_names = glob.glob('..' + os.sep + 'gitgif' + os.sep + '*.' + file_ext)
image_names.sort()
for img in image_names:
    frames.append(Image.open(img))
    img_widths.append(frames[-1].size[0])
    print('.', end='')
    if b_delete_images:
        os.remove(img)

# resize frames to match
print('\nresizing frames', end='')
if b_use_final_img_for_scale:
    gif_width = img_widths[0] * scaling_factor
else:
    gif_width = min(img_widths) * scaling_factor
for i, frm in enumerate(frames):
    frames[i] = frm.resize((round(gif_width), round(frm.size[1] * gif_width / frm.size[0])), Image.Resampling.LANCZOS)
    print('.', end='')

# save frames (in reversed order) into an infinitely looping gif
print('\nsaving git.gif')
frames[-1].save('..' + os.sep + 'gitgif' + os.sep + 'git' + '_' + str(frame_duration_ms) + '_' + str(n_loops) + '_' +
                str(scaling_factor) + '.gif', format='GIF', append_images=frames[-2:0:-1],
                save_all=True, duration=frame_duration_ms, disposal=2, optimize=True, loops=n_loops)
