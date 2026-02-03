/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    darkMode: "class",
    theme: {
        extend: {
            colors: {
                "primary": "#137fec",
                "primary-dark": "#0b5cb5",
                "background-light": "#f6f7f8",
                "background-dark": "#0f172a",
                "glass-border": "rgba(255, 255, 255, 0.08)",
                "glass-bg": "rgba(30, 41, 59, 0.4)",
            },
            fontFamily: {
                "display": ["Space Grotesk", "sans-serif"],
                "body": ["Noto Sans", "sans-serif"],
            },
            backgroundImage: {
                'grid-pattern': "url(\"data:image/svg+xml,%3Csvg width='40' height='40' viewBox='0 0 40 40' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M0 0h40v40H0V0zm1 1h38v38H1V1z' fill='%23ffffff' fill-opacity='0.03' fill-rule='evenodd'/%3E%3C/svg%3E\")",
                'premium-gradient': 'radial-gradient(circle at 15% 50%, rgba(19, 127, 236, 0.08), transparent 25%), radial-gradient(circle at 85% 30%, rgba(147, 51, 234, 0.05), transparent 25%)'
            },
            boxShadow: {
                'neon': '0 0 20px -5px rgba(19, 127, 236, 0.5)',
                'glass': '0 8px 32px 0 rgba(0, 0, 0, 0.37)',
            }
        },
    },
    plugins: [],
}
