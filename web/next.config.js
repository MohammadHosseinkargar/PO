/** @type {import('next').NextConfig} */
const withNextIntl = require('next-intl/plugin')();

const nextConfig = {
  output: 'standalone',
  reactStrictMode: true,
  images: {
    domains: ['localhost'],
  },
  // Enable edge runtime for better i18n performance
  experimental: {
    runtime: 'edge',
  },
};
module.exports = withNextIntl(nextConfig);