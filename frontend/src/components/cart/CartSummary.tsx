import { Link } from 'react-router-dom';
import { Shield, Truck } from 'lucide-react';
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
    if (window.confirm('Clear your entire haul?')) {
      clearCart.mutate(undefined, {
        onSuccess: () => {
          toast.success('Haul cleared');
        },
        onError: () => {
          toast.error('Failed to clear haul');
        },
      });
    }
  };

  return (
    <div>
      <div className="bg-[#1c1c1a] text-[#fcf9f6] p-8 space-y-8 border-2 border-[#1c1c1a]">
        <div className="border-b border-[#fcf9f6]/20 pb-4">
          <h2 className="font-headline font-black text-4xl uppercase tracking-tighter">DAMAGE</h2>
          <p className="text-[10px] tracking-[0.2em] opacity-60 uppercase mt-1">ORDER SUMMARY BREAKDOWN</p>
        </div>

        <div className="space-y-4 font-body uppercase text-sm tracking-tight">
          <div className="flex justify-between items-center">
            <span className="opacity-60 text-xs">RAW SUB ({itemCount} {itemCount === 1 ? 'ITEM' : 'ITEMS'})</span>
            <span className="font-bold">{formatCurrency(total)}</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="opacity-60 text-xs">LOGISTICS</span>
            <span className="font-bold">FREE</span>
          </div>
        </div>

        <div className="pt-6 border-t-2 border-primary">
          <div className="flex justify-between items-end mb-8">
            <span className="font-headline font-bold text-lg">TOTAL</span>
            <span className="font-headline font-black text-5xl tracking-tighter text-primary">
              {formatCurrency(total)}
            </span>
          </div>

          <Link to="/checkout" className="block">
            <button className="w-full bg-primary-container hover:bg-primary text-white font-headline font-black text-xl py-6 border-2 border-primary-container hover:border-on-surface transition-all active:scale-95 uppercase tracking-tighter">
              PROCEED TO CHECKOUT
            </button>
          </Link>

          <div className="mt-6 flex flex-col gap-4">
            <div className="flex items-center gap-3 opacity-60">
              <Shield className="h-4 w-4" />
              <span className="text-[10px] tracking-widest font-bold">SECURE ENCRYPTED NODE</span>
            </div>
            <div className="flex items-center gap-3 opacity-60">
              <Truck className="h-4 w-4" />
              <span className="text-[10px] tracking-widest font-bold">48H DEPLOYMENT</span>
            </div>
          </div>
        </div>
      </div>

      {/* Clear Cart */}
      <button
        onClick={handleClearCart}
        disabled={clearCart.isPending}
        className="mt-4 w-full border-2 border-on-surface py-3 font-headline font-bold text-xs tracking-widest hover:bg-on-surface hover:text-background transition-all uppercase disabled:opacity-50"
      >
        CLEAR HAUL
      </button>
    </div>
  );
}
