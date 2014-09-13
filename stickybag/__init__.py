from flask import Flask, render_template, request, g, redirect, Markup, url_for, flash, session
import hashlib, urllib
import datetime
import random, string
import os

#########################
####    STICKYBAG    ####
#########################


#Init Flask
app = Flask(__name__)

#Init Random
random.seed()

# Helper Functions

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False



def getrole(user):
    try:
        role = User.query.filter_by(username=user).first().role
        return role
    except:
        return False

def curr_is_admin():
    try:
        role = User.query.filter_by(username=session['username']).first().role
        if role == "Administrator" or role == "Developer" or role == "Owner":
            return True
        else:
            return False
    except:
        return False




#############################################
#                  ROUTINGS                 #
#############################################

@app.route('/io/in/<token>')
def ioin (token, methods=['GET', 'POST']):
	pass


# secret key used to encrypt sessions
app.secret_key = 'StickyBagIsAwesome'
