"""
module to import all necessary modules
"""
from tornado.gen import coroutine
from tornado.ioloop import IOLoop
from tornado.escape import json_encode
from tornado.httpserver import HTTPServer
from tornado.options import define, options
from tornado.web import RequestHandler, Application, removeslash

import jwt
import json
import pickle
import requests
import uuid, os
import textwrap
import collections
import numpy as np
import pandas as pd
from motor import MotorClient
from datetime import datetime
from bson.objectid import ObjectId
from passlib.hash import pbkdf2_sha256
from os.path import join, dirname, isfile
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

secret = os.environ['SECRET']
db = MotorClient("mongodb://" + os.environ['DB_UNAME'] + ":" + os.environ['DB_PSWD'] + "@ds133004.mlab.com:33004/arbitrium")["arbitrium"]
