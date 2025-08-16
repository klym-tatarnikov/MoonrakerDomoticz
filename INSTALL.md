# Installation Guide

This guide provides detailed installation instructions for the Moonraker Domoticz Plugin.

## Prerequisites

### Domoticz Requirements
- Domoticz version 2020.2 or later
- Python plugin support enabled
- Network access to your 3D printer

### 3D Printer Requirements
- Klipper firmware installed
- Moonraker API server running
- Network connectivity

### System Requirements
- Python 3.x
- `requests` library (usually included with Domoticz)

## Optional: API Key Setup

For secured Moonraker instances, you can configure API key authentication:

### 1. Generate API Key
```bash
# SSH to your printer
cd ~/moonraker
scripts/generate-api-key.py
```

### 2. Configure Moonraker
Add to your `moonraker.conf`:
```ini
[authorization]
api_key_file: ~/printer_data/moonraker.api
trusted_clients:
    192.168.1.0/24  # Your network range
    127.0.0.1
```

### 3. Use in Plugin
- Enter the generated API key in the "API Key" field when configuring the hardware
- Leave blank for anonymous access (if no authentication required)

## Installation Methods

### Method 1: Git Clone (Recommended)

1. **Access your Domoticz server**
   ```bash
   ssh pi@your-domoticz-server
   ```

2. **Navigate to plugins directory**
   ```bash
   cd /path/to/domoticz/plugins
   # Common paths:
   # /home/pi/domoticz/plugins
   # /opt/domoticz/plugins
   # /usr/local/domoticz/plugins
   ```

3. **Clone the repository**
   ```bash
   git clone https://github.com/klym-tatarnikov/MoonrakerDomoticz.git
   ```

4. **Set permissions**
   ```bash
   chmod +x MoonrakerDomoticz/plugin.py
   ```

### Method 2: Manual Download

1. **Download the files**
   - Download `plugin.py` from the repository
   - Save it to your Domoticz plugins directory

2. **Create directory structure**
   ```bash
   mkdir -p /path/to/domoticz/plugins/MoonrakerDomoticz
   ```

3. **Copy files**
   ```bash
   cp plugin.py /path/to/domoticz/plugins/MoonrakerDomoticz/
   chmod +x /path/to/domoticz/plugins/MoonrakerDomoticz/plugin.py
   ```

## Configuration

### 1. Enable Python Plugins in Domoticz

1. Go to **Setup** → **Settings** → **System**
2. Enable **Accept new Hardware Devices**
3. Enable **Python Plugin System**
4. Restart Domoticz if needed

### 2. Restart Domoticz

```bash
# Systemd systems:
sudo systemctl restart domoticz

# SysV systems:
sudo service domoticz restart

# Manual restart:
sudo pkill domoticz
sudo /path/to/domoticz -daemon
```

### 3. Add Hardware in Domoticz

1. **Navigate to Hardware**
   - Go to **Setup** → **Hardware**

2. **Add New Hardware**
   - Click **Add** button
   - **Type**: Select "Moonraker 3D Printer Monitoring"
   - **Name**: Give your printer a descriptive name (e.g., "Ender 3 Pro")

3. **Configure Settings**
   - **Moonraker API Address**: Your printer's IP address (e.g., "192.168.1.100")
   - **Port**: Moonraker port (default: 7125)
   - **API Key**: Optional authentication key (leave blank for anonymous access)
   - **Polling Interval**: Update frequency in seconds (recommended: 10)
   - **Logging**: Choose logging level (Normal for production, Debug for troubleshooting)

4. **Add Hardware**
   - Click **Add** to create the hardware entry

### 4. Verify Installation

1. **Check Hardware Status**
   - Hardware should show as "OK" in the hardware list
   - No error messages in the status

2. **Verify Device Creation**
   - Go to **Setup** → **Devices**
   - You should see 16 new devices created:
     - 6 Temperature sensors
     - 1 Job status selector switch
     - 2 Print job information devices
     - 1 Shutdown switch
     - 6 Historical statistic sensors

3. **Check Logs**
   ```bash
   tail -f /var/log/domoticz.log
   # Look for messages like:
   # "Moonraker Plugin Starting..."
   # "Created device: ..."
   # "Updated [device]: [value]"
   ```

## Verification Tests

### 1. Temperature Monitoring
- Check that temperature values are updating
- Verify temperatures match your printer display/interface

### 2. Job Status
- Start a print and verify status changes to "printing"
- Pause/resume print and verify status updates
- Check that status shows "unknown" when printer is offline

### 3. Historical Data
- Let plugin run for several polling cycles
- Verify historical statistics are updating

### 4. Shutdown Function
- **Test carefully!** This will shutdown your printer
- Toggle the shutdown switch ON
- Verify printer system shuts down
- Switch should automatically reset to OFF

## Troubleshooting

### Plugin Not Appearing
```bash
# Check plugin files exist
ls -la /path/to/domoticz/plugins/MoonrakerDomoticz/

# Check permissions
chmod +x /path/to/domoticz/plugins/MoonrakerDomoticz/plugin.py

# Restart Domoticz
sudo systemctl restart domoticz
```

### No Data Updates
```bash
# Test Moonraker API manually
curl http://YOUR_PRINTER_IP:7125/printer/info

# Test with API key (if using authentication)
curl -H "X-Api-Key: YOUR_API_KEY" http://YOUR_PRINTER_IP:7125/printer/info

# Check network connectivity
ping YOUR_PRINTER_IP

# Verify Moonraker is running
ssh pi@your-printer
sudo systemctl status moonraker
```

### Authentication Issues
```bash
# Check API key format
# API keys are typically 32-character hex strings

# Verify moonraker.conf authorization section
# Ensure trusted_clients includes your Domoticz server IP
```

### Python Dependencies
```bash
# Install requests if missing
pip3 install requests

# For Debian/Ubuntu systems
sudo apt-get install python3-requests
```

### Logs Showing Errors
```bash
# View detailed logs
tail -f /var/log/domoticz.log | grep -i moonraker

# Enable debug logging in hardware settings
# Set Logging to "Debug" or "Verbose"
```

## Uninstallation

1. **Remove Hardware**
   - Go to **Setup** → **Hardware**
   - Find your printer hardware entry
   - Click the red **X** to delete

2. **Remove Plugin Files**
   ```bash
   rm -rf /path/to/domoticz/plugins/MoonrakerDomoticz
   ```

3. **Restart Domoticz**
   ```bash
   sudo systemctl restart domoticz
   ```

## Next Steps

After successful installation:
- Explore the created devices in **Setup** → **Devices**
- Add devices to dashboards in **Setup** → **More Options** → **User Variables**
- Set up automation scripts using the temperature and status data
- Configure notifications for important events

For advanced usage and automation examples, see the main README.md file.
