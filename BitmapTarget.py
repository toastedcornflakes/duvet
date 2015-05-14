from Target import Target

import subprocess

class BitmapTarget(Target):
    def __init__(self, binpath):
        self.binpath = binpath

    # input is a filepath
    def run(self, input):
        p = subprocess.Popen([self.binpath, input], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        p.wait()
        if p.returncode != 0:
            return p.returncode
        else:
            return None
    
    def input_type(self):
        return "bmp"
    
    def __str__(self):
        return self.binpath
