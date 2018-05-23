# -*- encoding: utf-8 -*-
"""
Python Aplication Template
Licence: GPLv3
"""

#################
#### imports ####
#################

from flask import Flask


################
#### config ####
################

app = Flask(__name__, instance_relative_config=True)


####################
#### blueprints ####
####################

from app.views import login_blueprint, users_blueprint, clear_blueprint, admin_blueprint

# register the blueprints
app.register_blueprint(login_blueprint)
app.register_blueprint(users_blueprint)
app.register_blueprint(clear_blueprint)
app.register_blueprint(admin_blueprint)
