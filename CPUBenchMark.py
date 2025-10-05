import sys
import time
import multiprocessing
import cpuinfo
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# Reference benchmark scores
REFERENCE_BENCHMARKS = {
    "Intel Core i5-12600K": 12000,
    "Intel Core i7-13700K": 16000,
    "Intel Core i9-13900K": 20000,
    "Ryzen 5 7600X": 13000,
    "Ryzen 7 7700X": 17000,
}

# ✅ Top-level function for multiprocessing (Windows-safe)
def cpu_task(n):
    total = 0
    for i in range(n):
        total += i * i
    return total

# ✅ Benchmark logic
def run_benchmark():
    start = time.time()
    with multiprocessing.Pool() as pool:
        pool.map(cpu_task, [10_000_000] * multiprocessing.cpu_count())
    end = time.time()

    duration = end - start
    reference_duration = 2.0  # Assume i9 takes ~2 seconds
    score = int((reference_duration / duration) * 20000)
    return score, duration

# ✅ GUI class
class BenchmarkApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CPU Benchmark Viewer")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()
        self.button = QPushButton("Run Benchmark")
        self.button.clicked.connect(self.run_benchmark)

        self.canvas = FigureCanvas(Figure(figsize=(6, 4)))
        layout.addWidget(self.button)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def run_benchmark(self):
        score, duration = run_benchmark()
        print(f"Raw benchmark score: {score}, Duration: {duration:.2f}s")
        self.plot_chart(score)

    def plot_chart(self, raw_score):
        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)

        benchmarks = REFERENCE_BENCHMARKS.copy()
        cpu_name = cpuinfo.get_cpu_info()['brand_raw']
        benchmarks["Your CPU"] = raw_score

        labels = list(benchmarks.keys())
        scores = list(benchmarks.values())

        colors = []
        for label in labels:
            if "Ryzen" in label:
                colors.append("orange")
            elif "Your CPU" in label:
                colors.append("blue")
            else:
                colors.append("gray")

        ax.bar(range(len(scores)), scores, color=colors)
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels, rotation=30, ha='right')
        ax.set_ylabel("Benchmark Score")
        ax.set_title(f"CPU Performance Comparison\nYour CPU: {cpu_name} – Score: {int(raw_score)}")
        ax.set_ylim(0, max(scores) * 1.2)

        for i, v in enumerate(scores):
            ax.text(i, v + 500, f"{int(v)}", ha='center', va='bottom')

        self.canvas.draw()

# ✅ Entry point
if __name__ == '__main__':
    multiprocessing.freeze_support()  # Required for Windows
    app = QApplication(sys.argv)
    window = BenchmarkApp()
    window.show()
    sys.exit(app.exec_())