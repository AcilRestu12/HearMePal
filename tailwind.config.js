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
				primary: '#E88D67',
				secondary: '#F3F7EC',
				third: '#006989',
				fourth: '#005C78',
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