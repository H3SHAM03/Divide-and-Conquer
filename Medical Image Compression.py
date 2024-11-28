from PIL import Image
import numpy as np

def is_uniform(block, tolerance=10):
    """
    Check if a block is uniform within a given tolerance.
    """
    avg_color = np.mean(block, axis=(0, 1))
    return np.all(np.abs(block - avg_color) < tolerance)

def compress_image(image, x, y, size, tolerance=10):
    """
    Recursively compress the image using a quadtree approach.
    """
    block = image[y:y+size, x:x+size]
    
    if size == 1 or is_uniform(block, tolerance):
        # Return the average color if the block is uniform or size is 1 pixel.
        avg_color = np.mean(block, axis=(0, 1)).astype(int)
        return {"color": avg_color.tolist()}
    
    half = size // 2
    return {
        "top_left": compress_image(image, x, y, half, tolerance),
        "top_right": compress_image(image, x + half, y, half, tolerance),
        "bottom_left": compress_image(image, x, y + half, half, tolerance),
        "bottom_right": compress_image(image, x + half, y + half, half, tolerance),
    }

def decompress_image(compressed, size):
    """
    Reconstruct the image from the compressed structure.
    """
    image = np.zeros((size, size, 3), dtype=np.uint8)

    def fill_image(x, y, size, node):
        if "color" in node:
            # Assign the color to the block
            image[y:y+size, x:x+size] = np.array(node["color"])[np.newaxis, np.newaxis, :]
        else:
            # Recursively fill sub-blocks
            half = size // 2
            fill_image(x, y, half, node["top_left"])
            fill_image(x + half, y, half, node["top_right"])
            fill_image(x, y + half, half, node["bottom_left"])
            fill_image(x + half, y + half, half, node["bottom_right"])


    fill_image(0, 0, size, compressed)
    return image



import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSlider, QFileDialog, QWidget
)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import numpy as np

class ImageCompressionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Medical Image Compression")
        self.setGeometry(200, 200, 800, 600)
        
        self.initUI()
        self.image = None
        self.compressed = None
    
    def initUI(self):
        central_widget = QWidget()
        layout = QVBoxLayout()
        
        # Image displays
        self.original_label = QLabel("Original Image")
        self.compressed_label = QLabel("Compressed Image")
        image_layout = QHBoxLayout()
        image_layout.addWidget(self.original_label)
        image_layout.addWidget(self.compressed_label)
        layout.addLayout(image_layout)
        
        # Load button
        load_button = QPushButton("Load Image")
        load_button.clicked.connect(self.load_image)
        layout.addWidget(load_button)
        
        # Compression slider
        self.tolerance_slider = QSlider(Qt.Horizontal)
        self.tolerance_slider.setRange(1, 50)
        self.tolerance_slider.setValue(10)
        self.tolerance_slider.setTickInterval(5)
        self.tolerance_slider.setTickPosition(QSlider.TicksBelow)
        layout.addWidget(self.tolerance_slider)
        
        # Compress button
        compress_button = QPushButton("Compress Image")
        compress_button.clicked.connect(self.compress_image)
        layout.addWidget(compress_button)
        
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
    
    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Images (*.png *.jpg *.bmp)")
        if file_name:
            self.image = Image.open(file_name)
            self.original_label.setPixmap(QPixmap(file_name).scaled(300, 300, Qt.KeepAspectRatio))
    
    def compress_image(self):
        if self.image is not None:
            tolerance = self.tolerance_slider.value()
            image_array = np.array(self.image)
            size = image_array.shape[0]
            compressed = compress_image(image_array, 0, 0, size, tolerance)
            self.compressed = decompress_image(compressed, size)
            
            # Display the compressed image
            qimage = QImage(self.compressed.data, size, size, QImage.Format_RGB888)
            self.compressed_label.setPixmap(QPixmap.fromImage(qimage).scaled(300, 300, Qt.KeepAspectRatio))

# Run the app
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageCompressionApp()
    window.show()
    sys.exit(app.exec_())
