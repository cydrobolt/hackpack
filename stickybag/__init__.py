from flask import Flask, render_template, request, g, redirect, Markup, url_for, flash, session
import hashlib, urllib
import datetime
import random, string
import os, logging, time


#########################
####    STICKYBAG    ####
#########################
'''
(c) Copyright 2014 Chaoyi Zha, Jason Fisch, Max Shavrick

Authors: Chaoyi Zha <summermontreal@gmail.com>

</>ed w/ <3 @ PennApps X

In the future, use MongoDB :)

'''

####################
####    VARS    ####
####################

userdata = dict()

f = open('post.log', 'a')
f.write("Opened")

#Init Flask
app = Flask(__name__, static_url_path='')

#Init Random
random.seed()

# Helper Functions

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


#############################################
#                  ROUTINGS                 #
#############################################

@app.route('/')
def root():
	return app.send_static_file('index.html')
@app.route('/io/in/<token>/<accel_data>', methods=['POST', 'GET'])
def ioin (token, accel_data):
	accel_data = str(accel_data)
	try:
		bahtoken = userdata[token]['ex']+"exist?"
		# does the token already exist?
		
		# no exception? yup
	except:
		# nope
		userdata[token] = dict()
		userdata[token]['ex'] = "yes"
		userdata[token]['accel']  = dict()
		userdata[token]['gps']  = dict()
	try:
		try:
			#accel_data = str(request.args.get('accel_data', '')) # POST'ed piece of accelorometer data
			accel_array = accel_data.split("-")
			#f.write(accel_data)
			accel_array = [int(x) for x in accel_array]
			accel_data = sum(accel_array)
		except:
			accel_data = 0 # if N/A, don't graph as a large diff!
		try:
			gps_data = request.args.get('gps_data', '') # POST'ed piece of GPS data
		except:
			gps_data = 0 # if N/A, don't graph as a large diff!
		ts = time.time()
		st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
		userdata[token]['accel'][str(st)] = accel_data
		userdata[token]['gps'][str(st)] = gps_data
		userdata[token]['latest_accel'] = accel_data
		userdata[token]['latest_gps'] = gps_data
			
		return "ok"
	except:
		return "error"

@app.route('/pdata/<token>')
def pdata(token):
	return render_template('pdata.html', token=token)
	
@app.route('/sdata')
def sdata():
	return app.send_static_file('sdata.html')


@app.route('/io/out/<token>', methods=['GET', 'POST'])
def ioout(token):
	# get JSON accel & gps data
	try:
		accel_d = userdata[token]['latest_accel']
		gps_d = userdata[token]['latest_gps']
	except:
		return '{"accel":"0","gps":"0"}'

	return '{"accel":"'+str(accel_d)+'","gps":"'+str(gps_d)+'"}'

# weird things for skel.js

# secret key used to encrypt sessions
app.secret_key = 'StickyBagIsAwesome'
