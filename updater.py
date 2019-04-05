from subprocess import check_call as run 
from getopt import getopt, GetoptError 
UPDATE_CMD = ( # base command 
'pip install --src="%s" --upgrade -e ' 
'git@github.com:r58Playz/factories-python.git' 
) 
run(UPDATE_CMD)