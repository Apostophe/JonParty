import theme from './assets/theme';
import { fr } from 'vuetify/locale';


export default defineNuxtConfig({
  compatibilityDate: '2024-04-03',
  css: ['~/assets/scss/base.scss', '~/assets/scss/utilities.scss'],
  devtools: { enabled: true },
  modules: ['vuetify-nuxt-module'],
  vuetify: {
    moduleOptions: {
      styles: { configFile: 'assets/scss/settings.scss' },
    },
    vuetifyOptions: {
      icons: {
        defaultSet: 'mdi-svg',
      },
      locale: {
        locale: 'fr',
        messages: { fr },
      },
      defaults: {
        global: {
          // Disable the ripple effect on components that support it
          ripple: false,
        },
        VTextField: {
          variant: 'outlined',
          color: 'naval-blue-40',
        },
        VCheckbox: {
          color: 'naval-blue-40',
        },
      },
      theme: {
        defaultTheme: 'ce',
        themes: {
          ce: theme,
        },
      },
    },
  },
  vite: {
    css: {
      preprocessorOptions: {
        scss: {
          additionalData: '@use "~/assets/scss/abstracts" as *;',
        },
      },
    },
  },
})