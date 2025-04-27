import RPi.GPIO as GPIO
import time
from threading import Thread, Event

class GeigerCounter:
    def __init__(self, pin):
        self.pin = pin
        self.timestamps = []  # Liste zur Speicherung der Zeitstempel
        self.interval = 60  # Gleitendes Fenster von 10 Sekunden
        self.running = Event()

        # GPIO-Setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        # Event-Detection für Impulse
        GPIO.add_event_detect(self.pin, GPIO.RISING, callback=self._record_pulse)

        # Hintergrundthread zum Bereinigen
        self.running.set()
        self.thread = Thread(target=self._clean_old_timestamps, daemon=True)
        self.thread.start()

    def _record_pulse(self, channel):
        """Callback-Funktion zur Speicherung eines Impulses mit Zeitstempel."""
        now = time.time()
        self.timestamps.append(now)

    def _clean_old_timestamps(self):
        """Entfernt alte Zeitstempel, die nicht mehr im Intervall liegen."""
        while self.running.is_set():
            now = time.time()
            # Entferne alle Zeitstempel älter als das Intervall
            self.timestamps = [t for t in self.timestamps if now - t <= self.interval]
            time.sleep(1)  # Reinigungsintervall (kann angepasst werden)

    def get_count(self):
        """Gibt die Anzahl der Impulse in den letzten 10 Sekunden zurück."""
        now = time.time()
        return len([t for t in self.timestamps if now - t <= self.interval])

    def stop(self):
        """Beendet den Geiger-Müller-Zähler und räumt GPIO-Ressourcen auf."""
        self.running.clear()
        GPIO.cleanup()
