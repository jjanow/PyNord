import sys
import os
import threading
import time
from typing import Dict, Any, Optional
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from nordvpn_manager import NordVPNManager

class StatusMonitor:
    """Background thread for monitoring VPN status."""
    
    def __init__(self, vpn_manager: NordVPNManager, callback):
        self.vpn_manager = vpn_manager
        self.callback = callback
        self.running = False
        self.monitor_thread = None
        
    def start_monitoring(self):
        """Start monitoring VPN status."""
        self.running = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        
    def stop_monitoring(self):
        """Stop monitoring VPN status."""
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1)
            
    def _monitor_loop(self):
        """Background monitoring loop."""
        while self.running:
            try:
                status = self.vpn_manager.get_status()
                if self.callback:
                    # Use after() to schedule callback in main thread
                    self.callback(status)
                time.sleep(2)  # Check every 2 seconds
            except Exception as e:
                print(f"Error in monitoring loop: {e}")
                time.sleep(5)  # Wait longer on error

class MainWindow:
    """Main application window for PyNord VPN Manager."""
    
    def __init__(self, root):
        self.root = root
        self.vpn_manager = NordVPNManager()
        self.status_monitor = StatusMonitor(self.vpn_manager, self.update_status)
        self.countries = []
        self.cities = []
        self.current_status = {'connected': False}
        
        self.init_ui()
        self.setup_connections()
        if self.check_nordvpn_installation():
            self.load_countries()
        
    def init_ui(self):
        """Initialize the user interface."""
        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        
        # Create main frame
        main_frame = ttk.Frame(self.root)
        main_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Left panel - Connection controls
        left_panel = self.create_left_panel(main_frame)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # Right panel - Status and settings
        right_panel = self.create_right_panel(main_frame)
        right_panel.grid(row=0, column=1, sticky="nsew")
        
        # Apply styling
        self.apply_styling()
        
    def create_left_panel(self, parent):
        """Create the left panel with connection controls."""
        panel = ttk.Frame(parent)
        
        # Connection status group
        status_frame = ttk.LabelFrame(panel, text="Connection Status", padding=10)
        status_frame.pack(fill="x", pady=(0, 10))
        
        # Status indicator
        self.status_label = ttk.Label(status_frame, text="Disconnected", 
                                     font=("Arial", 14, "bold"), foreground="red")
        self.status_label.pack(pady=5)
        
        # Connection info
        self.connection_info = ttk.Label(status_frame, text="No active connection", 
                                        wraplength=300)
        self.connection_info.pack(pady=5)
        
        # Quick connect group
        quick_frame = ttk.LabelFrame(panel, text="Quick Connect", padding=10)
        quick_frame.pack(fill="x", pady=(0, 10))
        
        # Connect/Disconnect button
        self.connect_button = ttk.Button(quick_frame, text="Connect", 
                                        command=self.quick_connect)
        self.connect_button.pack(fill="x", pady=5)
        
        # Quick disconnect button
        self.disconnect_button = ttk.Button(quick_frame, text="Disconnect", 
                                           command=self.disconnect, state="disabled")
        self.disconnect_button.pack(fill="x", pady=5)
        
        # Server selection group
        server_frame = ttk.LabelFrame(panel, text="Server Selection", padding=10)
        server_frame.pack(fill="x", pady=(0, 10))
        
        # Country selection
        ttk.Label(server_frame, text="Country:").pack(anchor="w")
        self.country_combo = ttk.Combobox(server_frame, state="readonly")
        self.country_combo.pack(fill="x", pady=5)
        
        # City selection
        ttk.Label(server_frame, text="City:").pack(anchor="w")
        self.city_combo = ttk.Combobox(server_frame, state="readonly")
        self.city_combo.pack(fill="x", pady=5)
        
        # Connect to specific server button
        self.connect_specific_button = ttk.Button(server_frame, 
                                                 text="Connect to Selected Server",
                                                 command=self.connect_to_specific,
                                                 state="disabled")
        self.connect_specific_button.pack(fill="x", pady=5)
        
        return panel
        
    def create_right_panel(self, parent):
        """Create the right panel with status details and settings."""
        panel = ttk.Frame(parent)
        panel.grid_rowconfigure(0, weight=1)
        panel.grid_columnconfigure(0, weight=1)
        
        # Create notebook (tab widget)
        self.notebook = ttk.Notebook(panel)
        self.notebook.grid(row=0, column=0, sticky="nsew")
        
        # Status tab
        status_tab = self.create_status_tab()
        self.notebook.add(status_tab, text="Status")
        
        # Settings tab
        settings_tab = self.create_settings_tab()
        self.notebook.add(settings_tab, text="Settings")
        
        # Logs tab
        logs_tab = self.create_logs_tab()
        self.notebook.add(logs_tab, text="Logs")
        
        return panel
        
    def create_status_tab(self):
        """Create the status details tab."""
        tab = ttk.Frame(self.notebook)
        
        # Connection details group
        details_frame = ttk.LabelFrame(tab, text="Connection Details", padding=10)
        details_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create a frame for the grid
        grid_frame = ttk.Frame(details_frame)
        grid_frame.pack(fill="both", expand=True)
        
        self.detail_labels = {}
        details = [
            ("Server", "server"),
            ("Country", "country"),
            ("City", "city"),
            ("IP Address", "ip"),
            ("Technology", "technology"),
            ("Transfer", "transfer"),
            ("Uptime", "uptime")
        ]
        
        for i, (label_text, key) in enumerate(details):
            ttk.Label(grid_frame, text=f"{label_text}:").grid(row=i, column=0, sticky="w", padx=5, pady=2)
            self.detail_labels[key] = ttk.Label(grid_frame, text="N/A")
            self.detail_labels[key].grid(row=i, column=1, sticky="w", padx=5, pady=2)
        
        # Speed test section
        speed_frame = ttk.LabelFrame(tab, text="Speed Test", padding=10)
        speed_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.speed_button = ttk.Button(speed_frame, text="Test Connection Speed", 
                                      command=self.test_speed)
        self.speed_button.pack(pady=5)
        
        # Progress bar for speed test
        self.speed_progress = ttk.Progressbar(speed_frame, mode='indeterminate')
        self.speed_progress.pack(fill="x", pady=5)
        
        # Speed test result display
        self.speed_result = ttk.Label(speed_frame, text="Click 'Test Connection Speed' to start", 
                                     wraplength=400, justify="left")
        self.speed_result.pack(pady=5, fill="x")
        
        return tab
        
    def create_settings_tab(self):
        """Create the settings tab."""
        tab = ttk.Frame(self.notebook)
        
        # Settings frame
        settings_frame = ttk.LabelFrame(tab, text="VPN Settings", padding=10)
        settings_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Technology selection
        tech_frame = ttk.Frame(settings_frame)
        tech_frame.pack(fill="x", pady=5)
        ttk.Label(tech_frame, text="Technology:").pack(side="left")
        self.tech_var = tk.StringVar(value="NordLynx")
        self.tech_combo = ttk.Combobox(tech_frame, textvariable=self.tech_var, 
                                      values=["NordLynx", "OpenVPN"], state="readonly")
        self.tech_combo.pack(side="right", padx=5)
        
        # Protocol selection
        protocol_frame = ttk.Frame(settings_frame)
        protocol_frame.pack(fill="x", pady=5)
        ttk.Label(protocol_frame, text="Protocol:").pack(side="left")
        self.protocol_var = tk.StringVar(value="UDP")
        self.protocol_combo = ttk.Combobox(protocol_frame, textvariable=self.protocol_var, 
                                          values=["UDP", "TCP"], state="readonly")
        self.protocol_combo.pack(side="right", padx=5)
        
        # Kill switch
        self.kill_switch_var = tk.BooleanVar()
        kill_switch_check = ttk.Checkbutton(settings_frame, text="Kill Switch", 
                                           variable=self.kill_switch_var)
        kill_switch_check.pack(anchor="w", pady=5)
        
        # Auto connect
        self.auto_connect_var = tk.BooleanVar()
        auto_connect_check = ttk.Checkbutton(settings_frame, text="Auto Connect", 
                                            variable=self.auto_connect_var)
        auto_connect_check.pack(anchor="w", pady=5)
        
        # Apply settings button
        apply_button = ttk.Button(settings_frame, text="Apply Settings", 
                                 command=self.apply_settings)
        apply_button.pack(pady=10)
        
        return tab
        
    def create_logs_tab(self):
        """Create the logs tab."""
        tab = ttk.Frame(self.notebook)
        
        # Logs frame
        logs_frame = ttk.LabelFrame(tab, text="Application Logs", padding=10)
        logs_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Log text area
        self.log_text = scrolledtext.ScrolledText(logs_frame, height=20, width=60)
        self.log_text.pack(fill="both", expand=True)
        
        # Clear logs button
        clear_button = ttk.Button(logs_frame, text="Clear Logs", 
                                 command=lambda: self.log_text.delete(1.0, tk.END))
        clear_button.pack(pady=5)
        
        return tab
        
    def apply_styling(self):
        """Apply modern styling to the application."""
        style = ttk.Style()
        
        # Configure styles
        style.configure("Title.TLabel", font=("Arial", 14, "bold"))
        style.configure("Status.TLabel", font=("Arial", 12))
        
        # Configure button styles
        style.configure("Connect.TButton", font=("Arial", 12, "bold"))
        style.configure("Disconnect.TButton", font=("Arial", 11))
        
    def setup_connections(self):
        """Setup signal connections."""
        self.country_combo.bind("<<ComboboxSelected>>", self.on_country_changed)
        self.city_combo.bind("<<ComboboxSelected>>", self.on_city_changed)
        
        # Start status monitoring
        self.status_monitor.start_monitoring()
        
    def check_nordvpn_installation(self):
        """Check if NordVPN is installed."""
        if not self.vpn_manager.is_nordvpn_installed():
            messagebox.showerror("Error", "NordVPN CLI is not installed or not found in PATH.")
            return False
        return True
        
    def load_countries(self):
        """Load available countries."""
        self.countries = self.vpn_manager.get_countries()
        self.country_combo['values'] = ["Select Country"] + self.countries
        self.country_combo.set("Select Country")
        
    def on_country_changed(self, event):
        """Handle country selection change."""
        country = self.country_combo.get()
        if country and country != "Select Country":
            self.cities = self.vpn_manager.get_cities(country)
            self.city_combo['values'] = ["Select City"] + self.cities
            self.city_combo.set("Select City")
            self.city_combo.config(state="readonly")
            self.connect_specific_button.config(state="normal")
        else:
            self.city_combo.set("Select City")
            self.city_combo.config(state="disabled")
            self.connect_specific_button.config(state="disabled")
            
    def on_city_changed(self, event):
        """Handle city selection change."""
        city = self.city_combo.get()
        if city and city != "Select City":
            self.connect_specific_button.config(state="normal")
        else:
            self.connect_specific_button.config(state="disabled")
            
    def quick_connect(self):
        """Quick connect to NordVPN."""
        result = self.vpn_manager.connect()
        if result['success']:
            self.log_message("Quick connect initiated")
        else:
            messagebox.showerror("Connection Error", f"Failed to connect: {result['stderr']}")
            
    def connect_to_specific(self):
        """Connect to specific server."""
        country = self.country_combo.get()
        city = self.city_combo.get()
        
        if country == "Select Country":
            messagebox.showwarning("Warning", "Please select a country")
            return
        
        # If city is "Select City", pass None to connect to country only
        if city == "Select City":
            city = None
            
        result = self.vpn_manager.connect(country, city)
        if result['success']:
            city_text = f" {city}" if city else ""
            self.log_message(f"Connecting to {country}{city_text}")
        else:
            messagebox.showerror("Connection Error", f"Failed to connect: {result['stderr']}")
            
    def disconnect(self):
        """Disconnect from NordVPN."""
        result = self.vpn_manager.disconnect()
        if result['success']:
            self.log_message("Disconnected from NordVPN")
        else:
            messagebox.showerror("Disconnect Error", f"Failed to disconnect: {result['stderr']}")
            
    def update_status(self, status: Dict[str, Any]):
        """Update the status display."""
        self.current_status = status
        
        # Update status label
        if status.get('connected', False):
            self.status_label.config(text="Connected", foreground="green")
            self.connect_button.config(state="disabled")
            self.disconnect_button.config(state="normal")
        else:
            self.status_label.config(text="Disconnected", foreground="red")
            self.connect_button.config(state="normal")
            self.disconnect_button.config(state="disabled")
            
        # Update connection info
        if status.get('connected', False):
            server = status.get('server', 'Unknown')
            country = status.get('country', 'Unknown')
            city = status.get('city', 'Unknown')
            self.connection_info.config(text=f"Server: {server}\nCountry: {country}\nCity: {city}")
        else:
            self.connection_info.config(text="No active connection")
            
        # Update detail labels
        for key, label in self.detail_labels.items():
            value = status.get(key, 'N/A')
            label.config(text=str(value))
            
    def test_speed(self):
        """Test connection speed."""
        self.speed_button.config(state="disabled")
        self.speed_progress.start()
        self.speed_result.config(text="Initializing speed test...")
        
        # Run speed test in background
        threading.Thread(target=self._run_speed_test, daemon=True).start()
        
    def _run_speed_test(self):
        """Run speed test in background thread."""
        try:
            # Progress callback function
            def progress_callback(message):
                self.root.after(0, lambda: self.speed_result.config(text=message))
            
            # Run the speed test
            result = self.vpn_manager.run_speed_test(progress_callback)
            
            if result.get('success'):
                # Format the results nicely
                download = result['download_mbps']
                upload = result['upload_mbps']
                ping = result['ping_ms']
                server = result['server']
                country = result['server_country']
                
                result_text = f"""Speed Test Results:
Download: {download} Mbps ({result['download_rating']})
Upload: {upload} Mbps ({result['upload_rating']})
Ping: {ping} ms ({result['ping_rating']})
Server: {server} ({country})
Tested: {result['timestamp']}"""
                
                # Log the results
                self.log_message(f"Speed test completed - Download: {download} Mbps, Upload: {upload} Mbps, Ping: {ping} ms")
            else:
                result_text = f"Speed test failed: {result.get('error', 'Unknown error')}"
                self.log_message(f"Speed test failed: {result.get('error', 'Unknown error')}")
            
            # Update UI in main thread
            self.root.after(0, lambda: self.speed_result.config(text=result_text))
            self.root.after(0, lambda: self.speed_progress.stop())
            self.root.after(0, lambda: self.speed_button.config(state="normal"))
            
        except Exception as e:
            error_msg = f"Speed test failed: {e}"
            self.root.after(0, lambda: self.speed_result.config(text=error_msg))
            self.root.after(0, lambda: self.speed_progress.stop())
            self.root.after(0, lambda: self.speed_button.config(state="normal"))
            self.log_message(f"Speed test error: {e}")
            
    def apply_settings(self):
        """Apply VPN settings."""
        try:
            # Apply technology setting
            tech = self.tech_var.get()
            self.vpn_manager.set_technology(tech)
            
            # Apply protocol setting
            protocol = self.protocol_var.get()
            self.vpn_manager.set_protocol(protocol)
            
            # Apply kill switch setting
            kill_switch = self.kill_switch_var.get()
            self.vpn_manager.set_kill_switch(kill_switch)
            
            # Apply auto connect setting
            auto_connect = self.auto_connect_var.get()
            self.vpn_manager.set_autoconnect(auto_connect)
            
            messagebox.showinfo("Success", "Settings applied successfully")
            self.log_message("Settings applied")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply settings: {e}")
            
    def log_message(self, message: str):
        """Add message to log."""
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        
    def on_closing(self):
        """Handle window closing."""
        self.status_monitor.stop_monitoring()
        self.root.destroy() 