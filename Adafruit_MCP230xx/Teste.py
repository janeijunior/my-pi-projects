import subprocess

if __name__ == '__main__':
    #var = os.system("ls")
    subprocess.call(['./gst-server.sh'], shell=True)