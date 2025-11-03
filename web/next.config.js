/** @type {import('next').NextConfig} */
const withNextIntl = require('next-intl/plugin')('./i18n/request.ts');

const nextConfig = {
  output: 'standalone',
  reactStrictMode: true,
  images: {
    domains: ['localhost'],
  },
};

const configWithIntl = withNextIntl(nextConfig);

module.exports = {
  ...configWithIntl,
  env: {
    ...configWithIntl.env,
    _next_intl_trailing_slash: configWithIntl.env?._next_intl_trailing_slash ?? 'false',
  },
};

