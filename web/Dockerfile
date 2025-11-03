FROM node:18-alpine AS base
RUN npm install -g pnpm

FROM base AS deps
WORKDIR /app

# Copy root configuration files
COPY package.json ./
COPY pnpm-lock.yaml* ./
COPY pnpm-workspace.yaml* ./
COPY turbo.json ./

# Copy web app package.json
COPY apps/web/package.json ./apps/web/package.json

# Install ALL dependencies (including Next.js)
RUN pnpm install --frozen-lockfile

FROM base AS builder
WORKDIR /app

# Copy package files and node_modules from deps stage
COPY --from=deps /app/node_modules ./node_modules
COPY --from=deps /app/package.json ./
COPY --from=deps /app/pnpm-lock.yaml* ./
COPY --from=deps /app/pnpm-workspace.yaml* ./
COPY --from=deps /app/turbo.json ./

# Copy web app source code
COPY apps/web ./apps/web

# Set working directory to web app and build
WORKDIR /app/apps/web
RUN pnpm run build

FROM nginx:alpine AS runner
COPY --from=builder /app/apps/web/.next /usr/share/nginx/html/.next
COPY --from=builder /app/apps/web/public /usr/share/nginx/html/public
COPY --from=builder /app/apps/web/package.json /usr/share/nginx/html/package.json
# For Next.js standalone output (if using output: 'standalone' in next.config.js)
# COPY --from=builder /app/apps/web/.next/standalone /usr/share/nginx/html
# COPY --from=builder /app/apps/web/.next/static /usr/share/nginx/html/.next/static
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]