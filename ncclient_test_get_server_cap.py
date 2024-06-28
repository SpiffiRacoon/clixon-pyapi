from ncclient import manager
from time import sleep
import logging

logging.basicConfig(
    level=logging.DEBUG
)

nc_manager = manager.connect_UnixSocket('/usr/local/var/run/controller.sock')

sleep(5)

nc_manager.close_session()