import subprocess
import json
import threading
import time
import psutil
import os
from typing import Dict, List, Optional, Callable, Any
import logging

class NordVPNManager:
    """Main class for managing NordVPN connections and operations."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.status_callback: Optional[Callable] = None
        self.monitoring = False
        self.monitor_thread = None
        self.locations_data = None
        self._load_locations_data()
        
    def _load_locations_data(self):
        """Load NordVPN locations data from JSON file."""
        try:
            # Try to load from the same directory as this file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            json_path = os.path.join(os.path.dirname(current_dir), 'nordvpn_locations.json')
            
            if os.path.exists(json_path):
                with open(json_path, 'r', encoding='utf-8') as f:
                    self.locations_data = json.load(f)
                self.logger.info("Loaded NordVPN locations data from JSON file")
            else:
                self.logger.warning("NordVPN locations JSON file not found, will use CLI commands")
                self.locations_data = None
        except Exception as e:
            self.logger.error(f"Error loading locations data: {e}")
            self.locations_data = None
        
    def _run_command(self, command: List[str]) -> Dict[str, Any]:
        """Execute a NordVPN command and return the result."""
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=30
            )
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout.strip(),
                'stderr': result.stderr.strip(),
                'returncode': result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'stdout': '',
                'stderr': 'Command timed out',
                'returncode': -1
            }
        except Exception as e:
            return {
                'success': False,
                'stdout': '',
                'stderr': str(e),
                'returncode': -1
            }
    
    def get_status(self) -> Dict[str, Any]:
        """Get current NordVPN connection status."""
        result = self._run_command(['nordvpn', 'status'])
        if result['success']:
            status_text = result['stdout']
            return self._parse_status(status_text)
        return {'connected': False, 'error': result['stderr']}
    
    def _parse_status(self, status_text: str) -> Dict[str, Any]:
        """Parse NordVPN status output."""
        status: Dict[str, Any] = {'connected': False}
        
        lines = status_text.split('\n')
        for line in lines:
            line = line.strip()
            if 'Status:' in line:
                status['connected'] = 'Connected' in line
            elif 'Current server:' in line:
                parts = line.split(':', 1)
                if len(parts) > 1:
                    status['server'] = parts[1].strip()
            elif 'Country:' in line:
                parts = line.split(':', 1)
                if len(parts) > 1:
                    status['country'] = parts[1].strip()
            elif 'City:' in line:
                parts = line.split(':', 1)
                if len(parts) > 1:
                    status['city'] = parts[1].strip()
            elif 'Your new IP:' in line:
                parts = line.split(':', 1)
                if len(parts) > 1:
                    status['ip'] = parts[1].strip()
            elif 'Current technology:' in line:
                parts = line.split(':', 1)
                if len(parts) > 1:
                    status['technology'] = parts[1].strip()
            elif 'Transfer:' in line:
                parts = line.split(':', 1)
                if len(parts) > 1:
                    status['transfer'] = parts[1].strip()
            elif 'Uptime:' in line:
                parts = line.split(':', 1)
                if len(parts) > 1:
                    status['uptime'] = parts[1].strip()
        
        return status
    
    def connect(self, country: Optional[str] = None, city: Optional[str] = None) -> Dict[str, Any]:
        """Connect to NordVPN."""
        command = ['nordvpn', 'connect']
        if country:
            command.append(country)
            if city:
                command.append(city)
        
        return self._run_command(command)
    
    def disconnect(self) -> Dict[str, Any]:
        """Disconnect from NordVPN."""
        return self._run_command(['nordvpn', 'disconnect'])
    
    def get_countries(self) -> List[str]:
        """Get list of available countries."""
        # Try to use cached data first
        if self.locations_data and 'countries' in self.locations_data:
            return self.locations_data['countries']
        
        # Fallback to CLI command
        result = self._run_command(['nordvpn', 'countries'])
        if result['success']:
            countries = []
            lines = result['stdout'].split('\n')
            for line in lines:
                line = line.strip()
                if line and not line.startswith('Countries:') and not line.startswith('*'):
                    # Split by spaces and filter out empty strings
                    country_list = [c for c in line.split() if c]
                    countries.extend(country_list)
            return countries
        return []
    
    def get_cities(self, country: str) -> List[str]:
        """Get list of available cities for a country."""
        # Try to use cached data first
        if (self.locations_data and 
            'cities_by_country' in self.locations_data and 
            country in self.locations_data['cities_by_country']):
            return self.locations_data['cities_by_country'][country]
        
        # Fallback to CLI command
        result = self._run_command(['nordvpn', 'cities', country])
        if result['success']:
            cities = []
            lines = result['stdout'].split('\n')
            for line in lines:
                line = line.strip()
                if line and not line.startswith('Cities:') and not line.startswith('*'):
                    # Split by spaces and filter out empty strings
                    city_list = [c for c in line.split() if c]
                    cities.extend(city_list)
            return cities
        return []
    
    def set_technology(self, technology: str) -> Dict[str, Any]:
        """Set VPN technology (OpenVPN, NordLynx)."""
        return self._run_command(['nordvpn', 'set', 'technology', technology])
    
    def set_protocol(self, protocol: str) -> Dict[str, Any]:
        """Set VPN protocol (UDP, TCP)."""
        return self._run_command(['nordvpn', 'set', 'protocol', protocol])
    
    def set_kill_switch(self, enabled: bool) -> Dict[str, Any]:
        """Enable or disable kill switch."""
        value = 'enabled' if enabled else 'disabled'
        return self._run_command(['nordvpn', 'set', 'killswitch', value])
    
    def set_autoconnect(self, enabled: bool) -> Dict[str, Any]:
        """Enable or disable autoconnect."""
        value = 'enabled' if enabled else 'disabled'
        return self._run_command(['nordvpn', 'set', 'autoconnect', value])
    
    def get_settings(self) -> Dict[str, Any]:
        """Get current NordVPN settings."""
        result = self._run_command(['nordvpn', 'settings'])
        if result['success']:
            return self._parse_settings(result['stdout'])
        return {}
    
    def _parse_settings(self, settings_text: str) -> Dict[str, Any]:
        """Parse NordVPN settings output."""
        settings: Dict[str, Any] = {}
        lines = settings_text.split('\n')
        for line in lines:
            line = line.strip()
            if ':' in line:
                key, value = line.split(':', 1)
                settings[key.strip()] = value.strip()
        return settings
    
    def start_monitoring(self, callback: Callable):
        """Start monitoring NordVPN status in background thread."""
        self.status_callback = callback
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop monitoring NordVPN status."""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1)
    
    def _monitor_loop(self):
        """Background monitoring loop."""
        while self.monitoring:
            try:
                status = self.get_status()
                if self.status_callback:
                    self.status_callback(status)
                time.sleep(2)  # Check every 2 seconds
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                time.sleep(5)  # Wait longer on error
    
    def is_nordvpn_installed(self) -> bool:
        """Check if NordVPN CLI is installed."""
        result = self._run_command(['which', 'nordvpn'])
        return result['success']
    
    def get_connection_speed(self) -> Dict[str, Any]:
        """Get current connection speed using speedtest-cli."""
        try:
            import speedtest
            st = speedtest.Speedtest()
            
            # Get best server
            st.get_best_server()
            
            # Test download speed
            download_speed = st.download() / 1_000_000  # Convert to Mbps
            
            # Test upload speed
            upload_speed = st.upload() / 1_000_000  # Convert to Mbps
            
            # Get ping
            ping = st.results.ping
            
            return {
                'success': True,
                'download_mbps': round(download_speed, 2),
                'upload_mbps': round(upload_speed, 2),
                'ping_ms': round(ping, 1),
                'server': st.results.server['name'],
                'server_country': st.results.server['country'],
                'server_distance': round(st.results.server.get('distance', 0), 1)
            }
        except ImportError:
            return {'error': 'speedtest-cli library not installed'}
        except Exception as e:
            return {'error': f'Speed test failed: {str(e)}'}
    
    def run_speed_test(self, progress_callback=None) -> Dict[str, Any]:
        """Run a comprehensive speed test with progress updates."""
        try:
            import speedtest
            st = speedtest.Speedtest()
            
            if progress_callback:
                progress_callback("Finding best server...")
            
            # Get best server
            st.get_best_server()
            
            if progress_callback:
                progress_callback("Testing download speed...")
            
            # Test download speed
            download_speed = st.download() / 1_000_000  # Convert to Mbps
            
            if progress_callback:
                progress_callback("Testing upload speed...")
            
            # Test upload speed
            upload_speed = st.upload() / 1_000_000  # Convert to Mbps
            
            if progress_callback:
                progress_callback("Calculating results...")
            
            # Get ping
            ping = st.results.ping
            
            # Calculate speed ratings
            download_rating = self._get_speed_rating(download_speed)
            upload_rating = self._get_speed_rating(upload_speed)
            ping_rating = self._get_ping_rating(ping)
            
            return {
                'success': True,
                'download_mbps': round(download_speed, 2),
                'upload_mbps': round(upload_speed, 2),
                'ping_ms': round(ping, 1),
                'download_rating': download_rating,
                'upload_rating': upload_rating,
                'ping_rating': ping_rating,
                'server': st.results.server['name'],
                'server_country': st.results.server['country'],
                'server_distance': round(st.results.server.get('distance', 0), 1),
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
        except ImportError:
            return {'error': 'speedtest-cli library not installed'}
        except Exception as e:
            return {'error': f'Speed test failed: {str(e)}'}
    
    def _get_speed_rating(self, speed_mbps: float) -> str:
        """Get a human-readable rating for speed."""
        if speed_mbps >= 100:
            return "Excellent"
        elif speed_mbps >= 50:
            return "Very Good"
        elif speed_mbps >= 25:
            return "Good"
        elif speed_mbps >= 10:
            return "Fair"
        elif speed_mbps >= 5:
            return "Poor"
        else:
            return "Very Poor"
    
    def _get_ping_rating(self, ping_ms: float) -> str:
        """Get a human-readable rating for ping."""
        if ping_ms < 20:
            return "Excellent"
        elif ping_ms < 50:
            return "Very Good"
        elif ping_ms < 100:
            return "Good"
        elif ping_ms < 200:
            return "Fair"
        else:
            return "Poor" 