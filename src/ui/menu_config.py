"""
Configuration settings for the menu system
"""

from dataclasses import dataclass
from typing import List, Tuple
from PySide6.QtGui import QColor


@dataclass
class MenuCardConfig:
    """Configuration for menu cards"""
    
    # Card dimensions
    height: int = 100
    width: int = 650
    
    # Styling
    border_radius: int = 12
    border_width: int = 1
    border_color: str = "rgba(255, 255, 255, 0.1)"
    hover_border_color: str = "rgba(255, 255, 255, 0.2)"
    
    # Spacing
    margins: Tuple[int, int, int, int] = (20, 16, 20, 16)
    spacing: int = 16
    
    # Icon settings
    icon_size: int = 40
    icon_pixmap_size: int = 28
    icon_background: str = "rgba(255, 255, 255, 0.1)"
    icon_border_radius: int = 8
    
    # Typography
    title_font_size: int = 18
    title_font_family: str = "Cascadia Code"
    subtitle_font_size: int = 12
    subtitle_font_family: str = "Cascadia Code"
    
    # Colors
    title_color: str = "white"
    subtitle_color: str = "rgba(255, 255, 255, 0.85)"
    
    # Hover effects
    hover_lighten_factor: float = 0.1
    press_darken_factor: float = 0.1


@dataclass
class MiniCardConfig:
    """Configuration for mini cards"""
    
    # Card dimensions
    width: int = 150
    height: int = 65
    
    # Styling
    border_radius: int = 10
    border_width: int = 1
    border_color: str = "rgba(255, 255, 255, 0.1)"
    hover_border_color: str = "rgba(255, 255, 255, 0.2)"
    
    # Spacing
    margins: Tuple[int, int, int, int] = (14, 14, 14, 14)
    spacing: int = 12
    
    # Icon settings
    icon_size: int = 20
    icon_pixmap_size: int = 20
    
    # Typography
    title_font_size: int = 13
    title_font_family: str = "Cascadia Code"
    
    # Colors
    title_color: str = "white"
    
    # Hover effects
    hover_lighten_factor: float = 0.1
    press_darken_factor: float = 0.1


@dataclass
class MenuLayoutConfig:
    """Configuration for menu layout"""
    
    # Main layout - COMPACT SPACING
    main_margins: Tuple[int, int, int, int] = (30, 5, 30, 15)  # Reduced top margin from 15 to 5
    main_spacing: int = 15  # Reduced spacing between sections
    
    # Cards layout
    cards_spacing: int = 40  # More spaced out - equidistant spacing between main cards
    
    # Secondary layout
    secondary_spacing: int = 40  # More spaced out - equidistant spacing between secondary cards
    
    # Banner container
    banner_height: int = 240
    banner_width: int = 720
    
    # Card colors
    study_color: str = "#2563EB"
    decks_color: str = "#059669"
    timer_color: str = "#D97706"
    stats_color: str = "#7C3AED"
    exit_color: str = "#DC2626"
    
    # Icons
    study_icon: str = "sword-svgrepo-com.svg"
    decks_icon: str = "tomato-svgrepo-com.svg"
    timer_icon: str = "clock-svgrepo-com.svg"
    stats_icon: str = "research-svgrepo-com.svg"
    exit_icon: str = "school-bell-svgrepo-com.svg"
