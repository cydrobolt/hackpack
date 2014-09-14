from flask import Flask, render_template, request, g, redirect, Markup, url_for, flash, session
import hashlib, urllib
import datetime
import random, string
import os


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

user_data = dict()



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
@app.route('/io/in/<token>')
def ioin (token, methods=['GET', 'POST']):
	try:
		token = userdata[token]['ex']+"exist?"
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
			accel_data = request['accel_data'] # POST'ed piece of accelorometer data
		except:
			accel_data = 0 # if N/A, don't graph as a large diff!
		try:
			gps_data = request['gps_data'] # POST'ed piece of GPS data
		except:
			gps_data = 0 # if N/A, don't graph as a large diff!
		
		userdata[token]['accel'][str(time.strftime("%c"))] = accel_data
		userdata[token]['gps'][str(time.strftime("%c"))] = gps_data
		userdata[token]['latest_accel'] = accel_data
		userdata[token]['latest_gps'] = gps_data
		
		return "ok"
	except:
		return "error"

@app.route('/pdata/<token>')
def pdata(token):
	pass
	
@app.route('/sdata')
def sdata():
	return app.send_static_file('sdata.html')


@app.route('/io/out/<token>')
def ioout(token):
	# get JSON accel & gps data
	accel_d = userdata[token]['latest_accel']
	gps_d = userdata[token]['latest_gps']

	return '{"accel":"'+accel_d+'"gps":"'+gps_d+'"}'	

# weird things for skel.js

# secret key used to encrypt sessions
app.secret_key = 'StickyBagIsAwesome'
