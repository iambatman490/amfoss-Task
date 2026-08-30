# Grand Line Process Monitor

A simple terminal-based system monitoring tool built in Python. Inspired by utilities like `htop`, it gives a live view of active processes ("ships") running on the system, showing their resource usage and allowing process termination directly from the interface.
## Approach
1. **Fetching System Data:**
   The tool reads active process information directly from the Linux `/proc` virtual filesystem and system utilities (using Python's `psutil` library). It gathers:
    Process ID (PID)
    Process Name
    CPU Usage percentage
    Memory Usage percentage
    Total active process count
2. **User Interaction & Process Control:**
   - Uses non-blocking keyboard input.
   - Users can scroll up and down through the process list using arrow keys.
   - Allows sending a termination signal (`SIGTERM`) to kill a selected process.
### 1. Virtual Environment Setup
# Clone the repository
git clone https://github.com/iambatman490/amfoss-Task
cd amfoss-Task
# Install dependencies
pip install -r requirements.txt
