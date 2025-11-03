'use client';

import { useTranslations } from 'next-intl';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  LayoutDashboard,
  ShoppingBag,
  Package,
  Users,
  BarChart,
  Settings,
  X,
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { User } from '@/lib/auth/auth';

const navigation = [
  { name: 'nav.dashboard', href: '/dashboard', icon: LayoutDashboard },
  { name: 'nav.products', href: '/dashboard/products', icon: ShoppingBag },
  { name: 'nav.inventory', href: '/dashboard/inventory', icon: Package },
  { name: 'nav.suppliers', href: '/dashboard/suppliers', icon: Users },
  { name: 'nav.reports', href: '/dashboard/reports', icon: BarChart },
  { name: 'nav.settings', href: '/dashboard/settings', icon: Settings },
];

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
  user: User;
}

export function Sidebar({ isOpen, onClose, user }: SidebarProps) {
  const t = useTranslations();
  const pathname = usePathname();

  return (
    <>
      {/* Mobile backdrop */}
      <div
        className={cn(
          'fixed inset-0 z-40 bg-background/80 backdrop-blur-sm lg:hidden',
          {
            hidden: !isOpen,
          }
        )}
        onClick={onClose}
      />

      {/* Sidebar */}
      <div
        className={cn(
          'fixed inset-y-0 start-0 z-50 w-72 bg-background shadow-lg transition-transform duration-200 lg:static lg:translate-x-0',
          {
            'translate-x-0': isOpen,
            '-translate-x-full': !isOpen,
          }
        )}
      >
        <div className="flex h-full flex-col gap-2">
          {/* Header */}
          <div className="flex h-16 items-center justify-between px-4">
            <Link
              href="/dashboard"
              className="text-xl font-semibold"
            >
              {t('app.title')}
            </Link>
            <Button
              variant="ghost"
              size="icon"
              className="lg:hidden"
              onClick={onClose}
            >
              <X className="h-5 w-5" />
            </Button>
          </div>

          {/* Navigation */}
          <nav className="flex-1 space-y-1 px-2">
            {navigation.map((item) => {
              const isActive = pathname === item.href;
              return (
                <Link
                  key={item.name}
                  href={item.href}
                  className={cn(
                    'group flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium hover:bg-accent hover:text-accent-foreground',
                    {
                      'bg-accent text-accent-foreground': isActive,
                      'text-foreground/60': !isActive,
                    }
                  )}
                >
                  <item.icon className="h-5 w-5" />
                  {t(item.name)}
                </Link>
              );
            })}
          </nav>

          {/* User info */}
          <div className="border-t p-4">
            <div className="flex items-center gap-3">
              <div className="h-8 w-8 rounded-full bg-accent" />
              <div>
                <p className="text-sm font-medium">{user.name}</p>
                <p className="text-xs text-muted-foreground">{user.email}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}