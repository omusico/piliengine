from pili import lite
import time

def main():
    lite.init(globals())
    echo("111=="+str(time.time()))
    #exit(0)

if __name__ == "__main__": 
    main()
    exit(0)

