import os 
app_path = os.path.abspath(os.path.dirname(__file__) )

class Config(object):
    BOOTSTRAP_SERVE_LOCAL = True
    STATIC_FOLDER = 'static'
    SITE_NAME = 'Ishtar'
    
    