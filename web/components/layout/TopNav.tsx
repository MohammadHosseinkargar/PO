'use client';

import { useTranslations } from 'next-intl';
import { usePathname } from 'next/navigation';
import { Menu, Sun, Moon, Bell, Search } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import type { User } from '@/lib/auth/auth';
import { useAuth } from '@/lib/auth/AuthContext';
import { locales, localeMetadata } from '@/lib/config';

interface TopNavProps {
  onMenuButtonClick: () => void;
  onThemeToggle: () => void;
  user: User;
  theme?: string;
}

export function TopNav({
  onMenuButtonClick,
  onThemeToggle,
  user,
  theme,
}: TopNavProps) {
  const t = useTranslations();
  const pathname = usePathname();
  const { logout } = useAuth();

  // Get current locale and its metadata
  const currentLocale = pathname.split('/')[1];
  const currentLocaleMetadata = localeMetadata[currentLocale as keyof typeof localeMetadata];

  // Get next locale (cycling through available locales)
  const currentIndex = locales.indexOf(currentLocale);
  const nextLocale = locales[(currentIndex + 1) % locales.length];
  const nextLocalePath = pathname.replace(`/${currentLocale}`, `/${nextLocale}`);

  return (
    <header className="border-b">
      <div className="flex h-16 items-center px-4">
        <Button
          variant="ghost"
          size="icon"
          className="lg:hidden"
          onClick={onMenuButtonClick}
        >
          <Menu className="h-5 w-5" />
        </Button>

        <div className="flex flex-1 items-center gap-4 md:gap-8">
          {/* Search */}
          <form className="flex-1 md:flex-initial">
            <div className="relative">
              <Search className="absolute start-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
              <Input
                type="search"
                placeholder={t('common.search')}
                className="w-full bg-muted pe-4 ps-9 md:w-[300px]"
              />
            </div>
          </form>
        </div>

        <div className="flex items-center gap-2">
          {/* Theme toggle */}
          <Button
            variant="ghost"
            size="icon"
            onClick={onThemeToggle}
          >
            {theme === 'dark' ? (
              <Sun className="h-5 w-5" />
            ) : (
              <Moon className="h-5 w-5" />
            )}
          </Button>

          {/* Language toggle */}
          <Button
            variant="ghost"
            size="sm"
            className="hidden md:inline-flex"
            asChild
          >
            <a href={nextLocalePath} hrefLang={nextLocale}>
              {localeMetadata[nextLocale as keyof typeof localeMetadata].name}
            </a>
          </Button>

          {/* Notifications */}
          <Button variant="ghost" size="icon">
            <Bell className="h-5 w-5" />
          </Button>

          {/* User menu */}
          <Button
            variant="ghost"
            onClick={() => logout()}
            className="hidden md:inline-flex"
          >
            {t('auth.logout')}
          </Button>
        </div>
      </div>
    </header>
  );
}