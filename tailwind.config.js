/** @type {import('tailwindcss').Config} */
module.exports = {
	content: [
		"./templates/**/*.html",
		"./static/src/**/*.js",
		"./node_modules/flowbite/**/*.js"
	],
	theme: {
		extend: {
			colors: {
				primary: '#363062',
				secondary: '#4D4C7D',
				third: '#F99417',
				fourth: '#F5F5F5',
				fifth: '#6CA460',
				text: '#F5F5F5',
			},
			fontFamily: {
				lobster: ["Lobster Two", 'sans-serif'],
				kanit: ["Kanit", 'sans-serif'],
				hind: ["Hind", 'sans-serif'],
				montserrat: ['Montserrat', 'sans-serif'],
			},
		},
	},
	plugins: [
		require("flowbite/plugin")
	],
}