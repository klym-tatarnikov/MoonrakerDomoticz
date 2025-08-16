# Contributing to Moonraker Domoticz Plugin

Thank you for your interest in contributing to this project! This document provides guidelines for contributing.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Create a new branch for your feature or bug fix
4. Make your changes
5. Test your changes thoroughly
6. Submit a pull request

## Development Environment

### Requirements
- Domoticz installation for testing
- 3D printer with Klipper/Moonraker setup (or mock API for testing)
- Python 3.x
- Access to Domoticz plugin development environment

### Testing
- Test all temperature sensors
- Verify job status updates
- Test historical statistics
- Confirm shutdown functionality works
- Test connection monitoring (disconnect printer to test offline behavior)

## Code Style

- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add comments for complex logic
- Include docstrings for functions and classes

## Reporting Issues

When reporting issues, please include:
- Domoticz version
- Klipper/Moonraker versions
- Plugin version
- Detailed description of the problem
- Steps to reproduce
- Relevant log entries
- Your printer configuration (if relevant)

## Feature Requests

Before submitting feature requests:
- Check if the feature already exists
- Check if there's already an open issue for it
- Clearly describe the feature and its benefits
- Consider if it fits the plugin's scope

## Pull Request Process

1. Ensure your code follows the style guidelines
2. Update documentation if needed
3. Add or update tests if applicable
4. Update the CHANGELOG.md with your changes
5. Ensure all tests pass
6. Submit your pull request with a clear description

## Areas for Contribution

### High Priority
- Additional temperature sensors support
- Enhanced error handling
- Performance optimizations
- Documentation improvements

### Medium Priority
- Additional Moonraker API endpoints
- More automation examples
- Configuration validation
- Unit tests

### Low Priority
- UI enhancements
- Additional logging options
- Code refactoring

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help newcomers learn
- Keep discussions on-topic

## Questions?

If you have questions about contributing, feel free to:
- Open an issue for discussion
- Start a GitHub discussion
- Contact the maintainer

Thank you for contributing to the 3D printing community!
