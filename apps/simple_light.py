class PantryLight(appapi.AppDaemon):
  def initialize(self):
    self.listen_state(self.doorStatusChange, "binary_sensor.pantry_door_triggered")

  def doorStatusChange(self, entity, attribute, old, new, kwargs):
    self.turn_on("light.pantry") if new == "on" else 
self.turn_off("light.pantry")