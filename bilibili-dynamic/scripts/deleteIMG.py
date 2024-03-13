import os
import shutil

imgdir = 'images'

if os.path.exists(imgdir):
    shutil.rmtree(imgdir)
else:
    pass