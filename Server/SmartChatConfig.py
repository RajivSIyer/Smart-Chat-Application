import yaml

class smart_chat_config(object):
    def __init__(self):
        self.server_ip = ''
        self.port = 12345
        self.version = 1.0
        try:
            stream = open('SmartChat.yml', 'r')
            config_dict = yaml.load(stream)
            print("Loading Configuration...")
            for key, value in config_dict.items():
                print(key+':'+str(value))

            self.server_ip = config_dict['server_ip']
            self.port = config_dict['port']
            self.version = config_dict['version']
        except Exception as e:
            print('Error occured while loading the file.\n Exception: ', str(e))
            raise e