import tkinter as tk
import numpy as np
import tensorflow as tf
import threading
import time
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Suppress TensorFlow logs
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Load or create a simple CNN model trained on MNIST
try:
    model = tf.keras.models.load_model('mnist_model.h5')
except:
    from tensorflow.keras.datasets import mnist
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    x_train, x_test = x_train / 255.0, x_test / 255.0
    x_train = x_train.reshape(-1,28,28,1)
    x_test = x_test.reshape(-1,28,28,1)

    model = Sequential([
        Conv2D(16, (3,3), activation='relu', input_shape=(28,28,1)),
        MaxPooling2D(2,2),
        Flatten(),
        Dense(64, activation='relu'),
        Dense(10, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.fit(x_train, y_train, epochs=3, validation_data=(x_test, y_test))
    model.save('mnist_model.h5')

class MNISTApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Live MNIST Predictor")
        self.configure(bg='white')
        self.resizable(False, False)

        self.grid_size = 28
        self.cell_size = 10
        self.canvas_size = self.grid_size * self.cell_size

        # Create a grid canvas
        self.canvas = tk.Canvas(self, width=self.canvas_size, height=self.canvas_size, bg='white')
        self.canvas.pack(pady=10)

        self.cells = np.zeros((self.grid_size, self.grid_size))
        self.rectangles = {}

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x1 = j * self.cell_size
                y1 = i * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, outline='gray', fill='white')
                self.rectangles[(i,j)] = rect

        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<Button-1>", self.paint)

        # Prediction label
        self.prediction_label = tk.Label(self, text="Prediction: ", font=("Arial", 24), bg="white")
        self.prediction_label.pack(pady=10)

        # Clear Button
        self.clear_button = tk.Button(self, text="Clear", command=self.clear)
        self.clear_button.pack()

        # Setup probability graph
        self.figure = Figure(figsize=(6, 2), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.bar_canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.bar_canvas.get_tk_widget().pack(pady=10)

        self.running = True
        self.after(100, self.update_prediction)  # Start prediction after 0.5 sec

    def paint(self, event):
        x, y = event.x, event.y
        if 0 <= x < self.canvas_size and 0 <= y < self.canvas_size:
            j = x // self.cell_size
            i = y // self.cell_size
            self.cells[i, j] = 1.0
            self.canvas.itemconfig(self.rectangles[(i,j)], fill='black')

    def clear(self):
        self.cells = np.zeros((self.grid_size, self.grid_size))
        for rect in self.rectangles.values():
            self.canvas.itemconfig(rect, fill='white')
        self.prediction_label.config(text="Prediction: ")
        self.ax.clear()
        self.bar_canvas.draw()

    def update_prediction(self):
        if not self.running:
            return

        img = np.copy(self.cells)

        # 🛠️ Check if drawing is empty:
        if np.sum(img) == 0:
            self.prediction_label.config(text="Prediction: (waiting...)")
            self.ax.clear()
            self.bar_canvas.draw()
        else:
            img = img.reshape(1, 28, 28, 1)
            pred = model.predict(img, verbose=0)[0]
            number = np.argmax(pred)

            # Update text
            self.prediction_label.config(text=f"Prediction: {number}")

            # Update graph
            self.ax.clear()
            self.ax.bar(range(10), pred, color='lightblue')
            self.ax.set_ylim([0, 1])
            self.ax.set_xticks(range(10))
            self.bar_canvas.draw()

        # Repeat prediction after 300ms
        self.after(300, self.update_prediction)

    def on_closing(self):
        self.running = False
        self.destroy()

if __name__ == "__main__":
    app = MNISTApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
