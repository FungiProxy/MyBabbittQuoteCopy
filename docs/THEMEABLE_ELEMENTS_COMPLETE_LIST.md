# Complete List of Themeable Elements

## Overview

This document provides a comprehensive list of all themeable elements in the Babbitt Quote Generator application. The theming system supports multiple themes with sophisticated styling, animations, and visual hierarchy.

## Available Themes

1. **Babbitt Industrial** - Premium industrial theme with sophisticated gradients and animations
2. **Babbitt Theme** - Classic corporate theme with blue gradient sidebar
3. **Dark Theme** - Dark mode variant with sophisticated styling
4. **Modern Babbitt** - Modern interpretation with updated color scheme

## Main Window Elements

### Sidebar (QFrame#sidebarFrame)
- **Background**: Gradient from charcoal to dark steel
- **Border**: Right border with transparency
- **Width**: Fixed 220px (industrial) / 260px (corporate)
- **Shadow**: Premium drop shadow effects

### Logo Label (QLabel#logoLabel)
- **Color**: Pure white text
- **Font**: Bold, centered
- **Size**: Large, prominent display

### Navigation List (QListWidget#navList)
- **Background**: Transparent
- **Item styling**: Hover effects with slide animations
- **Selection**: Inset shadow effects
- **Text color**: White with transparency
- **Hover animations**: Slide right by 4px

### Settings Button (QPushButton#settingsButton)
- **Background**: Semi-transparent white gradient
- **Border**: White border with transparency
- **Text color**: White with transparency
- **Hover effects**: Enhanced transparency and border
- **Press effects**: Reduced transparency

## Content Area Elements

### Content Frame (QFrame#contentAreaFrame)
- **Background**: Pure white
- **Layout**: Full-width content area

### Header Frame (QFrame#contentHeader)
- **Background**: Gradient from white to light gray
- **Border**: Bottom border with gray
- **Height**: Fixed 70px
- **Padding**: 32px horizontal, 20px vertical

### Page Title (QLabel#pageTitle)
- **Color**: Dark gray (primary text)
- **Font**: 28px, bold, negative letter spacing
- **Margin**: None

### Action Button (QPushButton with class="primary")
- **Background**: Orange gradient
- **Text color**: White
- **Border**: Orange border
- **Hover effects**: Enhanced orange gradient
- **Press effects**: Darker orange gradient

## Dashboard Elements

### Statistics Cards (QFrame with class="statCard")
- **Background**: Pure white
- **Border**: Light gray border
- **Border radius**: 8px
- **Padding**: 24px
- **Shadow**: Card shadow (0 2px 8px rgba(0, 0, 0, 0.1))
- **Hover animations**: Lift up by 2px + premium shadow

### Stat Title (QLabel with class="statTitle")
- **Color**: Charcoal gray
- **Font**: Bold, uppercase transform
- **Size**: 14px

### Stat Value (QLabel with class="statValue")
- **Color**: Primary blue
- **Font**: Large, bold
- **Size**: 24px+

### Stat Subtitle (QLabel with class="statSubtitle")
- **Color**: Secondary gray
- **Font**: Regular weight
- **Size**: 12px

### Stat Icon (QLabel with class="statIcon")
- **Color**: Accent color
- **Size**: Large emoji display

## Form Elements

### Input Fields (QLineEdit)
- **Background**: White
- **Border**: Gray border with rounded corners
- **Focus effects**: Blue glow (0 0 0 3px rgba(0, 82, 204, 0.3))
- **Padding**: 12px
- **Font**: 14px

### Combo Boxes (QComboBox)
- **Background**: White
- **Border**: Gray border with rounded corners
- **Dropdown arrow**: Custom styling
- **Focus effects**: Blue glow
- **Hover effects**: Light blue background

### Spin Boxes (QSpinBox)
- **Background**: White
- **Border**: Gray border with rounded corners
- **Up/down arrows**: Custom styling
- **Focus effects**: Blue glow
- **Number display**: Bold styling

### Buttons (QPushButton)
- **Primary buttons**: Blue gradient background
- **Secondary buttons**: Gray background
- **Border**: Rounded corners (8px)
- **Padding**: 12px horizontal, 24px vertical
- **Hover animations**: Lift up by 1px
- **Press animations**: Press down by 1px
- **Shadow effects**: Button shadows with color

## Dialog Elements

### Dialog Windows (QDialog)
- **Background**: White
- **Border**: Rounded corners
- **Shadow**: Elevated shadow (0 8px 32px rgba(0, 0, 0, 0.2))
- **Title bar**: Custom styling

### Dialog Buttons
- **Primary**: Blue gradient with white text
- **Secondary**: Gray with dark text
- **Cancel**: Red or gray styling
- **Hover effects**: Enhanced gradients
- **Press effects**: Darker gradients

## Product Selection Dialog

### Product List (QListWidget)
- **Background**: Light gray
- **Item styling**: White background with hover effects
- **Selection**: Blue background with white text
- **Border**: Rounded corners

### Configuration Panels (QFrame)
- **Background**: Light gray
- **Border**: Rounded corners
- **Padding**: 16px
- **Header styling**: Bold titles

### Price Labels
- **Base price**: Gray, 14px
- **Total price**: Blue, 18px, bold
- **Adder prices**: Colored badges (green/red/gray)

### Progress Bar (QProgressBar)
- **Background**: Light gray
- **Progress**: Blue gradient
- **Border**: Rounded corners
- **Text**: White, centered

## Status Indicators

### Success Status (QLabel with status="success")
- **Color**: Green (#38a169)
- **Font**: Bold

### Warning Status (QLabel with status="warning")
- **Color**: Amber (#d69e2e)
- **Font**: Bold

### Error Status (QLabel with status="error")
- **Color**: Red (#e53e3e)
- **Font**: Bold

### Info Status (QLabel with status="info")
- **Color**: Cyan (#0987a0)
- **Font**: Bold

## Animation System

### Hover Animations
- **Navigation items**: Slide right by 4px
- **Cards**: Lift up by 2px
- **Buttons**: Lift up by 1px
- **Duration**: 200ms with OutCubic easing

### Press Animations
- **Buttons**: Press down by 1px
- **Duration**: 100ms with OutQuad easing

### Shadow Transitions
- **Card shadow**: 0 2px 8px rgba(0, 0, 0, 0.1)
- **Premium shadow**: 0 4px 16px rgba(0, 0, 0, 0.15)
- **Elevated shadow**: 0 8px 32px rgba(0, 0, 0, 0.2)
- **Button shadow**: 0 2px 8px rgba(0, 82, 204, 0.15)

### Focus Effects
- **Glow**: 0 0 0 3px rgba(0, 82, 204, 0.3)
- **Duration**: Instant application

## Color Palette

### Primary Colors
- **Primary Blue**: #0052cc (industrial) / #1e40af (corporate)
- **Secondary Blue**: #003d99 (industrial) / #1d4ed8 (corporate)
- **Accent Blue**: #0066ff (industrial) / #3b82f6 (corporate)

### Dark Colors
- **Charcoal**: #1a1a1a
- **Dark Steel**: #2d3748
- **Gunmetal**: #4a5568

### Gray Scale
- **Platinum**: #f7fafc (lightest background)
- **Silver**: #edf2f7 (secondary background)
- **Steel Gray**: #e2e8f0 (borders)
- **Charcoal Gray**: #718096 (secondary text)
- **Iron Gray**: #4a5568 (primary text)

### Status Colors
- **Success Green**: #38a169
- **Warning Amber**: #d69e2e
- **Error Red**: #e53e3e
- **Info Cyan**: #0987a0

### Accent Colors
- **Gold Accent**: #d69e2e
- **Copper Accent**: #dd6b20
- **Steel Accent**: #718096

## Typography

### Font Family
- **Primary**: 'Segoe UI', 'Roboto', 'San Francisco', 'Helvetica Neue', sans-serif

### Font Sizes
- **Base**: 14px
- **Large**: 18px
- **Extra Large**: 24px+
- **Small**: 12px
- **Extra Small**: 10px

### Font Weights
- **Regular**: 400
- **Medium**: 500
- **Semi-bold**: 600
- **Bold**: 700

## Spacing System

### Margins and Padding
- **Section spacing**: 24px
- **Group spacing**: 16px
- **Field spacing**: 12px
- **Element spacing**: 8px
- **Tight spacing**: 4px

### Border Radius
- **Small**: 4px
- **Medium**: 8px
- **Large**: 12px
- **Extra Large**: 16px

## Interactive States

### Hover Overlays
- **Light overlay**: rgba(0, 82, 204, 0.08)
- **Medium overlay**: rgba(0, 82, 204, 0.12)

### Focus States
- **Glow effect**: 0 0 0 3px rgba(0, 82, 204, 0.3)
- **Border color**: Primary blue

### Disabled States
- **Background**: Light gray
- **Text**: Medium gray
- **Opacity**: 0.6

## Theme Switching

### Settings Integration
- **Theme dropdown**: Available themes list
- **Preview widgets**: Color samples for each theme
- **Apply button**: Immediate theme application
- **Persistence**: QSettings storage

### Animation Transitions
- **Smooth transitions**: 200ms duration
- **Easing curves**: OutCubic for natural feel
- **Property animations**: Position, shadow, opacity

## Customization Guidelines

### Adding New Themes
1. Create theme class with color constants
2. Implement `get_main_stylesheet()` method
3. Add to ThemeManager's available themes
4. Include preview information

### Modifying Existing Themes
1. Update color constants
2. Modify stylesheet rules
3. Test across all components
4. Verify accessibility contrast

### Best Practices
- Maintain consistent color hierarchy
- Ensure sufficient contrast ratios
- Use semantic color naming
- Test animations performance
- Support both light and dark variants

## Accessibility Considerations

### Color Contrast
- **Text on background**: Minimum 4.5:1 ratio
- **Large text**: Minimum 3:1 ratio
- **UI components**: Minimum 3:1 ratio

### Focus Indicators
- **Visible focus**: Blue glow effect
- **Keyboard navigation**: Full support
- **Screen readers**: Proper labeling

### Animation Preferences
- **Reduced motion**: Respect user preferences
- **Duration control**: Configurable timing
- **Disable option**: User choice support 