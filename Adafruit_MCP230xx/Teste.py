os.system
os.spawn*
os.popen*
popen2.*
commands.*

if __name__ == '__main__':
    #var = os.system("ls")
    subprocess.call(['gst-server.sh', str(domid)])