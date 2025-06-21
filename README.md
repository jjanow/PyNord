# PyNord - NordVPN Management Application

A modern, user-friendly desktop application for managing NordVPN on Kubuntu and other Linux distributions. Built with Python and Tkinter, PyNord provides an intuitive graphical interface for all your NordVPN needs.

## Features

- **Easy Connection Management**: Quick connect/disconnect with one click
- **Server Selection**: Browse and connect to specific countries and cities
- **Real-time Status Monitoring**: Live updates of connection status and details
- **Advanced Settings**: Configure technology, protocol, kill switch, and auto-connect
- **Speed Testing**: Built-in connection speed testing
- **Comprehensive Logging**: Detailed logs for troubleshooting
- **Modern Tkinter UI**: Clean, native-looking interface for Linux
- **Background Monitoring**: Continuous status monitoring without blocking the UI
- **Offline Locations Data**: Pre-loaded NordVPN server locations for fast access

## NordVPN Locations Data

PyNord includes a comprehensive database of NordVPN server locations stored in `nordvpn_locations.json`. This file contains:

- **125 countries** with NordVPN servers
- **163 cities** across all supported locations
- **Fast loading** without requiring CLI calls
- **Easy maintenance** - update the JSON file to refresh locations

The application automatically loads this data on startup, providing instant access to all available server locations. If the JSON file is not found, PyNord falls back to querying the NordVPN CLI directly.

### Updating Locations Data

To update the server locations data:

1. Ensure NordVPN CLI is installed and working
2. Run the data collection script (if provided)
3. Restart PyNord to load the updated data

The locations data is stored in a human-readable JSON format for easy inspection and modification.

## Screenshots

*Screenshots will be added here*

## Requirements

- **Operating System**: Linux (tested on Kubuntu 22.04+)
- **Python**: 3.8 or higher
- **NordVPN CLI**: Must be installed and configured
- **Dependencies**: See requirements.txt

## Installation

### Prerequisites

1. **Install NordVPN CLI**:
   ```bash
   # Download and install NordVPN CLI
   wget https://repo.nordvpn.com/deb/nordvpn/debian/pool/main/nordvpn-release_1.0.0_all.deb
   sudo dpkg -i nordvpn-release_1.0.0_all.deb
   sudo apt update
   sudo apt install nordvpn
   
   # Login to your NordVPN account
   nordvpn login
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Install PyNord

#### Option 1: Install from source
```bash
git clone https://github.com/yourusername/pynord.git
cd pynord
pip install -e .
```

#### Option 2: Run directly
```bash
git clone https://github.com/yourusername/pynord.git
cd pynord
python main.py
```

## Usage

### Starting the Application

```bash
# If installed via pip
pynord

# Or run directly
python main.py
```

### Basic Operations

1. **Quick Connect**: Click the "Connect" button to connect to the best available server
2. **Server Selection**: 
   - Select a country from the dropdown
   - Optionally select a specific city
   - Click "Connect to Selected Server"
3. **Disconnect**: Click the "Disconnect" button to disconnect from VPN
4. **Status Monitoring**: View real-time connection status in the Status tab
5. **Settings**: Configure VPN settings in the Settings tab

### Advanced Features

- **Speed Testing**: Click "Test Speed" in the Status tab to check connection speed
- **Settings Configuration**: 
  - Choose between NordLynx and OpenVPN technologies
  - Set protocol (UDP/TCP)
  - Enable/disable kill switch
  - Configure auto-connect
- **Logs**: View detailed application logs in the Logs tab

## Configuration

### NordVPN CLI Setup

Before using PyNord, ensure NordVPN CLI is properly configured:

```bash
# Login to your account
nordvpn login

# Set default settings (optional)
nordvpn set technology NordLynx
nordvpn set protocol UDP
nordvpn set killswitch enabled
```

### PyNord Configuration

PyNord automatically detects NordVPN CLI settings and provides a GUI to modify them. No additional configuration files are required.

## Troubleshooting

### Common Issues

1. **"NordVPN CLI not found" error**:
   - Ensure NordVPN CLI is installed and in your PATH
   - Try running `nordvpn status` in terminal to verify installation

2. **Permission denied errors**:
   - NordVPN CLI requires root privileges for some operations
   - Ensure you're running PyNord with appropriate permissions

3. **Connection failures**:
   - Check your internet connection
   - Verify NordVPN account credentials
   - Check NordVPN service status: `sudo systemctl status nordvpnd`

4. **GUI not displaying properly**:
   - Tkinter is included with Python by default
   - Ensure your system has proper display support
   - Check if your system supports the required Tkinter features

### Logs

PyNord creates detailed logs in `pynord.log` in the application directory. Check this file for detailed error information.

## Development

### Project Structure

```
pynord/
├── src/
│   ├── __init__.py
│   ├── nordvpn_manager.py    # Core VPN management logic
│   └── main_window.py        # GUI implementation
├── main.py                   # Application entry point
├── setup.py                  # Installation script
├── requirements.txt          # Python dependencies
├── nordvpn_locations.json    # NordVPN server locations data
└── README.md                # This file
```

### Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Add tests if applicable
5. Commit your changes: `git commit -am 'Add feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a pull request

### Building from Source

```bash
git clone https://github.com/yourusername/pynord.git
cd pynord
pip install -r requirements.txt
python main.py
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- NordVPN for providing the CLI tool
- Python Tkinter team for the excellent GUI framework
- The open-source community for inspiration and tools

## Support

- **Issues**: Report bugs and feature requests on GitHub
- **Documentation**: Check this README and inline code comments
- **Community**: Join discussions in GitHub issues

## Changelog

### Version 1.0.0
- Initial release
- Basic VPN connection management
- Server selection by country/city
- Real-time status monitoring
- Settings configuration
- Offline NordVPN locations data (125 countries, 163 cities)