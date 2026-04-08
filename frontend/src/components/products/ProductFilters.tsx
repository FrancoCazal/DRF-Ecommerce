import { useCategories } from '@/hooks/useProducts';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';

interface ProductFiltersProps {
  filters: {
    category?: string;
    min_price?: number;
    max_price?: number;
  };
  onFilterChange: (filters: { category?: string; min_price?: number; max_price?: number }) => void;
}

export function ProductFilters({ filters, onFilterChange }: ProductFiltersProps) {
  const { data: categories, isLoading } = useCategories();

  const handleCategoryChange = (slug: string) => {
    const newCategory = filters.category === slug ? undefined : slug;
    onFilterChange({ ...filters, category: newCategory });
  };

  const handlePriceChange = (field: 'min_price' | 'max_price', value: string) => {
    const numValue = value ? parseFloat(value) : undefined;
    onFilterChange({ ...filters, [field]: numValue });
  };

  const handleClearFilters = () => {
    onFilterChange({});
  };

  const hasFilters = filters.category || filters.min_price || filters.max_price;

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-lg">Filters</CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        <div>
          <Label className="mb-3 block text-sm font-semibold">Categories</Label>
          {isLoading ? (
            <div className="space-y-2">
              {Array.from({ length: 4 }).map((_, i) => (
                <Skeleton key={i} className="h-6 w-full" />
              ))}
            </div>
          ) : (
            <div className="space-y-2">
              {categories?.map((category) => (
                <label key={category.id} className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    checked={filters.category === category.slug}
                    onChange={() => handleCategoryChange(category.slug)}
                    className="h-4 w-4 rounded border-slate-300 text-slate-900 focus:ring-2 focus:ring-slate-950"
                  />
                  <span className="text-sm text-slate-700">{category.name}</span>
                </label>
              ))}
            </div>
          )}
        </div>

        <div>
          <Label className="mb-3 block text-sm font-semibold">Price Range</Label>
          <div className="space-y-3">
            <div>
              <Label htmlFor="min-price" className="mb-1 block text-xs text-slate-600">
                Min Price
              </Label>
              <Input
                id="min-price"
                type="number"
                placeholder="0"
                value={filters.min_price || ''}
                onChange={(e) => handlePriceChange('min_price', e.target.value)}
                min="0"
                step="1"
              />
            </div>
            <div>
              <Label htmlFor="max-price" className="mb-1 block text-xs text-slate-600">
                Max Price
              </Label>
              <Input
                id="max-price"
                type="number"
                placeholder="1000"
                value={filters.max_price || ''}
                onChange={(e) => handlePriceChange('max_price', e.target.value)}
                min="0"
                step="1"
              />
            </div>
          </div>
        </div>

        {hasFilters && (
          <Button variant="outline" className="w-full" onClick={handleClearFilters}>
            Clear Filters
          </Button>
        )}
      </CardContent>
    </Card>
  );
}
