"""
<plugin 
    key="MoonrakerDomoticz" 
    name="Moonraker 3D Printer Monitoring"
    version="1.3"
    author="Klym Tatarnikov"
    externallink="https://github.com/klym-tatarnikov/MoonrakerDomoticz">
   
    <description>
        <h2>Moonraker 3D Printer Monitoring Plugin for Domoticz</h2>
        <br/>
        This plugin monitors Moonraker-based 3D printers (Klipper firmware) and provides real-time data integration with Domoticz home automation system.
        <br/><br/>
        <h3>Features:</h3>
        <ul>
            <li><b>Real-time Temperature Monitoring:</b> Extruder, bed, chamber, CPU, and MCU temperatures</li>
            <li><b>Job Status Tracking:</b> Complete printer state monitoring with selector switch (idle, printing, paused, completed, etc.)</li>
            <li><b>Print Job Information:</b> Current job name and estimated time remaining</li>
            <li><b>Historical Statistics:</b> Total jobs, print time, filament usage, and longest print records</li>
            <li><b>Remote Shutdown:</b> Safely shutdown the printer system via Domoticz switch</li>
            <li><b>Connection Monitoring:</b> Automatic detection of printer availability</li>
        </ul>
        <br/>
        <h3>Requirements:</h3>
        <ul>
            <li>Moonraker API enabled on your 3D printer</li>
            <li>Network connectivity between Domoticz and printer</li>
            <li>Python requests library</li>
        </ul>
        <br/>
        Compatible with popular 3D printer firmwares using Moonraker: Klipper, Mainsail, Fluidd
    </description>
    <params>
        <param field="Address" label="Moonraker API Address" width="300px" required="true" default="localhost"/>
        <param field="Port" label="Port" width="300px" required="true" default="7125"/>
        <param field="Mode1" label="Polling Interval (seconds)" width="75px" required="true" default="10"/>
        <param field="Mode6" label="Logging" width="75px">
            <options>
                <option label="Verbose" value="Verbose"/>
                <option label="Debug" value="Debug"/>
                <option label="Normal" value="Normal" default="true"/>
            </options>
        </param>
    </params>
</plugin>
"""

import Domoticz
import requests
import subprocess
import platform


class BasePlugin:
    def __init__(self):
        self.moonraker_url = None
        self.poll_interval = 10
        self.sensor_keys = {
            # Temperature sensors (Temperature Sensor type)
            "extruder_temp": ("Extruder Temperature", "Temperature Sensor", "°C"),
            "bed_temp": ("Bed Temperature", "Temperature Sensor", "°C"),
            "chamber_temp": ("Chamber Temperature", "Temperature Sensor", "°C"),
            "cpu_temp": ("CPU Temperature", "Temperature Sensor", "°C"),
            "mcu_temp": ("Motherboard MCU Temperature", "Temperature Sensor", "°C"),
            "printhead_mcu_temp": ("Printhead MCU Temperature", "Temperature Sensor", "°C"),
            # Job status
            "job_status": ("Job Status", "Selector Switch", ""),
            "time_left": ("Time Left (min)", "Text", "min"),
            "job_name": ("Job Name", "Text", ""),
            # Historical stats (Custom Sensor devices with UOM)
            "total_jobs": ("Total Jobs Printed", "Custom Sensor", ""),
            "total_time": ("Total Printer Time (h)", "Custom Sensor", "h"),
            "total_print_time": ("Total Print Time (h)", "Custom Sensor", "h"),
            "total_filament_used": ("Total Filament Used (m)", "Custom Sensor", "m"),
            "longest_job": ("Longest Print Job (h)", "Custom Sensor", "h"),
            "longest_print": ("Longest Continuous Print (h)", "Custom Sensor", "h"),
            # Control switches
            "shutdown_switch": ("Shutdown Printer", "Switch", "")

        }
        
        # Define job status levels for selector switch - all possible Moonraker statuses
        self.job_status_levels = {
            "unknown": 0,
            "idle": 10,
            "ready": 20,
            "standby": 30,
            "printing": 40,
            "paused": 50,
            "complete": 60,
            "completed": 70,
            "cancelled": 80,
            "error": 90
        }

    def onStart(self):
        Domoticz.Log("Moonraker Plugin Starting...")
        self.moonraker_url = f"http://{Parameters['Address']}:{Parameters['Port']}"
        self.poll_interval = int(Parameters["Mode1"])

        # Create devices if not exist
        for idx, (key, (label, dev_type, uom)) in enumerate(self.sensor_keys.items(), start=1):
            Domoticz.Debug(f"Checking device {idx}: {label} ({dev_type}) - Exists: {idx in Devices}")
            if idx not in Devices:
                if dev_type == "Custom Sensor":
                    Domoticz.Device(Name=label, Unit=idx, TypeName="Custom", Options={"UOM": uom}).Create()
                elif dev_type == "Temperature Sensor":
                    Domoticz.Device(Name=label, Unit=idx, TypeName="Temperature", Options={"UOM": uom}).Create()
                elif dev_type == "Text":
                    Domoticz.Device(Name=label, Unit=idx, TypeName="Text").Create()
                elif dev_type == "Switch":
                    Domoticz.Device(Name=label, Unit=idx, TypeName="Switch").Create()
                elif dev_type == "Selector Switch":
                    # Create selector switch with all possible job status options
                    options = {"LevelActions": "|||||||||", 
                              "LevelNames": "unknown|idle|ready|standby|printing|paused|complete|completed|cancelled|error",
                              "LevelOffHidden": "false",
                              "SelectorStyle": "1"}
                    Domoticz.Device(Name=label, Unit=idx, TypeName="Selector Switch", 
                                  Options=options).Create()
                Domoticz.Log(f"Created device: {label} ({dev_type})")
            else:
                Domoticz.Debug(f"Device already exists: {label} ({dev_type})")

        Domoticz.Heartbeat(self.poll_interval)

    def onHeartbeat(self):
        if self.is_host_alive(Parameters['Address']):
            self.fetchPrinterStatus()
            self.fetchPrinterHistory()
        else:
            Domoticz.Debug(f"{Parameters['Address']} is not reachable")
            # Set job status to "unknown" (level 0) when printer is not reachable
            for idx, (key, (label, dev_type, uom)) in enumerate(self.sensor_keys.items(), start=1):
                if key == "job_status" and idx in Devices:
                    Devices[idx].Update(nValue=0, sValue="0")  # Set to "unknown" level
                    Domoticz.Debug("Updated Job Status to 'unknown' - printer not reachable")
                    break
    
    def is_host_alive(self, host):
        """Returns True if the host is reachable, False otherwise."""
        # Choose the correct ping command based on OS
        param = "-n" if platform.system().lower() == "windows" else "-c"
        command = ["ping", param, "1", host]
    
        try:
            output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return output.returncode == 0  # 0 means success
        except Exception as e:
            print(f"Error: {e}")
            return False

    def fetchPrinterStatus(self):
        """Fetch real-time printer status and temperatures from Moonraker."""
        try:
            query_url = f"{self.moonraker_url}/printer/objects/query?print_stats&heater_bed&extruder&heater_generic chamber&temperature_host CPU&temperature_sensor CPU&temperature_sensor Motherboard MCU&temperature_sensor Printhead MCU"
            response = requests.get(query_url, timeout=5)
            response.raise_for_status()
            data = response.json().get("result", {}).get("status", {})

            # Extract values
            job_status = data.get("print_stats", {}).get("state", "unknown")
            job_name = data.get("print_stats", {}).get("filename", "N/A")
            time_left = round(data.get("print_stats", {}).get("print_duration", 0) / 60)  # Convert sec to min

            extruder_temp = round(data.get("extruder", {}).get("temperature", 0))
            bed_temp = round(data.get("heater_bed", {}).get("temperature", 0))
            chamber_temp = round(data.get("heater_generic chamber", {}).get("temperature", 0))
            cpu_temp = round(data.get("temperature_host CPU", {}).get("temperature", 0))
            mcu_temp = round(data.get("temperature_sensor Motherboard MCU", {}).get("temperature", 0))
            printhead_mcu_temp = round(data.get("temperature_sensor Printhead MCU", {}).get("temperature", 0))

            # Device values
            sensor_values = {
                "extruder_temp": extruder_temp,
                "bed_temp": bed_temp,
                "chamber_temp": chamber_temp,
                "cpu_temp": cpu_temp,
                "mcu_temp": mcu_temp,
                "printhead_mcu_temp": printhead_mcu_temp,
                "job_status": job_status,
                "time_left": time_left,
                "job_name": job_name,
            }

            # Update Domoticz devices
            for idx, (key, (label, dev_type, uom)) in enumerate(self.sensor_keys.items(), start=1):
                if key in sensor_values and idx in Devices:
                    if dev_type == "Temperature Sensor":
                        Devices[idx].Update(nValue=0, sValue=str(sensor_values[key]))
                    elif dev_type == "Selector Switch" and key == "job_status":
                        # For selector switch, get the level directly from job_status_levels
                        level = self.job_status_levels.get(sensor_values[key].lower(), 0)
                        Devices[idx].Update(nValue=level, sValue=str(level))
                    else:
                        Devices[idx].Update(nValue=0, sValue=str(sensor_values[key]))
                    Domoticz.Debug(f"Updated {label}: {sensor_values[key]}")

        except requests.RequestException as e:
            Domoticz.Debug(f"Error fetching printer status: {e}")

    def fetchPrinterHistory(self):
        """Fetch historical print statistics from Moonraker."""
        try:
            history_url = f"{self.moonraker_url}/server/history/totals"
            response = requests.get(history_url, timeout=5)
            response.raise_for_status()
            data = response.json().get("result", {}).get("job_totals", {})

            # Extract historical values
            total_jobs = data.get("total_jobs", 0)
            total_time = round(data.get("total_time", 0) / 3600)  # Convert sec to hours
            total_print_time = round(data.get("total_print_time", 0) / 3600)  # Convert sec to hours
            total_filament_used = round(data.get("total_filament_used", 0) / 1000)  # Convert mm to meters
            longest_job = round(data.get("longest_job", 0) / 3600)  # Convert sec to hours
            longest_print = round(data.get("longest_print", 0) / 3600)  # Convert sec to hours

            history_values = {
                "total_jobs": total_jobs,
                "total_time": total_time,
                "total_print_time": total_print_time,
                "total_filament_used": total_filament_used,
                "longest_job": longest_job,
                "longest_print": longest_print,
            }

            # Update Domoticz devices
            for idx, (key, (label, dev_type, uom)) in enumerate(self.sensor_keys.items(), start=1):
                if key in history_values and idx in Devices:
                    if dev_type == "Temperature Sensor":
                        Devices[idx].Update(nValue=0, sValue=str(history_values[key]))
                    else:
                        Devices[idx].Update(nValue=history_values[key], sValue=str(history_values[key]))
                    Domoticz.Debug(f"Updated {label}: {history_values[key]}")

        except requests.RequestException as e:
            Domoticz.Debug(f"Error fetching printer history: {e}")

    def shutdown_printer_system(self):
        """Send system shutdown command to printer host via Moonraker API"""
        try:
            shutdown_url = f"{self.moonraker_url}/machine/shutdown"
            response = requests.post(shutdown_url, timeout=5)
            response.raise_for_status()
            Domoticz.Log("System shutdown command sent successfully")
            return True
        except requests.RequestException as e:
            Domoticz.Error(f"Error sending shutdown command: {e}")
            return False

    def onCommand(self, Unit, Command, Level, Hue):
        """Handle commands from Domoticz devices"""
        Domoticz.Debug(f"onCommand called for Unit {Unit}: Command '{Command}', Level: {Level}")
        
        # Find which device was triggered
        device_key = None
        for idx, (key, (label, dev_type, uom)) in enumerate(self.sensor_keys.items(), start=1):
            if idx == Unit:
                device_key = key
                break
        
        if device_key == "shutdown_switch" and Command == "On":
            Domoticz.Log("Shutdown switch activated - sending shutdown command")
            if self.shutdown_printer_system():
                # Reset switch to Off after command is sent
                Devices[Unit].Update(nValue=0, sValue="Off")
            else:
                Domoticz.Error("Failed to send shutdown command")

global _plugin
_plugin = BasePlugin()

def onStart():
    _plugin.onStart()

def onHeartbeat():
    _plugin.onHeartbeat()

def onCommand(Unit, Command, Level, Hue):
    _plugin.onCommand(Unit, Command, Level, Hue)
