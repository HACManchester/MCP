# Add the current file's parent folder to the path, so wsgi imjport will work
import sys
sys.path.insert(0, os.path.dirname(__file__))

from space_automation import app as application
