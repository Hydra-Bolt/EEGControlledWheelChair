# EEG Signal Processing and Wheelchair Control

<div align = "center">
        <a href="https://ibb.co/6XB74yY" target="_blank">
            <img src="https://i.ibb.co/wcsFKdy/dataset-cover.jpg" alt="dataset-cover">
        </a>
    </div>
   
## Overview
This project focuses on utilizing EEG (Electroencephalography) signals for controlling the movement of a wheelchair. EEG signals are recorded from the brain and processed to detect specific patterns associated with various mental activities, such as thinking about moving left, right, forward, or backward. These detected patterns are then used to control the direction of the wheelchair accordingly.

## Features
- **Real-time EEG Signal Processing**: The system captures EEG signals in real-time and processes them to extract relevant features.
- **Machine Learning Classification**: Extracted features are classified using a Random Forest classifier to determine the intended movement direction.
- **Serial Communication with Wheelchair**: Upon classification, the detected movement command is sent via serial communication to the wheelchair control system.

## Getting Started
Follow these instructions to set up and run the EEG signal processing and wheelchair control system:

### Prerequisites
- Arduino board with appropriate EEG sensor(s) connected.
- Python 3.x installed on your system.
- Required Python libraries installed (NumPy, pandas, scikit-learn, matplotlib, seaborn, joblib, scipy).

### Installation
1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/Hydra-Bolt/EEGControlledWheelChair.git
   ```

2. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

### Usage
1. Connect the EEG sensor(s) to the Arduino board and ensure it is properly calibrated.
2. Upload the Arduino script (`SerialConnection.ino`) to the Arduino board.
3. Adjust the COM port and baud rate in the `SerialConnection.py` script.
4. Run the Python script `SerialConnection.py` to start capturing and processing EEG signals:
   ```bash
   python SerialConnection.py
   ```
5. Monitor the console for classification results and ensure the wheelchair moves accordingly.


## Contributing
Contributions are welcome! Please feel free to fork the repository, make changes, and submit a pull request.

### Pending Contributions

- **Web interface**: Imploying a web interface will be welcomed to better visualize the signals comming from the bioamp
- **Model**: Using GNN, RNN or a more complex ML model to improve the recall and accuracy will also be welcomed
  
## License
EEG WheelChair Control © 2024 by Mind Mobilizers is licensed under [Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/)

## Acknowledgements
- This project is a part of the EEG Wheelchair project of Mind Mobilizers


