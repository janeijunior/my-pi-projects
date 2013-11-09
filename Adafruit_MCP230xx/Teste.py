import os.system
import os.spawn*
import os.popen*
import popen2.*
import commands.*

if __name__ == '__main__':
    #var = os.system("ls")
    subprocess.call(['gst-server.sh', str(domid)])