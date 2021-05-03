from KAuthServer import KAuthServer
kas = KAuthServer(('localhost', 10005), 'k_auth_server')
kas.start()