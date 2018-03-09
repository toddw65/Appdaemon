import appdaemon.plugins.hass.hassapi as hass
import pymysql

#
# Change Channel on Dish Receiver
# To call it, fire a change_channel event with room/channel string
#      i.e. - "office tv to channel 132"
#             or
#             "master bedroom tv to Turner Classic Movies" 
#             or
#             "kitchen tv to TCM" 
#
# Note that the word 'tv' is required

class SetChannel(hass.Hass):
    def initialize(self):
        self.log("SetChannel loaded")
        self.listen_event(self.do_change, 'change_channel')

    def do_change(self, event_name, data, kwargs): 
        host_ip = self.args["host_ip"]
        db_user = self.args["db_user"]
        db_pass = self.args["db_pass"]
        db_name = self.args["db_name"]
        
        words = str(data["channel_name"]).lower().split()
        room = words[words.index("tv")-1]
        channel_name = ' '.join(words[words.index("tv")+2:])
        
        self.log(words)
        self.log(room)
        self.log(channel_name)
       
        # If the word 'channel' is in the phrase, assume a number follows
        try:
            if "channel" not in channel_name:
                conn = pymysql.connect(host = host_ip, user = db_user, passwd = db_pass, db = db_name)
                c = conn.cursor()
                c.execute("""SELECT channel_number FROM dish_channels WHERE channel_name like %s UNION SELECT channel_number FROM dish_channels WHERE channel_abbrev = %s;""", ('%' + channel_name + '%', channel_name))
                results = c.fetchone()
                channel_number = results[0]
                self.log("Something went wrong.  Couldn't get a channel number.").log(channel_number)
                self.log(channel_number)
                conn.close()
            else:
                #if the word 'channel' is NOT in the phrase, assume we're getting a channel name or abbreviation
                results = [int(s) for s in channel_name.split() if s.isdigit()]
                self.log(results)
                channel_number = results[0]
                self.log(channel_number)
        except:
            self.log("Something went wrong.  Couldn't get a channel number.")
        
        delay = 2
        for c in str(results):
            self.run_in(self.do_channel, delay, channel_number = c, room = room)
            delay += 1
                
    def do_channel(self, kwargs):
        self.call_service("media_player/select_source", source = "chan_0"+kwargs["channel_number"], entity_id = "media_player."+kwargs["room"]+"_tv__dish")