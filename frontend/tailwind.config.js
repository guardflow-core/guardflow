/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#31DBC3', // Verde-Água (Inteligência)
        secondary: '#FFB911', // Amarelo Solar (Clareza)
        accent: '#FB4F48', // Vermelho Ético (Energia)
        dark: '#0F1421', // Fundo Noturno
        slate: '#64748B', // Slate Gray
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        heading: ['Montserrat', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
