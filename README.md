# Moonraker 3D Printer Monitoring Plugin for Domoticz

A comprehensive Domoticz plugin for monitoring Moonraker-based 3D printers (Klipper firmware). This plugin provides real-time integration between your 3D printer and Domoticz home automation system.

![Domoticz](https://img.shields.io/badge/Domoticz-Plugin-blue)
![Klipper](https://img.shields.io/badge/Klipper-Compatible-green)
![Moonraker](https://img.shields.io/badge/Moonraker-API-orange)
![Python](https://img.shields.io/badge/Python-3.x-yellow)

![Alt text](dashboard.png?raw=true "Dashboard")

## Features

### 🌡️ Real-time Temperature Monitoring
- **Extruder Temperature** - Current hotend temperature
- **Bed Temperature** - Heated bed temperature
- **Chamber Temperature** - Enclosure temperature (if available)
- **CPU Temperature** - Raspberry Pi/host CPU temperature
- **MCU Temperatures** - Motherboard and printhead MCU temperatures

### 📊 Job Status Tracking
- **Complete Status Monitoring** - Real-time printer state with selector switch
- **Status Options**: `unknown`, `idle`, `ready`, `standby`, `printing`, `paused`, `complete`, `completed`, `cancelled`, `error`
- **Automatic Offline Detection** - Status updates to "unknown" when printer is unreachable

### 🖨️ Print Job Information
- **Current Job Name** - Display active print filename
- **Time Remaining** - Estimated time left for current print (in minutes)

### 📈 Historical Statistics
- **Total Jobs Printed** - Complete job counter
- **Total Printer Time** - Cumulative printer uptime (hours)
- **Total Print Time** - Active printing time (hours)
- **Total Filament Used** - Cumulative filament consumption (meters)
- **Longest Print Job** - Record of longest single print (hours)
- **Longest Continuous Print** - Longest uninterrupted print session (hours)

### 🔌 Remote Control
- **System Shutdown** - Safely shutdown printer host system via Domoticz switch
- **Connection Monitoring** - Automatic detection of printer availability
- **API Key Support** - Optional authentication for secured Moonraker instances

## Requirements

- **Domoticz** home automation system
- **3D Printer** running Klipper firmware with Moonraker API
- **Network connectivity** between Domoticz and printer
- **Python requests library** (usually pre-installed with Domoticz)
- **Optional: API Key** for secured Moonraker installations

## Compatible Printers

This plugin works with any 3D printer running:
- **Klipper** firmware
- **Moonraker** API server
- Compatible front-ends: **Mainsail**, **Fluidd**, **KlipperScreen**

## Installation

### 1. Download Plugin
```bash
cd /home/pi/domoticz/plugins
git clone https://github.com/klym-tatarnikov/MoonrakerDomoticz.git
```

### 2. Restart Domoticz
```bash
sudo systemctl restart domoticz
```

### 3. Add Hardware
1. Go to **Setup** → **Hardware** in Domoticz
2. Add hardware type: **Moonraker 3D Printer Monitoring**
3. Configure settings:
   - **Name**: Give your printer a name (e.g., "My 3D Printer")
   - **Moonraker API Address**: IP address of your printer (e.g., "192.168.1.100")
   - **Port**: Moonraker port (default: 7125)
   - **API Key**: Optional authentication key (leave blank for anonymous access)
   - **Polling Interval**: Update frequency in seconds (default: 10)
   - **Logging Level**: Choose logging verbosity

### 4. Devices Created
The plugin automatically creates these devices:
- Temperature sensors (6 devices)
- Job status selector switch
- Print job information (2 text devices)
- System shutdown switch
- Historical statistics (6 custom sensors)

## Configuration

### Moonraker Setup
Ensure Moonraker is properly configured in your `moonraker.conf`:

```ini
[machine]
provider: systemd_dbus

[history]
# Required for historical statistics

# Optional: API Key authentication
[authorization]
trusted_clients:
    192.168.1.0/24
    127.0.0.1
cors_domains:
    *.lan
    *.local
    *://localhost
    *://localhost:*
    *://my.mainsail.xyz
    *://app.fluidd.xyz

# API Key configuration (optional)
[secrets]
# Create API keys for secure access
```

### API Key Setup (Optional)
For secured Moonraker instances:

1. **Generate API Key** in Moonraker:
   ```bash
   # SSH to your printer
   cd ~/moonraker
   scripts/generate-api-key.py
   ```

2. **Configure in moonraker.conf**:
   ```ini
   [authorization]
   api_key_file: ~/printer_data/moonraker.api
   ```

3. **Use in Domoticz**: Enter the generated API key in the plugin settings

### Network Access
Make sure your Domoticz server can reach your printer:
```bash
# Test connectivity
curl http://YOUR_PRINTER_IP:7125/printer/info
```

## Usage

### Monitoring
- **Temperature devices** update in real-time with current temperatures
- **Job Status** shows current printer state via selector switch
- **Historical data** updates periodically with cumulative statistics

### Remote Shutdown
1. Locate the "Shutdown Printer" switch in Domoticz
2. Turn switch **ON** to send shutdown command
3. Switch automatically resets to **OFF** after command is sent
4. Printer host system will safely shutdown

### Automation Examples

#### Temperature Alert
```lua
-- Lua script example: Alert if extruder temperature too high
commandArray = {}
if devicechanged['Your Printer - Extruder Temperature'] then
    temp = tonumber(uservariables['Your Printer - Extruder Temperature'])
    if temp > 250 then
        commandArray['SendNotification'] = 'High Temperature Alert#Extruder: ' .. temp .. '°C'
    end
end
return commandArray
```

#### Auto-shutdown After Print
```lua
-- Lua script example: Shutdown printer after print completes
commandArray = {}
if devicechanged['Your Printer - Job Status'] then
    if device['Your Printer - Job Status'].sValue == 'completed' then
        -- Wait 10 minutes then shutdown
        commandArray['Variable:shutdown_timer'] = tostring(os.time() + 600)
    end
end
return commandArray
```

## Troubleshooting

### Plugin Not Working
1. Check Domoticz logs: `tail -f /var/log/domoticz.log`
2. Verify Python requests library: `pip3 install requests`
3. Test Moonraker API manually: `curl http://PRINTER_IP:7125/printer/info`

### No Temperature Data
- Verify temperature sensor names in your Klipper configuration
- Check if sensors are properly configured in `printer.cfg`

### Authentication Errors
- Verify API key is correct if using authentication
- Check Moonraker authorization configuration
- Ensure trusted clients include Domoticz server IP

### Historical Data Missing
- Ensure Moonraker `[history]` section is enabled
- Wait for plugin to complete first polling cycle

### Shutdown Not Working
- Verify Moonraker machine provider: `provider: systemd_dbus`
- Check user permissions for system shutdown
- Review Moonraker logs for shutdown errors

## API Endpoints Used

This plugin utilizes these Moonraker API endpoints:
- `/printer/objects/query` - Real-time printer status and temperatures
- `/server/history/totals` - Historical print statistics  
- `/machine/shutdown` - System shutdown command

**Authentication**: All endpoints support optional API key authentication via `X-Api-Key` header.

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

### Development Setup
1. Fork this repository
2. Make your changes
3. Test with your printer setup
4. Submit a pull request

## License

This project is open source. Feel free to use, modify, and distribute according to your needs.

## Support

- **Issues**: Report bugs or request features via GitHub Issues
- **Discussions**: Share experiences and ask questions in GitHub Discussions
- **Domoticz Forum**: Get help from the community

## Changelog

### Version 1.3
- Added comprehensive job status selector with all Moonraker states
- Implemented remote system shutdown functionality
- Added connection monitoring with automatic offline detection
- Enhanced error handling and logging
- Improved device creation and management

### Version 1.2
- Added historical statistics tracking
- Improved temperature sensor handling
- Enhanced error handling

### Version 1.1
- Added job status and print information
- Improved API error handling

### Version 1.0
- Initial release
- Basic temperature monitoring
- Moonraker API integration

---

**Made with ❤️ for the 3D printing community**
