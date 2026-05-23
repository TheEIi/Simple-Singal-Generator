import numpy as np
from scipy import signal

class WaveDescriptor:
    def __init__(self, name, wave_type, freq, amp, phase, noise):
        self.name = name
        self.wave_type = wave_type
        self.freq = freq
        self.amp = amp
        self.phase = phase 
        self.noise = noise # Value from 0.0 to 5.0

class SignalEngine:
    def __init__(self, sample_rate=44100, duration=0.2):
        self.sample_rate = sample_rate
        self.duration = duration
        self.t = np.linspace(0, self.duration, int(self.sample_rate * self.duration))

    def generate(self, wave_obj: WaveDescriptor):
        # Base signal calculation
        theta = 2 * np.pi * wave_obj.freq * self.t + wave_obj.phase
        
        if wave_obj.wave_type == "Sine":
            y = wave_obj.amp * np.sin(theta)
        elif wave_obj.wave_type == "Square":
            y = wave_obj.amp * signal.square(theta)
        elif wave_obj.wave_type == "Sawtooth":
            y = wave_obj.amp * signal.sawtooth(theta)
        elif wave_obj.wave_type == "Triangle":
            y = wave_obj.amp * signal.sawtooth(theta, width=0.5)
        else:
            y = np.zeros_like(self.t)
            
        # NOISE
        if wave_obj.noise > 0:
            noise_array = np.random.uniform(-wave_obj.noise, wave_obj.noise, len(self.t))
            y = y + noise_array
            
        return self.t, y