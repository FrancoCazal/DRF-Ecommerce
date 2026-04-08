import { Link } from 'react-router-dom';
import { ShoppingCart } from 'lucide-react';
import { Card, CardContent, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Product } from '@/lib/types';
import { formatCurrency } from '@/lib/utils';
import { useAddToCart } from '@/hooks/useCart';
import { useUser } from '@/hooks/useAuth';
import { toast } from 'sonner';

interface ProductCardProps {
  product: Product;
}

export function ProductCard({ product }: ProductCardProps) {
  const { data: user } = useUser();
  const addToCart = useAddToCart();

  const handleAddToCart = (e: React.MouseEvent) => {
    e.preventDefault();

    if (!user) {
      toast.error('Please login to add items to cart');
      return;
    }

    if (product.stock === 0) return;

    addToCart.mutate(
      { product_id: product.id, quantity: 1 },
      {
        onSuccess: () => {
          toast.success(`${product.name} added to cart`);
        },
        onError: () => {
          toast.error('Failed to add item to cart');
        },
      }
    );
  };

  const imageUrl = product.image || 'https://images.pexels.com/photos/230544/pexels-photo-230544.jpeg?auto=compress&cs=tinysrgb&w=400';

  return (
    <Link to={`/products/${product.slug}`}>
      <Card className="h-full transition-shadow hover:shadow-lg">
        <CardContent className="p-4">
          <div className="aspect-square overflow-hidden rounded-lg bg-slate-100">
            <img
              src={imageUrl}
              alt={product.name}
              className="h-full w-full object-cover"
            />
          </div>
          <div className="mt-4">
            <h3 className="font-semibold text-slate-900">{product.name}</h3>
            <div className="mt-2 flex items-center justify-between">
              <p className="text-lg font-bold text-slate-900">
                {formatCurrency(product.price)}
              </p>
              {product.stock > 0 ? (
                <Badge variant="success" className="text-xs">
                  In Stock
                </Badge>
              ) : (
                <Badge variant="destructive" className="text-xs">
                  Out of Stock
                </Badge>
              )}
            </div>
          </div>
        </CardContent>
        <CardFooter className="p-4 pt-0">
          <Button
            className="w-full"
            onClick={handleAddToCart}
            disabled={product.stock === 0 || addToCart.isPending}
          >
            <ShoppingCart className="mr-2 h-4 w-4" />
            Add to Cart
          </Button>
        </CardFooter>
      </Card>
    </Link>
  );
}
