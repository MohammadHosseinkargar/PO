export const locales = ['en', 'fa'] as const;
export type Locale = typeof locales[number];

export const defaultLocale = 'en' as const;

// Define metadata for each locale
export const localeMetadata = {
  en: {
    name: 'English',
    dir: 'ltr',
  },
  fa: {
    name: 'فارسی',
    dir: 'rtl',
  },
} as const;