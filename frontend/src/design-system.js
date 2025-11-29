// Design System - Single source of truth for our visual design
export const colors = {
  // Neutral base colors
  neutral: {
    50: '#fafafa',   // backgrounds
    100: '#f5f5f5',  // subtle backgrounds
    200: '#e5e5e5',  // borders
    300: '#d4d4d4',  // disabled states
    400: '#a3a3a3',  // placeholders
    500: '#737373',  // secondary text
    600: '#525252',  // primary text
    700: '#404040',  // headings
    800: '#262626',  // emphasis
    900: '#171717',  // maximum contrast
  },
  
  // Amber accent system
  accent: {
    50: '#fffbeb',
    100: '#fef3c7',
    200: '#fde68a',
    300: '#fcd34d',
    400: '#fbbf24',  // Primary accent
    500: '#f59e0b',
    600: '#d97706',
    700: '#b45309',
    800: '#92400e',
    900: '#78350f',
  },
  
  // Semantic colors (subtle, not aggressive)
  success: '#10b981',    // emerald-500
  warning: '#f59e0b',    // amber-500  
  error: '#ef4444',      // red-500 (muted)
  info: '#3b82f6',       // blue-500
}

export const spacing = {
  xs: '0.5rem',    // 8px
  sm: '0.75rem',   // 12px
  md: '1rem',      // 16px
  lg: '1.5rem',    // 24px
  xl: '2rem',      // 32px
  '2xl': '3rem',   // 48px
}

export const borderRadius = {
  card: '12px',
  button: '8px',
  input: '6px',
}

export const shadows = {
  card: '0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)',
  cardHover: '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
}

export const typography = {
  // Font sizes following a scale
  xs: '0.75rem',   // 12px
  sm: '0.875rem',  // 14px
  base: '1rem',    // 16px
  lg: '1.125rem',  // 18px
  xl: '1.25rem',   // 20px
  '2xl': '1.5rem', // 24px
  '3xl': '1.875rem', // 30px
}