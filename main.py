import sys
import numpy as np
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QSlider, QLabel, QComboBox, 
                             QPushButton, QRadioButton, QGroupBox, QListWidget, 
                             QSpinBox, QDoubleSpinBox)
from PyQt6.QtCore import Qt
from signal_engine import SignalEngine, WaveDescriptor
from plot_canvas import MplCanvas

# --- CSS part ---
DARK_STYLE = """
QMainWindow { background-color: #0B0E14; }
QWidget { background-color: #0B0E14; color: #D1D5DB; font-family: 'Segoe UI'; font-size: 12px; }

QGroupBox { 
    border: 1px solid #1F2937; 
    border-radius: 4px; 
    margin-top: 20px; 
    padding-top: 10px; 
    font-weight: bold; 
    color: #38BDF8; 
}
QGroupBox::title { subcontrol-origin: margin; left: 8px; }

QSlider::groove:horizontal { background: #1F2937; height: 4px; }
QSlider::handle:horizontal { background: #38BDF8; width: 14px; height: 14px; margin: -5px 0; border-radius: 7px; }

QPushButton#addBtn { background-color: #059669; color: white; border-radius: 4px; padding: 6px; font-weight: bold; }
QPushButton#clearBtn { background-color: #991B1B; color: white; border-radius: 4px; padding: 6px; font-weight: bold; }

/* COMPACT LOG STYLING */
QListWidget { 
    background: #090C10; 
    border: 1px solid #1F2937; 
    font-family: 'Consolas', 'Monaco', monospace; 
    font-size: 10px; 
    color: #94A3B8;
}
QListWidget::item { 
    padding: 1px 4px; 
    border-bottom: 1px solid #161B22;
}
QListWidget::item:selected { background-color: #1E293B; color: #38BDF8; }
"""

class SignalGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Signal Generator")
        self.resize(1300, 850)
        self.setStyleSheet(DARK_STYLE)

        self.engine = SignalEngine()
        self.active_signals = []
        self.init_ui()
        self.update_live_preview()
        

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)

        # --- LEFT CONTROLS ---
        controls = QVBoxLayout()
        controls.setSpacing(15)
        
        cfg_box = QGroupBox("WAVEFORM PARAMETERS")
        cfg_layout = QVBoxLayout()

        # Wave Selection
        cfg_layout.addWidget(QLabel("Signal Type:"))
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Sine", "Square", "Sawtooth", "Triangle"])
        self.type_combo.currentIndexChanged.connect(self.update_live_preview)
        cfg_layout.addWidget(self.type_combo)

        # Freq, Amp, Noise Controls
        self.freq_slider, self.freq_spin = self.create_input_row(cfg_layout, "Frequency (Hz):", 1, 50, 10)
        self.amp_slider, self.amp_spin = self.create_input_row(cfg_layout, "Amplitude (1-10):", 0, 10, 5)
        self.noise_slider, self.noise_spin = self.create_input_row(cfg_layout, "White Noise (0-5):", 0, 5, 0)

        cfg_box.setLayout(cfg_layout)
        controls.addWidget(cfg_box)

        # Phase Control
        phase_box = QGroupBox("PHASE OFFSET")
        p_lay = QVBoxLayout()
        
        mode_lay = QHBoxLayout()
        self.deg_radio = QRadioButton("Degrees")
        self.rad_radio = QRadioButton("Radians (π)")
        self.deg_radio.setChecked(True)
        self.deg_radio.toggled.connect(self.toggle_phase_mode)
        mode_lay.addWidget(self.deg_radio)
        mode_lay.addWidget(self.rad_radio)
        p_lay.addLayout(mode_lay)

        # Degree UI
        self.phase_deg_container = QWidget()
        deg_h = QHBoxLayout(self.phase_deg_container)
        self.p_deg_slider = QSlider(Qt.Orientation.Horizontal)
        self.p_deg_slider.setRange(0, 360)
        self.p_deg_spin = QSpinBox()
        self.p_deg_spin.setRange(0, 360)
        self.p_deg_slider.valueChanged.connect(self.p_deg_spin.setValue)
        self.p_deg_spin.valueChanged.connect(self.p_deg_slider.setValue)
        self.p_deg_slider.valueChanged.connect(self.update_live_preview)
        deg_h.addWidget(self.p_deg_slider)
        deg_h.addWidget(self.p_deg_spin)
        p_lay.addWidget(self.phase_deg_container)

        # Radian UI
        self.phase_rad_container = QWidget()
        rad_h = QHBoxLayout(self.phase_rad_container)
        self.spin_x = QSpinBox()
        self.spin_x.setRange(-100, 100)
        self.spin_y = QSpinBox()
        self.spin_y.setRange(1, 100)
        self.spin_y.setValue(1)
        self.spin_x.valueChanged.connect(self.update_live_preview)
        self.spin_y.valueChanged.connect(self.update_live_preview)
        rad_h.addWidget(self.spin_x)
        rad_h.addWidget(QLabel(" π / "))
        rad_h.addWidget(self.spin_y)
        self.phase_rad_container.setVisible(False)
        p_lay.addWidget(self.phase_rad_container)

        phase_box.setLayout(p_lay)
        controls.addWidget(phase_box)

        # Buttons
        self.add_btn = QPushButton("ADD SIGNAL TO COMPARISON")
        self.add_btn.setObjectName("addBtn")
        self.add_btn.clicked.connect(self.add_signal)
        controls.addWidget(self.add_btn)

        self.clear_btn = QPushButton("CLEAR ALL DATA")
        self.clear_btn.setObjectName("clearBtn")
        self.clear_btn.clicked.connect(self.clear_signals)
        controls.addWidget(self.clear_btn)

        self.sig_list = QListWidget()
        controls.addWidget(self.sig_list)
        layout.addLayout(controls, 1)

        self.canvas = MplCanvas()
        layout.addWidget(self.canvas, 3)

    def create_input_row(self, layout, label, min_v, max_v, start_v):
        layout.addWidget(QLabel(label))
        row = QHBoxLayout()
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(int(min_v * 100), int(max_v * 100))
        slider.setValue(int(start_v * 100))
        
        spin = QDoubleSpinBox()
        spin.setRange(min_v, max_v)
        spin.setValue(start_v)
        spin.setFixedWidth(80)

        slider.valueChanged.connect(lambda v: spin.setValue(v / 100.0))
        spin.valueChanged.connect(lambda v: slider.setValue(int(v * 100)))
        slider.valueChanged.connect(self.update_live_preview)
        
        row.addWidget(slider)
        row.addWidget(spin)
        layout.addLayout(row)
        return slider, spin

    def toggle_phase_mode(self):
        is_rad = self.rad_radio.isChecked()
        self.phase_deg_container.setVisible(not is_rad)
        self.phase_rad_container.setVisible(is_rad)
        self.update_live_preview()

    def get_phase_data(self):
        if self.deg_radio.isChecked():
            val = self.p_deg_spin.value()
            return np.deg2rad(val), f"{val}°"
        else:
            x, y = self.spin_x.value(), self.spin_y.value()
            return (x * np.pi) / y, f"{x}π/{y}"

    def update_live_preview(self):
        f, a, n = self.freq_spin.value(), self.amp_spin.value(), self.noise_spin.value()
        p_rad, p_str = self.get_phase_data()

        plot_data = []
        # Draw Existing
        for sig in self.active_signals:
            t, y = self.engine.generate(sig)
            plot_data.append((t, y, sig.name))
        
        # Draw Live Preview
        preview = WaveDescriptor("PREVIEW", self.type_combo.currentText(), f, a, p_rad, n)
        t, y = self.engine.generate(preview)
        plot_data.append((t, y, "Adjusting..."))
        self.canvas.plot_signals(plot_data)

    def add_signal(self):
        f = self.freq_spin.value()
        a = self.amp_spin.value()
        n = self.noise_spin.value()
        p_rad, p_str = self.get_phase_data()
        w_type = self.type_combo.currentText()[:3].upper() # SINE -> SIN
        
        count = len(self.active_signals) + 1
        
        # Ultra-compact formatting: ID | TYP | F | A | P | N
        log_name = (
            f"{count:02d}|{w_type}|"
            f"F:{f:>4.1f}|"
            f"A:{a:>4.1f}|"
            f"P:{p_str:>5}|"
            f"N:{n:>3.1f}"
        )
        
        new_sig = WaveDescriptor(log_name, self.type_combo.currentText(), f, a, p_rad, n)
        self.active_signals.append(new_sig)
        
        self.sig_list.addItem(log_name)
        # Automatically resize the list height to fit contents if possible
        self.sig_list.scrollToBottom()

    def clear_signals(self):
        self.active_signals = []
        self.sig_list.clear()
        self.update_live_preview()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SignalGeneratorApp()
    window.show()
    sys.exit(app.exec())