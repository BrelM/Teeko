#!/usr/bin/env python3
"""
GUI module verification script
Tests that pygame is available and the GUI module loads correctly
"""

def test_pygame_available():
    """Test if pygame is available"""
    try:
        import pygame
        print("✓ pygame is installed")
        return True
    except ImportError:
        print("✗ pygame is not installed")
        return False

def test_gui_module_loads():
    """Test if GUI module loads"""
    try:
        from src.gui import GameGUI, launch_gui
        print("✓ GUI module loads successfully")
        return True
    except Exception as e:
        print(f"✗ GUI module failed to load: {e}")
        return False

def test_game_controller_integration():
    """Test game controller integration"""
    try:
        from src.gui import GameGUI
        from src.player import Player
        from src.control import GameController
        print("✓ All dependencies available")
        return True
    except Exception as e:
        print(f"✗ Dependency check failed: {e}")
        return False

def test_resources_available():
    """Test that resources exist"""
    from pathlib import Path
    resource_path = Path("resources")
    
    checks = [
        ("Images", resource_path / "images" / "board.jpg"),
        ("Sounds", resource_path / "sounds" / "pawn_move.mp3"),
    ]
    
    all_good = True
    for name, path in checks:
        if path.exists():
            print(f"✓ {name} found: {path}")
        else:
            print(f"⚠ {name} not found: {path} (optional)")
    
    return all_good

if __name__ == "__main__":
    print("\nTeeko GUI Module Verification")
    print("="*50)
    
    print("\n1. Checking pygame installation...")
    pygame_ok = test_pygame_available()
    
    print("\n2. Checking GUI module...")
    gui_ok = test_gui_module_loads()
    
    print("\n3. Checking dependencies...")
    deps_ok = test_game_controller_integration()
    
    print("\n4. Checking resources...")
    res_ok = test_resources_available()
    
    print("\n" + "="*50)
    if pygame_ok and gui_ok and deps_ok:
        print("✓ All checks passed! GUI is ready to use.")
        print("\nTo start the GUI, run:")
        print("  python play.py")
    else:
        print("✗ Some checks failed. Please install pygame:")
        print("  pip install pygame")
    print("="*50 + "\n")
