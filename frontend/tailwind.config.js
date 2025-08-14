import defaultTheme from 'tailwindcss/defaultTheme';

/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', ...defaultTheme.fontFamily.sans],
      },
      colors: {
        primary: {
          DEFAULT: '#4338ca', // Using indigo-700
          '50': '#eef2ff',
          '100': '#e0e7ff',
          '600': '#4f46e5',
          '700': '#4338ca',
        }
      }
    },
  },
  plugins: [],
};