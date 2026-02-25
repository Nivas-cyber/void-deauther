import time
import threading

class ChannelHopper:
    def __init__(self, interface_manager, channels=None):
        self.im = interface_manager
        self.channels = channels or [1, 6, 11, 2, 7, 12, 3, 8, 13, 4, 9, 5, 10]
        self.hopping = False

    def hop(self):
        while self.hopping:
            for channel in self.channels:
                if not self.hopping:
                    break
                self.im.set_channel(channel)
                time.sleep(2) # Spend 2 seconds on each channel

    def start(self):
        self.hopping = True
        self.hop_thread = threading.Thread(target=self.hop, daemon=True)
        self.hop_thread.start()

    def stop(self):
        self.hopping = False
