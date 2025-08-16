# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.0] - 2025-08-17

### Added
- Comprehensive job status selector switch with all possible Moonraker states
- Remote system shutdown functionality via Domoticz switch
- Connection monitoring with automatic offline detection
- Job status updates to "unknown" when printer is unreachable
- Enhanced device creation with proper switch support
- Detailed logging for device creation and status updates

### Changed
- Job status device changed from Text to Selector Switch
- Improved error handling and logging throughout the plugin
- Device update logic enhanced for better reliability
- Logging levels adjusted for better debugging (Debug vs Log)

### Fixed
- Device numbering consistency issues
- Proper handling of unreachable printer states
- Switch reset functionality after shutdown command

## [1.2.0] - 2024-XX-XX

### Added
- Historical statistics tracking
- Total jobs, print time, and filament usage monitoring
- Longest print job and continuous print records
- Custom sensor devices with proper units of measurement

### Changed
- Improved temperature sensor handling
- Enhanced API error handling
- Better data validation and conversion

## [1.1.0] - 2024-XX-XX

### Added
- Job status and print information monitoring
- Current job name display
- Time remaining estimation
- Print duration tracking

### Changed
- Improved API error handling
- Enhanced data extraction from Moonraker responses

## [1.0.0] - 2024-XX-XX

### Added
- Initial release
- Basic temperature monitoring for extruder, bed, chamber, CPU, and MCU
- Moonraker API integration
- Real-time data updates
- Configurable polling intervals
- Network connectivity testing

### Features
- Temperature sensor devices creation
- Automatic device management
- Connection status monitoring
- Configurable logging levels
