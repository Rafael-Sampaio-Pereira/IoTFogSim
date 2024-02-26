import datetime
from core.functions import get_last_dir_inside_of
from twisted.internet import reactor
import sys

from core.configurations import CoreConfig

import sys
sys.dont_write_bytecode = True


import os
import setproctitle
setproctitle.setproctitle('SmartSecene Simulator - A IoTFogSim Extension')

if __name__ == '__main__':
    CoreConfig()
    import subprocess
    import  time
    time.sleep(3)
    os.system("chmod +x ./cpu_n_ram_logger.py")
    # subprocess.Popen("chmod +x ./cpu_n_ram_logger.py", shell=True, stdout=subprocess.PIPE)
    
    reactor.run()
    