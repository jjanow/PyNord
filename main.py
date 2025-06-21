#!/usr/bin/env python3
"""
PyNord - NordVPN Management Application
A desktop application for managing NordVPN on Kubuntu/Linux
"""

import sys
import os
import logging
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

import tkinter as tk
from tkinter import ttk
from main_window import MainWindow

def setup_logging():
    """Setup logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('pynord.log')
        ]
    )

def main():
    """Main application entry point."""
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # Create Tkinter root window
        root = tk.Tk()
        root.title("PyNord - NordVPN Manager")
        root.geometry("900x700")
        
        # Configure the root window
        root.minsize(800, 600)
        
        # Create and show main window
        app = MainWindow(root)
        
        # Set up window closing handler
        root.protocol("WM_DELETE_WINDOW", app.on_closing)
        
        logger.info("PyNord application started successfully")
        
        # Start event loop
        root.mainloop()
        
    except Exception as e:
        logger.error(f"Failed to start PyNord: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 