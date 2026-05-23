⚡ Simple Signal Generator (SSG): Pro Multi-Wave Generator

Python GUI License

✨ Key Features

  - 🌊 Diverse Waveform Engine: Generate Sine, Square, Sawtooth, and Triangle
    waves with high-fidelity sampling.
  - 🎛️ Dual-Control Interface: Every parameter has a smooth Sleek Slider for
    quick adjustments and a Precision Manual Box for exact numerical entry.
  - 📐 Fractional \pi Phase Control: Switch between standard degrees (0-360°) and
    mathematical radians using fractional \pi inputs (e.g., 3\pi/4).
  - 🔊 White Noise Injection: Add a variable "Noise Floor" to simulate real-world
    interference and electronic static.
  - 📊 Multi-Signal Comparison: Add multiple signals to the plot to compare
    different frequencies and phases simultaneously.
  - 📑 Compact Digital Log: A monospaced technical log that tracks all active
    signals in a dense, easy-to-read table.
  - 🌙 Midnight UI: A custom-designed CSS (QSS) dark theme optimized for long
    engineering sessions.

🛠️ Tech Stack

  - Language: Python 3.x
  - GUI Framework: PyQt6 (Professional window management)
  - Math Engine: NumPy & SciPy (High-speed signal calculation)
  - Plotting Engine: Matplotlib (Scientific-grade graphing)

🚀 Installation & Getting Started

1. Clone the repository

git clone https://github.com/TheEIi/signal-generator-project.git
cd signal-generator-project

2. Install Dependencies

Make sure you have Python installed, then run:

pip install -r requirements.txt

3. Launch the Application

python main.py

📖 How to Use

1.  Configure the Signal: Select your waveform type from the dropdown (e.g.,
    Sine).
2.  Adjust Parameters:
      - Move the Frequency slider or type the value (1-50 Hz).
      - Set the Amplitude (1-10 V).
      - Add some White Noise if you want to test signal interference.
3.  Set the Phase:
      - Select Degrees to shift by angle.
      - Select Radians and enter X and Y to shift by \frac{X\pi}{Y}.
4.  Compare:
      - The "Preview" line shows your current adjustments.
      - Click 🟢 ADD SIGNAL TO PLOT to lock it in and start configuring a second
        wave for comparison.
5.  Analyze: View the Compact Log at the bottom left to see exact technical data
    for every active channel.

📁 Project Structure

  - main.py 🧠 — The Controller & View. Handles the GUI layout, dark theme
    styling, and button interactions.
  - signal_engine.py 🔢 — The Math Engine. Contains the logic for NumPy wave
    generation and noise injection.
  - plot_canvas.py 📉 — The Graphing Bridge. Integrates Matplotlib into the PyQt6
    window with dark-mode styling.
  - requirements.txt 📦 — List of all necessary libraries.

🤝 Contributing

Contributions are welcome!
Feel free to fork the repo and submit a Pull Request.

📜 License

This project is licensed under the MIT License

Developed with ❤️ for the Engineering Community.
