import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';
import { formatCurrency } from '@/lib/utils';
import { useClearCart } from '@/hooks/useCart';
import { toast } from 'sonner';

interface CartSummaryProps {
  total: string;
  itemCount: number;
}

export function CartSummary({ total, itemCount }: CartSummaryProps) {
  const clearCart = useClearCart();

  const handleClearCart = () => {
    if (window.confirm('Are you sure you want to clear your cart?')) {
      clearCart.mutate(undefined, {
        onSuccess: () => {
          toast.success('Cart cleared');
        },
        onError: () => {
          toast.error('Failed to clear cart');
        },
      });
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Order Summary</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex justify-between text-sm">
          <span className="text-slate-600">Items</span>
          <span className="font-medium text-slate-900">{itemCount}</span>
        </div>
        <Separator />
        <div className="flex justify-between">
          <span className="font-semibold text-slate-900">Total</span>
          <span className="text-xl font-bold text-slate-900">{formatCurrency(total)}</span>
        </div>
      </CardContent>
      <CardFooter className="flex flex-col gap-2">
        <Link to="/checkout" className="w-full">
          <Button className="w-full" size="lg">
            Proceed to Checkout
          </Button>
        </Link>
        <Button
          variant="outline"
          className="w-full"
          onClick={handleClearCart}
          disabled={clearCart.isPending}
        >
          Clear Cart
        </Button>
      </CardFooter>
    </Card>
  );
}
