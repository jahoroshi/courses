# 🖥️ System Monitoring in Python

This project provides functionality for monitoring system resources such as CPU load, memory usage, swap, and disk usage. The project uses the `psutil` library and tools to display data in the console.

## 🛠️ Technologies and Libraries Used

- **psutil** — for gathering system resource information.
- **json** — for data storage and configuration.
- **time** — for working with time intervals.

## 🎯 Project Goals

The goal of this project is to:

1. Retrieve and display information about CPU load, memory, and disk usage in real-time.
2. Use Python to create system utilities and monitoring tools.
3. Work with the **psutil** library to access system resource data.
4. Develop console applications with dynamic output.

## 📂 Project Structure

- **`main.py`** — the main module that controls the display of system information and the program loop.
- **`get_info.py`** — the module responsible for gathering data on system resources (CPU, memory, disks).
- **`dsp_info.py`** — the module for visualizing data in the console.

## 🚀 Key Features

- **CPU Monitoring** — displays the usage of each CPU core in real-time with color-coded indicators.
- **Memory Status** — shows the used and available RAM and swap memory.
- **Disk Information** — outputs disk usage, including used and free space, in a graphical format.

## 📊 Features of Graphical Representation

- **Innovative Approach**: The graphical representation of the system’s status is done in the form of a vertical equalizer that dynamically reflects CPU load.
- **Visual Indicator**: The vertical indicator is a series of bars that adjust their height according to the current CPU load, creating a “pulse” effect.
- **No External Modules**: The equalizer is implemented without using any external graphical libraries, demonstrating a deep understanding of programming and algorithmic skills.
- **Algorithmic Foundation**: The display is based on an algorithm that uses a matrix as a field for visualizing data. This allows the information to be shown directly in the terminal using symbols to create colored blocks.
- **Real-Time Updates**: The system updates data every five seconds, providing current and accurate CPU status.
- **Equalizer Transition**: New CPU load metrics are added to the top of the stack, and the last entry is removed, creating a continuous flow of data.
- **Work Demonstration**: A video demonstration of the program in action is included in the repository to showcase the project’s functionality.

---

This project is designed to practice working with system utilities and the psutil library, as well as to learn how to create console applications with dynamic data visualization.
