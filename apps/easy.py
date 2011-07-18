from pili import lite
import time

def main():
    lite.init(globals())
    echo("Hello, webapp World!"+str(time.time()))

if __name__ == "__main__": 
    main()

