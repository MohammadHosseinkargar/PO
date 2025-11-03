import {ReactNode} from 'react';
import {notFound} from 'next/navigation';
import {NextIntlClientProvider} from 'next-intl';
import {unstable_setRequestLocale} from 'next-intl/server';
import {locales, localeMetadata, type Locale} from '@/lib/config';
import {AuthProvider} from '@/lib/auth/AuthContext';

export function generateStaticParams() {
  return locales.map((locale) => ({locale}));
}

export default async function LocaleLayout({
  children,
  params: {locale}
}: {
  children: ReactNode;
  params: {locale: string};
}) {
  if (!locales.includes(locale as Locale)) notFound();

  const currentLocale = locale as Locale;
  unstable_setRequestLocale(currentLocale);

  let messages;
  try {
    messages = (await import(`../../messages/${currentLocale}.json`)).default;
  } catch (error) {
    notFound();
  }

  return (
    <html lang={currentLocale} dir={localeMetadata[currentLocale].dir}>
      <body>
        <AuthProvider>
          <NextIntlClientProvider locale={currentLocale} messages={messages}>
            {children}
          </NextIntlClientProvider>
        </AuthProvider>
      </body>
    </html>
  );
}
