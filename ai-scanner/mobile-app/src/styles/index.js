/**
 * Styles Index
 * QuickFlow Mobile App
 */

// Colors
export const colors = {
  primary: {
    green: '#00C851',
    blue: '#007BFF',
    purple: '#6F42C1',
  },
  secondary: {
    success: '#28A745',
    warning: '#FD7E14',
    error: '#DC3545',
    info: '#17A2B8',
  },
  gray: {
    dark: '#343A40',
    medium: '#6C757D',
    light: '#F8F9FA',
  },
  white: '#FFFFFF',
  black: '#000000',
  transparent: 'transparent',
  
  // Gradients
  gradients: {
    primary: ['#00C851', '#007BFF'],
    success: ['#28A745', '#20C997'],
    hero: ['rgba(0, 200, 81, 0.1)', 'rgba(0, 123, 255, 0.1)'],
  },
  
  // Semantic colors
  background: '#FFFFFF',
  surface: '#F8F9FA',
  text: {
    primary: '#343A40',
    secondary: '#6C757D',
    inverse: '#FFFFFF',
  },
  border: '#E9ECEF',
  shadow: 'rgba(0, 0, 0, 0.1)',
};

// Typography
export const typography = {
  fonts: {
    regular: 'Inter-Regular',
    medium: 'Inter-Medium',
    semiBold: 'Inter-SemiBold',
    bold: 'Inter-Bold',
  },
  sizes: {
    xs: 12,
    sm: 14,
    base: 16,
    lg: 18,
    xl: 20,
    '2xl': 24,
    '3xl': 30,
    '4xl': 36,
    '5xl': 48,
  },
  lineHeights: {
    tight: 1.2,
    normal: 1.4,
    relaxed: 1.6,
  },
  letterSpacing: {
    tight: -0.5,
    normal: 0,
    wide: 0.5,
  },
};

// Spacing
export const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  '2xl': 48,
  '3xl': 64,
};

// Border Radius
export const borderRadius = {
  none: 0,
  sm: 4,
  md: 8,
  lg: 12,
  xl: 16,
  '2xl': 24,
  full: 9999,
};

// Shadows
export const shadows = {
  sm: {
    shadowOffset: {width: 0, height: 1},
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 2,
  },
  md: {
    shadowOffset: {width: 0, height: 2},
    shadowOpacity: 0.15,
    shadowRadius: 4,
    elevation: 4,
  },
  lg: {
    shadowOffset: {width: 0, height: 4},
    shadowOpacity: 0.2,
    shadowRadius: 8,
    elevation: 8,
  },
  xl: {
    shadowOffset: {width: 0, height: 8},
    shadowOpacity: 0.25,
    shadowRadius: 16,
    elevation: 16,
  },
};

// Layout
export const layout = {
  window: {
    width: 375, // Base iPhone width
    height: 812, // Base iPhone height
  },
  container: {
    paddingHorizontal: spacing.md,
  },
  section: {
    paddingVertical: spacing.lg,
  },
};

// Animation
export const animation = {
  timing: {
    fast: 200,
    normal: 300,
    slow: 500,
  },
  easing: {
    ease: 'ease',
    easeIn: 'ease-in',
    easeOut: 'ease-out',
    easeInOut: 'ease-in-out',
  },
};

// Z-Index
export const zIndex = {
  hide: -1,
  base: 0,
  dropdown: 1000,
  sticky: 1020,
  fixed: 1030,
  modal: 1040,
  popover: 1050,
  tooltip: 1060,
  toast: 1070,
};

// Component Styles
export const components = {
  button: {
    height: 48,
    borderRadius: borderRadius.md,
    paddingHorizontal: spacing.lg,
  },
  input: {
    height: 48,
    borderRadius: borderRadius.md,
    paddingHorizontal: spacing.md,
    borderWidth: 1,
    borderColor: colors.border,
  },
  card: {
    backgroundColor: colors.white,
    borderRadius: borderRadius.lg,
    padding: spacing.md,
    ...shadows.md,
  },
  header: {
    height: 56,
    backgroundColor: colors.white,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
  },
};

// Export all styles
export default {
  colors,
  typography,
  spacing,
  borderRadius,
  shadows,
  layout,
  animation,
  zIndex,
  components,
};



