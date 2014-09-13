import stickybag
import os
from stickybag import app

cport = 8080#os.getenv(PORT, 8080)
cip = '0.0.0.0'#os.getenv(IP,'0.0.0.0')


if __name__ == "__main__":
	app.run(debug=True)
    print "running"

