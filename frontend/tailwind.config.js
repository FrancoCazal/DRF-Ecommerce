/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        'primary': '#9b000d',
        'primary-container': '#c02020',
        'on-primary': '#ffffff',
        'background': '#fcf9f6',
        'surface': '#fcf9f6',
        'surface-container': '#f0edea',
        'surface-container-low': '#f6f3f0',
        'surface-container-high': '#eae8e5',
        'surface-container-highest': '#e5e2df',
        'on-surface': '#1c1c1a',
        'on-background': '#1c1c1a',
        'secondary': '#5f5e5e',
        'outline': '#8f6f6c',
        'outline-variant': '#e4beb9',
        'error': '#ba1a1a',
      },
      borderRadius: {
        DEFAULT: '0px',
        sm: '0px',
        md: '0px',
        lg: '0px',
        xl: '0px',
        '2xl': '0px',
        '3xl': '0px',
        full: '0px',
      },
      fontFamily: {
        headline: ['Space Grotesk', 'sans-serif'],
        body: ['Manrope', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
