import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None):
        # Set up a dark themed figure
        plt.style.use('dark_background')
        self.fig = Figure(figsize=(8, 5), dpi=100, facecolor='#121212')
        self.axes = self.fig.add_subplot(111)
        self.axes.set_facecolor('#1e1e1e')
        self.axes.grid(True, color='#444444', linestyle='--', linewidth=0.5)
        super().__init__(self.fig)

    def plot_signals(self, signals_data):
        self.axes.clear()
        self.axes.grid(True, color='#444444', linestyle='--', linewidth=0.5)
        
        for t, y, label in signals_data:
            self.axes.plot(t, y, label=label, linewidth=2)
        
        if signals_data:
            legend = self.axes.legend(loc='upper right', frameon=True)
            legend.get_frame().set_facecolor('#121212')
            
        self.axes.set_ylim(-11, 11)
        self.axes.set_xlabel("Time (s)", color='gray')
        self.axes.set_ylabel("Amplitude", color='gray')
        self.draw()