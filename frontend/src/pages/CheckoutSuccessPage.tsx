import { Link } from 'react-router-dom';
import { CheckCircle, Package, ArrowRight } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

export function CheckoutSuccessPage() {
  return (
    <div className="container mx-auto px-4 py-16">
      <div className="mx-auto max-w-md text-center">
        <Card>
          <CardContent className="pt-8 pb-8 space-y-6">
            <div className="flex justify-center">
              <CheckCircle className="h-16 w-16 text-green-500" />
            </div>

            <div>
              <h1 className="mb-2 text-2xl font-bold text-on-surface">
                Payment Successful!
              </h1>
              <p className="text-secondary">
                Your order has been confirmed and is now being processed.
                You will receive a confirmation email shortly.
              </p>
            </div>

            <div className="flex flex-col gap-3">
              <Link to="/orders">
                <Button className="w-full gap-2">
                  <Package className="h-4 w-4" />
                  View My Orders
                </Button>
              </Link>
              <Link to="/products">
                <Button variant="outline" className="w-full gap-2">
                  Continue Shopping
                  <ArrowRight className="h-4 w-4" />
                </Button>
              </Link>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
