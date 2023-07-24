import logging 


server_logger = logging.getLogger('server_logs')

server_logger.setLevel(logging.INFO)

server_handler = logging.FileHandler('server.log', mode='w')
server_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

server_handler.setFormatter(server_formatter)
server_logger.addHandler(server_handler)




