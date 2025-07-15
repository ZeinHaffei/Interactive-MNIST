# Live MNIST Digit Predictor 🎨🔢

A user-friendly interactive app that lets you **draw a digit (0-9)** in a grid and instantly see how a neural network (CNN, trained on MNIST) predicts what number you wrote—complete with real-time probability graphs!

---

## ✨ Features

- **Interactive Drawing:** Draw a digit with your mouse in a 28×28 pixel grid.
- **Live Prediction:** The neural network predicts your digit every 0.3 seconds.
- **Probability Bar Chart:** Visualizes the probability for each digit (0-9) in real-time.
- **Instant Reset:** Clear the canvas at any time.
- **No Internet Required:** Trains a simple CNN model on MNIST locally if not already present.
- **Easy to Run:** Simple Python dependencies, works on Windows, Linux, or Mac.

---

## 🖼️ Preview

!(https://raw.githubusercontent.com/ZeinHaffei/Interactive-MNIST/main/assets/1.png)

---

## 🚀 Installation

1. **Clone this repo:**

   ```bash
   git clone https://github.com/your-ZeinHaffei/mnist-live-predictor.git
   cd mnist-live-predictor
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

   Or, manually:

   ```bash
   pip install tensorflow numpy matplotlib
   ```

3. *(Optional but recommended)*\
   Download the pre-trained model `mnist_model.h5` from the release page or let the app train it for you on first run.

---

## 🕹️ Usage

```bash
python mnist_gui.py
```

- Draw a digit (0-9) in the grid using your mouse.
- The model predicts what you drew and updates the probability graph below.
- Click **Clear** to erase and try again!

---

## ⚙️ How It Works

- If `mnist_model.h5` (trained model) exists, loads it for fast startup.
- If not, automatically trains a small CNN on the MNIST dataset (\~3 epochs, takes \~1-2 minutes), then saves the model for next time.
- The drawing grid data is continuously fed to the model for prediction.

---

## 📦 Requirements

- Python 3.7+
- [TensorFlow](https://www.tensorflow.org/) (`pip install tensorflow`)
- [NumPy](https://numpy.org/)
- [Matplotlib](https://matplotlib.org/)

See [`requirements.txt`](requirements.txt) for details.

---

## 🛠️ Troubleshooting

- **Slow startup?**\
  The first run trains the model if `mnist_model.h5` is missing. You can reuse the saved model next time.
- **No window appears?**\
  Make sure you are running a local Python installation with GUI support (not in a headless server).
- **Pip errors?**\
  Upgrade pip: `python -m pip install --upgrade pip`

---

## 🧑‍💻 Author

- [Zein Al Haffei](https://github.com/ZeinHaffei)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

*Inspired by neural network visualizations and interactive AI demos!*

