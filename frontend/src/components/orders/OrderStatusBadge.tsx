import { Badge } from '@/components/ui/badge';

interface OrderStatusBadgeProps {
  status: string;
}

export function OrderStatusBadge({ status }: OrderStatusBadgeProps) {
  const variants: Record<string, 'warning' | 'info' | 'default' | 'success' | 'destructive'> = {
    pending: 'warning',
    processing: 'info',
    shipped: 'default',
    delivered: 'success',
    cancelled: 'destructive',
  };

  const variant = variants[status] || 'default';

  return (
    <Badge variant={variant} className="capitalize">
      {status}
    </Badge>
  );
}
