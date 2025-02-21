/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontSize: {
        'tiny': '0.7rem',
        'mid': '14px',   
        'huge': '3rem',      
        'xxl': '2.5rem',    
      },
      colors: {
        primary: '#E48320', 
        secondary: '#EFF5F7',
        teritary: '#69A8A3', 
        four: '#000', 
      },
      height: {
        'custom-height': '550px',
        'about-height': '480px', 
      },
    },
  },
  plugins: [],
}

