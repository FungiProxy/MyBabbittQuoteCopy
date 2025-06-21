# Theme Switching Guide

## Overview

The Babbitt Quote Generator now supports multiple themes that can be switched dynamically through the settings interface. This guide explains how the theme system works and how to use it.

## Available Themes

The application includes the following themes:

1. **Babbitt Theme** - Classic industrial blue theme with gold accents
2. **Babbitt Professional** - Enhanced professional version with refined styling
3. **Modern Babbitt** - Modern interpretation with updated color scheme
4. **Modern Light** - Clean, light theme with modern aesthetics
5. **Corporate** - Professional corporate theme with sophisticated styling

## How to Switch Themes

### Through the Settings Interface

1. **Open Settings**: Click the "⚙️ Settings" button in the sidebar
2. **Select Theme**: In the "General" section, use the dropdown to select your preferred theme
3. **Preview**: The "Theme Preview" section shows color samples for each theme
4. **Apply**: The theme is applied immediately when you change the selection
5. **Save**: Click "Save Settings" to persist your theme choice

### Theme Preview

The settings page includes a visual preview section that shows:
- Theme name
- Primary color sample
- Accent color sample  
- Background color sample
- Theme description

## Technical Implementation

### Theme Manager

The `ThemeManager` class (`src/ui/theme/theme_manager.py`) provides:
- `get_available_themes()` - Returns list of all available themes
- `apply_theme(theme_name, app)` - Applies a theme to the application
- `get_theme_preview_info(theme_name)` - Returns theme preview information

### Settings Integration

Themes are managed through the `SettingsService`:
- `get_theme()` - Retrieves the current theme setting
- `set_theme(theme_name)` - Saves the selected theme
- Settings are persisted using QSettings for platform-independent storage

### Main Window Integration

The `MainWindowRedesign` class:
- Loads the saved theme on startup
- Handles theme changes from the settings page
- Applies themes to the entire application using `ThemeManager`

## Theme Structure

Each theme is implemented as a separate class with:
- Color constants (primary, accent, background colors)
- `get_main_stylesheet()` method returning CSS styles
- Consistent styling across all UI components

## Testing Theme Switching

You can test theme switching using the provided test script:

```bash
python test_theme_switching.py
```

This opens a simple test window with buttons to apply each theme and verify functionality.

## Customization

### Adding New Themes

To add a new theme:

1. Create a new theme class in `src/ui/theme/`
2. Implement the required methods and color constants
3. Add the theme to the `THEMES` dictionary in `ThemeManager`
4. The theme will automatically appear in the settings interface

### Modifying Existing Themes

Each theme file can be modified to:
- Change color schemes
- Update styling rules
- Add new component styles
- Modify layout and spacing

## Best Practices

1. **Consistency**: Maintain consistent styling patterns across themes
2. **Accessibility**: Ensure sufficient contrast ratios for readability
3. **Performance**: Keep stylesheets efficient and avoid redundant rules
4. **Testing**: Test themes across different screen sizes and resolutions

## Troubleshooting

### Common Issues

1. **Theme not applying**: Check that the theme name matches exactly in the ThemeManager
2. **CSS errors**: Look for unsupported CSS properties (PySide6 doesn't support all CSS3 features)
3. **Settings not saving**: Verify QSettings permissions and storage location

### Debug Information

The application logs theme changes:
```
INFO:src.ui.main_window_redesign:Applied theme: Modern Babbitt
```

Check the console output for theme application status and any errors.

## Future Enhancements

Potential improvements for the theme system:
- Theme import/export functionality
- Custom theme creation interface
- Theme-specific icon sets
- Dark/light mode variants
- User-defined color schemes 