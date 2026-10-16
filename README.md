
# GestureFlow AI

### Real-Time Hand Gesture Recognition and Smart Action Engine

GestureFlow AI is a real-time computer vision application that recognizes hand gestures through a camera and maps them to predefined actions. Built using Python, OpenCV, and MediaPipe, the system detects hand landmarks, identifies gestures using geometric rules, and displays the results through a live visual interface.

The project demonstrates how human-computer interaction can be made more intuitive through contactless gesture recognition.

## ✨ Features

- **Real-Time Hand Tracking:** Detects and tracks hand landmarks using MediaPipe.
- **Six Gesture Categories:** Recognizes Open Palm, Fist, Thumbs Up, Peace, Pointing, and Pinch.
- **Smart Action Mapping:** Maps recognized gestures to predefined simulated actions.
- **Live Gesture Dashboard:** Displays the detected gesture, heuristic score, and tracking status.
- **Performance Monitoring:** Shows live FPS information.
- **Action History:** Displays recent triggered actions.
- **Session Statistics:** Tracks gesture counts during the current session.
- **Cooldown Mechanism:** Helps prevent repeated action triggers when a gesture is held.
- **Session Reset:** Reset gesture statistics and action history using a keyboard shortcut.
- **Flexible Camera Input:** Supports compatible webcams and a DroidCam virtual camera when available to OpenCV.

## 🖐️ Supported Gestures

| Hand Gesture | Simulated Action |
|---|---|
| Open Palm | Play |
| Fist | Pause |
| Thumbs Up | Volume Up |
| Peace | Next Slide |
| Pointing | Previous Slide |
| Pinch | Select |

**Note:** Actions are currently simulated and displayed in the interface. Actual media playback, system volume adjustment, and PowerPoint control are not implemented.

## 🛠️ Technology Stack

- **Programming Language:** Python
- **Computer Vision:** OpenCV
- **Hand Landmark Detection:** MediaPipe
- **Numerical Computing:** NumPy
- **Interface:** OpenCV real-time display window
- **Development Environment:** Visual Studio Code

## 📁 Project Structure

```text
Syntecxhub_GestureFlowAI/
├── app.py
├── gestureflow/
│   ├── __init__.py
│   ├── recognizer.py
│   └── actions.py
├── requirements.txt
├── README.md
└── .gitignore
```

The `gestureflow/__init__.py` file is optional and may be included if present in the project.

## ⚙️ Installation and Setup

### Prerequisites

- Windows 10 or Windows 11
- Python 3.12
- A compatible webcam or virtual camera
- Git (optional, for cloning the repository)

### 1. Clone the Repository

```bash
git clone https://github.com/tusharganvekar1234/Syntecxhub_GestureFlowAI.git
cd Syntecxhub_GestureFlowAI
```

### 2. Create a Virtual Environment

```powershell
py -3.12 -m venv .venv
```

### 3. Activate the Virtual Environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```powershell
python -m pip install -r requirements.txt
```

### 5. Run the Application

```powershell
python app.py
```

The application opens a camera window and begins detecting hand gestures in real time.

## 🎮 Keyboard Controls

| Key | Function |
|---|---|
| Q | Quit the application |
| R | Reset session statistics and recent action history |

## 🔍 How It Works

1. **Video Capture:** OpenCV captures frames from the selected camera.
2. **Hand Detection:** MediaPipe identifies hand landmarks in each frame.
3. **Gesture Recognition:** The recognizer uses hand landmark geometry to classify the observed pose.
4. **Gesture Smoothing:** A short history of recent predictions helps stabilize the displayed gesture.
5. **Action Processing:** The action engine maps recognized gestures to predefined actions and applies a cooldown.
6. **Visual Feedback:** The interface displays the gesture, heuristic score, tracking status, FPS, recent actions, and session counts.

## 📊 Interface Information

The live interface displays:

- Current detected gesture
- Heuristic recognition score
- Hand tracking status
- Frames per second (FPS)
- Total triggered actions
- Recent action events
- Gesture counts for the current session
- Temporary action notifications

The displayed heuristic score is a rule-based score, not a calibrated probability or validated accuracy measurement.

## ⚠️ Limitations

- Gesture recognition can be affected by lighting, camera quality, background conditions, and hand orientation.
- Geometric rules may misclassify gestures in certain hand positions.
- Gesture smoothing may introduce a small delay before the displayed gesture changes.
- The system has not been evaluated on a formal labelled test dataset.
- Actions are simulated rather than connected to external applications.
- Performance depends on the device, camera, and processing conditions.

## 🚀 Future Improvements

- Integrate actual media playback and presentation controls.
- Add configurable gesture-to-action mappings.
- Improve recognition robustness under different lighting conditions.
- Evaluate performance using a labelled gesture dataset.
- Add camera selection and adjustable recognition settings.
- Develop a standalone graphical user interface.
- Explore machine-learning-based gesture classification.

## 🎯 Project Objective

The objective of GestureFlow AI is to demonstrate a practical application of computer vision for touch-free human-computer interaction. The project combines hand landmark detection, rule-based gesture recognition, action mapping, and real-time visual feedback in a single application.

## 👨‍💻 Author

**Tushar G. Anvekar**

GitHub: [@tusharganvekar1234](https://github.com/tusharganvekar1234)

Developed as a hand gesture recognition project for the Syntecxhub internship.

## 📄 License

No license has been specified for this project. Please add a `LICENSE` file if you decide to distribute it under an open-source license.
