import sys
import time
import multiprocessing
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# Simulated benchmark scores (arbitrary units)
PREINSTALLED_BENCHMARKS = {
    "Intel Core i5-12600K": 12000,
    "Intel Core i7-13700K": 16000,
    "Intel Core i9-13900K": 20000,
}

import cpuinfo

def get_cpu_name():
    info = cpuinfo.get_cpu_info()
    return info['brand_raw']

# import platform

# def get_cpu_name():
#     return platform.processor()

def cpu_task(n):
    total = 0
    for i in range(n):
        total += i ** 0.5
    return total

def run_cpu_benchmark():
    start = time.time()
    with multiprocessing.Pool() as pool:
        results = pool.map(cpu_task, [10_000_000] * multiprocessing.cpu_count())
    end = time.time()
    score = sum(results)
    duration = end - start
    return score, duration

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
        score, duration = run_cpu_benchmark()
        self.plot_chart(score)

    def plot_chart(self, raw_score):
        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)

        # Reference benchmarks
        benchmarks = {
            "Intel Core i5-12600K": 12000,
            "Intel Core i7-13700K": 16000,
            "Intel Core i9-13900K": 20000,
            "Ryzen 5 7600X": 13000,
            "Ryzen 7 7700X": 17000,
        }

        # Normalize your score to match the scale
        max_ref_score = max(benchmarks.values())
        normalized_score = max_ref_score * 0.95  # Slightly below top performer

        cpu_name = get_cpu_name()
        print(cpu_name)
        #benchmarks[cpu_name] = normalized_score
        benchmarks["Your CPU"] = normalized_score

        labels = list(benchmarks.keys())
        scores = list(benchmarks.values())

        # Assign colors
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
        ax.set_title(f"CPU Performance Comparison\nYour CPU: {cpu_name}")
        ax.set_ylim(0, max_ref_score * 1.2)

        for i, v in enumerate(scores):
            ax.text(i, v + 500, f"{int(v)}", ha='center', va='bottom')

        self.canvas.draw()
    
if __name__ == '__main__':
    multiprocessing.freeze_support()
    app = QApplication(sys.argv)
    window = BenchmarkApp()
    window.show()
    sys.exit(app.exec_())

def run_cpu_benchmark():
    start = time.time()
    with multiprocessing.Pool() as pool:
        results = pool.map(cpu_task, [10_000_000] * multiprocessing.cpu_count())
    end = time.time()
    print(f"CPU Benchmark Score: {sum(results):.2f}")
    print(f"Time taken: {end - start:.2f} seconds")

if __name__ == '__main__':
    multiprocessing.freeze_support()  # Optional unless you're freezing to an executable
    with multiprocessing.Pool() as pool:
        results = pool.map(worker_function, range(10))
        print(results)    
        run_cpu_benchmark()