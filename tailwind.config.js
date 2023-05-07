/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
	"./ratings/**/*.{html,js}",
    "./node_modules/flowbite/**/*.js"
  ],
  theme: {
    extend: {},
  },
  plugins: [
  	  require('flowbite/plugin'),
  	  require('flowbite-typography')
  ],
}
