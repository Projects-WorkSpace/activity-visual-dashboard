export default defineNuxtConfig({
    css: ['~/assets/styles/tailwind.css', '~/assets/styles/global.css'],
    modules: ['@nuxtjs/tailwindcss', '@pinia/nuxt'],
    app: {
        pageTransition: { name: 'page', mode: 'out-in' },
        layoutTransition: { name: 'layout', mode: 'out-in' },
    },
    build: {
        transpile: [/echarts/, /zrender/],
    },
    runtimeConfig: {
        public: {
            apiBase: '/api',
        },
    },
    routeRules: {
        '/reports': { ssr: false },
    },
});
