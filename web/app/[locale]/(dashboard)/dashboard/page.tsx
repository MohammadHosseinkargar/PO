'use client';

import { useTranslations } from 'next-intl';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import {
  BarChart,
  LineChart,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  Bar,
  Line,
  ResponsiveContainer,
} from 'recharts';

const mockData = {
  totalStock: 1234,
  activeSKUs: 567,
  stockValue: 123456.78,
  lowStockAlerts: 12,
  recentSales: [
    { date: '2023-11-01', amount: 5200 },
    { date: '2023-11-02', amount: 4800 },
    { date: '2023-11-03', amount: 6100 },
    { date: '2023-11-04', amount: 5400 },
    { date: '2023-11-05', amount: 5900 },
  ],
  topProducts: [
    { name: 'T-Shirt', sales: 120 },
    { name: 'Jeans', sales: 95 },
    { name: 'Hoodie', sales: 85 },
    { name: 'Jacket', sales: 75 },
    { name: 'Sneakers', sales: 70 },
  ],
};

export default function DashboardPage() {
  const t = useTranslations();

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">{t('nav.dashboard')}</h1>

      {/* KPI Cards */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader>
            <CardTitle>{t('dashboard.totalStock')}</CardTitle>
            <CardDescription>{t('dashboard.totalStockDesc')}</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-bold">{mockData.totalStock}</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>{t('dashboard.activeSKUs')}</CardTitle>
            <CardDescription>{t('dashboard.activeSKUsDesc')}</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-bold">{mockData.activeSKUs}</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>{t('dashboard.stockValue')}</CardTitle>
            <CardDescription>{t('dashboard.stockValueDesc')}</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-bold">
              ${mockData.stockValue.toLocaleString()}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>{t('dashboard.lowStockAlerts')}</CardTitle>
            <CardDescription>{t('dashboard.lowStockAlertsDesc')}</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-bold">{mockData.lowStockAlerts}</p>
          </CardContent>
        </Card>
      </div>

      {/* Charts */}
      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>{t('dashboard.recentSales')}</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-[300px]">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={mockData.recentSales}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line
                    type="monotone"
                    dataKey="amount"
                    name={t('dashboard.sales')}
                    stroke="#2563eb"
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>{t('dashboard.topProducts')}</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-[300px]">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={mockData.topProducts}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar
                    dataKey="sales"
                    name={t('dashboard.unitsSold')}
                    fill="#2563eb"
                  />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}