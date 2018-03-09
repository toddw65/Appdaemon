import appdaemon.appapi as appapi

class hello_api(appapi.AppDaemon):

    def initialize(self):
        self.register_endpoint(self.hello_api)        

    def hello_api(self, data):
      self.log(data)
      return "ok",200