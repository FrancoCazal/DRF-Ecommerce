import { useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { ShoppingCart, ArrowLeft } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Skeleton } from '@/components/ui/skeleton';
import { useProduct } from '@/hooks/useProducts';
import { useAddToCart } from '@/hooks/useCart';
import { useUser } from '@/hooks/useAuth';
import { formatCurrency } from '@/lib/utils';
import { toast } from 'sonner';

export function ProductDetailPage() {
  const { slug } = useParams<{ slug: string }>();
  const { data: product, isLoading } = useProduct(slug!);
  const { data: user } = useUser();
  const addToCart = useAddToCart();
  const [quantity, setQuantity] = useState(1);

  const handleAddToCart = () => {
    if (!user) {
      toast.error('Please login to add items to cart');
      return;
    }

    if (!product || product.stock === 0) return;

    addToCart.mutate(
      { product_id: product.id, quantity },
      {
        onSuccess: () => {
          toast.success(`${product.name} added to cart`);
          setQuantity(1);
        },
        onError: () => {
          toast.error('Failed to add item to cart');
        },
      }
    );
  };

  if (isLoading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="grid gap-8 lg:grid-cols-2">
          <Skeleton className="aspect-square w-full" />
          <div className="space-y-4">
            <Skeleton className="h-8 w-3/4" />
            <Skeleton className="h-6 w-1/4" />
            <Skeleton className="h-24 w-full" />
            <Skeleton className="h-12 w-full" />
          </div>
        </div>
      </div>
    );
  }

  if (!product) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="text-center">
          <h1 className="mb-4 text-2xl font-bold text-slate-900">Product not found</h1>
          <Link to="/products">
            <Button>Back to Products</Button>
          </Link>
        </div>
      </div>
    );
  }

  const imageUrl = product.image || 'https://images.pexels.com/photos/230544/pexels-photo-230544.jpeg?auto=compress&cs=tinysrgb&w=800';

  return (
    <div className="container mx-auto px-4 py-8">
      <Link to="/products" className="mb-6 inline-flex items-center gap-2 text-sm text-slate-600 hover:text-slate-900">
        <ArrowLeft className="h-4 w-4" />
        Back to Products
      </Link>

      <div className="grid gap-8 lg:grid-cols-2">
        <div className="overflow-hidden rounded-2xl bg-slate-100">
          <img
            src={imageUrl}
            alt={product.name}
            className="h-full w-full object-cover"
          />
        </div>

        <div className="space-y-6">
          <div>
            <h1 className="mb-2 text-4xl font-bold text-slate-900">{product.name}</h1>
            <Link
              to={`/products?category=${product.category.slug}`}
              className="inline-block"
            >
              <Badge variant="secondary">{product.category.name}</Badge>
            </Link>
          </div>

          <div className="text-3xl font-bold text-slate-900">
            {formatCurrency(product.price)}
          </div>

          <div>
            {product.stock > 0 ? (
              <Badge variant="success">In Stock ({product.stock} available)</Badge>
            ) : (
              <Badge variant="destructive">Out of Stock</Badge>
            )}
          </div>

          <div>
            <h2 className="mb-2 text-lg font-semibold text-slate-900">Description</h2>
            <p className="text-slate-700">{product.description}</p>
          </div>

          {product.stock > 0 && (
            <div className="space-y-4">
              <div>
                <Label htmlFor="quantity" className="mb-2 block">
                  Quantity
                </Label>
                <div className="flex items-center gap-2">
                  <Button
                    variant="outline"
                    onClick={() => setQuantity(Math.max(1, quantity - 1))}
                    disabled={quantity <= 1}
                  >
                    -
                  </Button>
                  <Input
                    id="quantity"
                    type="number"
                    value={quantity}
                    onChange={(e) =>
                      setQuantity(Math.max(1, Math.min(product.stock, parseInt(e.target.value) || 1)))
                    }
                    className="w-24 text-center"
                    min="1"
                    max={product.stock}
                  />
                  <Button
                    variant="outline"
                    onClick={() => setQuantity(Math.min(product.stock, quantity + 1))}
                    disabled={quantity >= product.stock}
                  >
                    +
                  </Button>
                </div>
              </div>

              <Button
                size="lg"
                className="w-full gap-2"
                onClick={handleAddToCart}
                disabled={addToCart.isPending}
              >
                <ShoppingCart className="h-5 w-5" />
                Add to Cart
              </Button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
