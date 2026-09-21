/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        background: '#0D0E12',
        card: '#13141B',
        'card-hover': '#181A23',
        secondary: '#1C1D26',
        border: '#252733',
        'border-light': '#323544',
        primary: {
          DEFAULT: '#F5BE38',
          hover: '#E5AF2F',
          foreground: '#0D0E12',
          muted: 'rgba(245, 190, 56, 0.15)',
        },
        destructive: {
          DEFAULT: '#FF5C67',
          hover: '#E84A55',
          foreground: '#FFFFFF',
          muted: 'rgba(255, 92, 103, 0.15)',
        },
        warning: {
          DEFAULT: '#F5BE38',
          muted: 'rgba(245, 190, 56, 0.15)',
        },
        success: {
          DEFAULT: '#3DD68C',
          muted: 'rgba(61, 214, 140, 0.15)',
        },
        muted: {
          DEFAULT: '#1E202B',
          foreground: '#9E9FA9',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
      },
      borderRadius: {
        'xl': '12px',
        '2xl': '16px',
      }
    },
  },
  plugins: [],
}
