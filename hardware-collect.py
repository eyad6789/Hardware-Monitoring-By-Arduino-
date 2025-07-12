import serial
import time
import psutil
import subprocess
import sys
import os
from datetime import datetime
import json

class PCHardwareMonitor:
    def __init__(self, port='COM3', baudrate=9600):
        """
        Initialize the PC Hardware Monitor for Arduino TFT Display
        
        Args:
            port: Serial port (COM3, COM4, etc. on Windows; /dev/ttyUSB0, /dev/ttyACM0 on Linux)
            baudrate: Serial communication speed
        """
        self.port = port
        self.baudrate = baudrate
        self.serial_connection = None
        self.running = False
        
        # Hardware data
        self.cpu_temp = 0
        self.gpu_temp = 0
        self.cpu_usage = 0
        self.ram_usage = 0
        self.gpu_usage = 0
        self.fps = 60
        
        print("🖥️  PC Hardware Monitor for Arduino TFT Display")
        print("=" * 55)
        self.detect_available_ports()
        
    def detect_available_ports(self):
        """Detect available serial ports"""
        try:
            import serial.tools.list_ports
            ports = serial.tools.list_ports.comports()
            
            print("\n📡 Available serial ports:")
            for port, desc, hwid in sorted(ports):
                print(f"  {port}: {desc}")
            
            if not ports:
                print("  ❌ No serial ports found!")
            print()
        except ImportError:
            print("⚠️  Could not list ports. Please install pyserial: pip install pyserial")
    
    def connect_serial(self):
        """Establish serial connection to Arduino"""
        try:
            self.serial_connection = serial.Serial(self.port, self.baudrate, timeout=1)
            time.sleep(2)  # Wait for Arduino to initialize
            print(f"✅ Connected to Arduino on {self.port}")
            return True
        except serial.SerialException as e:
            print(f"❌ Error connecting to {self.port}: {e}")
            print("   Please check:")
            print("   - Arduino is connected to the correct port")
            print("   - No other program is using the port")
            print("   - Arduino is properly powered")
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False
    
    def get_cpu_temperature(self):
        """Get CPU temperature using multiple methods"""
        try:
            # Method 1: Try psutil sensors (Linux/some Windows systems)
            if hasattr(psutil, "sensors_temperatures"):
                temps = psutil.sensors_temperatures()
                if temps:
                    for name, entries in temps.items():
                        if any(keyword in name.lower() for keyword in ['cpu', 'core', 'processor']):
                            if entries:
                                return max(int(entry.current) for entry in entries if entry.current)
            
            # Method 2: Try OpenHardwareMonitor (Windows)
            try:
                import wmi
                w = wmi.WMI(namespace="root\\OpenHardwareMonitor")
                sensors = w.Sensor()
                for sensor in sensors:
                    if sensor.SensorType == 'Temperature' and 'CPU' in sensor.Name:
                        return int(sensor.Value)
            except:
                pass
            
            # Method 3: Try LibreHardwareMonitor (Windows)
            try:
                import wmi
                w = wmi.WMI(namespace="root\\LibreHardwareMonitor")
                sensors = w.Sensor()
                for sensor in sensors:
                    if sensor.SensorType == 'Temperature' and 'CPU' in sensor.Name:
                        return int(sensor.Value)
            except:
                pass
            
            # Method 4: Try WMI thermal zone (Windows)
            try:
                import wmi
                w = wmi.WMI(namespace="root\\wmi")
                temperature_info = w.MSAcpi_ThermalZoneTemperature()
                if temperature_info:
                    temp_celsius = (temperature_info[0].CurrentTemperature / 10.0) - 273.15
                    return int(temp_celsius)
            except:
                pass
            
            # Fallback: Simulate based on CPU usage
            cpu_load = psutil.cpu_percent(interval=0.1)
            simulated_temp = 35 + (cpu_load * 0.4)
            return int(simulated_temp)
            
        except Exception as e:
            # Return safe default
            return 45
    
    def get_gpu_temperature(self):
        """Get GPU temperature using nvidia-smi and other methods"""
        try:
            # Method 1: NVIDIA GPU via nvidia-smi
            result = subprocess.run(
                ['nvidia-smi', '--query-gpu=temperature.gpu', '--format=csv,noheader,nounits'], 
                capture_output=True, text=True, timeout=5, 
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            if result.returncode == 0:
                temp_str = result.stdout.strip()
                if temp_str and temp_str != '[Not Supported]':
                    return int(float(temp_str))
        except:
            pass
        
        # Method 2: Try OpenHardwareMonitor
        try:
            import wmi
            w = wmi.WMI(namespace="root\\OpenHardwareMonitor")
            sensors = w.Sensor()
            for sensor in sensors:
                if sensor.SensorType == 'Temperature' and 'GPU' in sensor.Name:
                    return int(sensor.Value)
        except:
            pass
        
        # Method 3: Try LibreHardwareMonitor
        try:
            import wmi
            w = wmi.WMI(namespace="root\\LibreHardwareMonitor")
            sensors = w.Sensor()
            for sensor in sensors:
                if sensor.SensorType == 'Temperature' and 'GPU' in sensor.Name:
                    return int(sensor.Value)
        except:
            pass
        
        # Fallback: Return simulated temperature
        return 55
    
    def get_gpu_usage(self):
        """Get GPU usage percentage"""
        try:
            # Method 1: NVIDIA GPU via nvidia-smi
            result = subprocess.run(
                ['nvidia-smi', '--query-gpu=utilization.gpu', '--format=csv,noheader,nounits'], 
                capture_output=True, text=True, timeout=5,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            if result.returncode == 0:
                usage_str = result.stdout.strip()
                if usage_str and usage_str != '[Not Supported]':
                    return int(float(usage_str))
        except:
            pass
        
        # Method 2: Try OpenHardwareMonitor
        try:
            import wmi
            w = wmi.WMI(namespace="root\\OpenHardwareMonitor")
            sensors = w.Sensor()
            for sensor in sensors:
                if sensor.SensorType == 'Load' and 'GPU' in sensor.Name:
                    return int(sensor.Value)
        except:
            pass
        
        # Method 3: Try LibreHardwareMonitor
        try:
            import wmi
            w = wmi.WMI(namespace="root\\LibreHardwareMonitor")
            sensors = w.Sensor()
            for sensor in sensors:
                if sensor.SensorType == 'Load' and 'GPU' in sensor.Name:
                    return int(sensor.Value)
        except:
            pass
        
        # Fallback: Return simulated usage
        return 35
    
    def get_fps(self):
        """Get current FPS - simplified version for Arduino"""
        try:
            # Try to get from OpenHardwareMonitor/LibreHardwareMonitor
            try:
                import wmi
                w = wmi.WMI(namespace="root\\OpenHardwareMonitor")
                sensors = w.Sensor()
                for sensor in sensors:
                    if 'fps' in sensor.Name.lower() or 'framerate' in sensor.Name.lower():
                        return int(sensor.Value)
            except:
                pass
            
            try:
                import wmi
                w = wmi.WMI(namespace="root\\LibreHardwareMonitor")
                sensors = w.Sensor()
                for sensor in sensors:
                    if 'fps' in sensor.Name.lower() or 'framerate' in sensor.Name.lower():
                        return int(sensor.Value)
            except:
                pass
            
            # Estimate FPS based on GPU usage (for demo purposes)
            gpu_usage = self.get_gpu_usage()
            if gpu_usage > 90:
                return 45 + (gpu_usage - 90) * 2  # 45-65 FPS
            elif gpu_usage > 70:
                return 80 + (gpu_usage - 70) * 2  # 80-120 FPS
            elif gpu_usage > 50:
                return 100 + (gpu_usage - 50) * 2  # 100-140 FPS
            else:
                return 144  # Idle/light load
            
        except Exception as e:
            return 60  # Default fallback
    
    def get_system_stats(self):
        """Collect all system statistics"""
        try:
            # Get basic stats
            self.cpu_usage = int(psutil.cpu_percent(interval=0.1))
            self.ram_usage = int(psutil.virtual_memory().percent)
            
            # Get temperatures and GPU stats
            self.cpu_temp = self.get_cpu_temperature()
            self.gpu_temp = self.get_gpu_temperature()
            self.gpu_usage = self.get_gpu_usage()
            self.fps = self.get_fps()
            
            # Ensure all values are within valid ranges
            self.cpu_temp = max(0, min(100, self.cpu_temp))
            self.gpu_temp = max(0, min(100, self.gpu_temp))
            self.cpu_usage = max(0, min(100, self.cpu_usage))
            self.ram_usage = max(0, min(100, self.ram_usage))
            self.gpu_usage = max(0, min(100, self.gpu_usage))
            self.fps = max(0, min(999, self.fps))
            
            return {
                'cpu_temp': self.cpu_temp,
                'gpu_temp': self.gpu_temp,
                'cpu_usage': self.cpu_usage,
                'ram_usage': self.ram_usage,
                'gpu_usage': self.gpu_usage,
                'fps': self.fps
            }
            
        except Exception as e:
            print(f"⚠️  Error collecting system stats: {e}")
            return {
                'cpu_temp': 45,
                'gpu_temp': 55,
                'cpu_usage': 25,
                'ram_usage': 50,
                'gpu_usage': 35,
                'fps': 60
            }
    
    def send_data_to_arduino(self, data):
        """Send formatted data to Arduino"""
        if not self.serial_connection:
            return False
        
        try:
            # Format for Arduino: CPU_Temp,GPU_Temp,CPU_Usage,RAM_Usage,GPU_Usage,FPS
            data_string = f"{data['cpu_temp']},{data['gpu_temp']},{data['cpu_usage']},{data['ram_usage']},{data['gpu_usage']},{data['fps']}\n"
            self.serial_connection.write(data_string.encode())
            self.serial_connection.flush()
            return True
        except Exception as e:
            print(f"❌ Error sending data: {e}")
            return False
    
    def start_monitoring(self):
        """Start the monitoring loop"""
        if not self.connect_serial():
            return
        
        self.running = True
        print("\n" + "="*60)
        print("🚀 PC Hardware Monitor Started!")
        print("="*60)
        print("📊 Monitoring system statistics...")
        print("📡 Sending data to Arduino every second")
        print("🖥️  Check your Arduino TFT display")
        print("⏹️  Press Ctrl+C to stop")
        print("="*60)
        
        consecutive_errors = 0
        max_consecutive_errors = 5
        
        try:
            while self.running:
                # Get system stats
                stats = self.get_system_stats()
                
                # Print to console
                timestamp = datetime.now().strftime("%H:%M:%S")
                print(f"\r[{timestamp}] CPU: {stats['cpu_temp']:2d}°C ({stats['cpu_usage']:2d}%) | "
                      f"GPU: {stats['gpu_temp']:2d}°C ({stats['gpu_usage']:2d}%) | "
                      f"RAM: {stats['ram_usage']:2d}% | FPS: {stats['fps']:3d}", end="", flush=True)
                
                # Send to Arduino
                if self.send_data_to_arduino(stats):
                    consecutive_errors = 0
                else:
                    consecutive_errors += 1
                    if consecutive_errors >= max_consecutive_errors:
                        print(f"\n❌ Too many consecutive errors ({consecutive_errors}). Stopping...")
                        break
                
                time.sleep(1)  # Update every second
                
        except KeyboardInterrupt:
            print("\n\n⏹️  Monitoring stopped by user")
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
        finally:
            self.stop_monitoring()
    
    def stop_monitoring(self):
        """Stop monitoring and close connections"""
        self.running = False
        if self.serial_connection:
            try:
                self.serial_connection.close()
                print("🔌 Serial connection closed")
            except:
                pass
        print("👋 PC Hardware Monitor stopped")

def check_dependencies():
    """Check if required libraries are installed"""
    print("🔍 Checking dependencies...")
    
    required_libs = {
        'serial': 'pyserial',
        'psutil': 'psutil'
    }
    
    missing_libs = []
    
    for lib, pip_name in required_libs.items():
        try:
            __import__(lib)
            print(f"✅ {lib} library found")
        except ImportError:
            print(f"❌ {lib} not found")
            missing_libs.append(pip_name)
    
    # Check optional libraries
    optional_libs = ['wmi']
    for lib in optional_libs:
        try:
            __import__(lib)
            print(f"✅ {lib} library found (optional)")
        except ImportError:
            print(f"⚠️  {lib} not found (optional - for better temperature readings)")
    
    if missing_libs:
        print(f"\n❌ Missing required libraries: {', '.join(missing_libs)}")
        print("Install them with:")
        for lib in missing_libs:
            print(f"  pip install {lib}")
        return False
    
    return True

def main():
    """Main function"""
    print("🖥️  PC Hardware Monitor for Arduino TFT Display v2.1")
    print("=" * 55)
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Please install missing dependencies and try again.")
        return
    
    print("\n📋 Configuration:")
    
    # Get serial port
    while True:
        serial_port = input("Enter Arduino serial port (e.g., COM3, COM8): ").strip()
        if serial_port:
            break
        print("❌ Please enter a valid port.")
    
    baudrate = 9600
    print(f"📡 Using baudrate: {baudrate}")
    
    print("\n" + "="*55)
    print("🔧 Setup Instructions:")
    print("1. Connect your Arduino with TFT display")
    print("2. Upload the Arduino sketch to your board")
    print("3. Make sure the TFT display is wired correctly")
    print("4. The display should show 'Waiting for PC data...'")
    print("=" * 55)
    
    # Create monitor instance
    monitor = PCHardwareMonitor(port=serial_port, baudrate=baudrate)
    
    # Start monitoring
    monitor.start_monitoring()

if __name__ == "__main__":
    main()