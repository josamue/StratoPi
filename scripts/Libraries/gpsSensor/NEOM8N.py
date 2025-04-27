from threading import Thread, Event
from ublox_gps import UbloxGps
import serial

class NEOM8N:
    def __init__(self):
        self.port = serial.Serial('/dev/ttyAMA0', baudrate=9600, timeout=1)
        self.gps = UbloxGps(self.port)

        self.position = [0, 0, 0]  # Longitude, Latitude, Altitude

        self.running = Event()
        self.running.set()
        self.thread = Thread(target=self._update_gps_values, daemon=True)
        self.thread.start()

    def _update_gps_values(self):
        while self.running.is_set():
            try:
                coords = self.gps.geo_coords()  # Holt die GPS-Daten
                self.position[0] = coords.lon   # Longitude
                self.position[1] = coords.lat   # Latitude
                self.position[2] = coords.height  # Altitude (Höhe)

            except Exception as err:
                print(f"GPS-Fehler: {err}")

    def getPosition(self):
        if len(self.position) < 3:
            return 0, 0, 0  # Falls noch keine Daten verfügbar sind
        return self.position[0], self.position[1], self.position[2]

    def stop(self):
        """Beendet den Thread sauber."""
        self.running.clear()
        self.thread.join()

