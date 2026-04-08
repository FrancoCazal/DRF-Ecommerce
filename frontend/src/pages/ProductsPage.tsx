import { useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Search } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { ProductGrid } from '@/components/products/ProductGrid';
import { ProductFilters } from '@/components/products/ProductFilters';
import { useProducts } from '@/hooks/useProducts';

export function ProductsPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [searchInput, setSearchInput] = useState(searchParams.get('search') || '');

  const filters = {
    search: searchParams.get('search') || undefined,
    category: searchParams.get('category') || undefined,
    min_price: searchParams.get('min_price') ? parseFloat(searchParams.get('min_price')!) : undefined,
    max_price: searchParams.get('max_price') ? parseFloat(searchParams.get('max_price')!) : undefined,
    page: searchParams.get('page') ? parseInt(searchParams.get('page')!) : 1,
  };

  const { data, isLoading } = useProducts(filters);

  const handleFilterChange = (newFilters: { category?: string; min_price?: number; max_price?: number }) => {
    const params = new URLSearchParams(searchParams);

    if (newFilters.category) {
      params.set('category', newFilters.category);
    } else {
      params.delete('category');
    }

    if (newFilters.min_price) {
      params.set('min_price', newFilters.min_price.toString());
    } else {
      params.delete('min_price');
    }

    if (newFilters.max_price) {
      params.set('max_price', newFilters.max_price.toString());
    } else {
      params.delete('max_price');
    }

    params.delete('page');
    setSearchParams(params);
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    const params = new URLSearchParams(searchParams);

    if (searchInput) {
      params.set('search', searchInput);
    } else {
      params.delete('search');
    }

    params.delete('page');
    setSearchParams(params);
  };

  const handlePageChange = (newPage: number) => {
    const params = new URLSearchParams(searchParams);
    params.set('page', newPage.toString());
    setSearchParams(params);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const totalPages = data ? Math.ceil(data.count / 20) : 1;

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="mb-8 text-4xl font-bold text-slate-900">Products</h1>

      <div className="grid gap-8 lg:grid-cols-[300px_1fr]">
        <aside>
          <ProductFilters
            filters={filters}
            onFilterChange={handleFilterChange}
          />
        </aside>

        <main>
          <form onSubmit={handleSearch} className="mb-6">
            <div className="flex gap-2">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
                <Input
                  type="text"
                  placeholder="Search products..."
                  value={searchInput}
                  onChange={(e) => setSearchInput(e.target.value)}
                  className="pl-10"
                />
              </div>
              <Button type="submit">Search</Button>
            </div>
          </form>

          {data && (
            <div className="mb-4 text-sm text-slate-600">
              Showing {data.results.length} of {data.count} products
            </div>
          )}

          <ProductGrid products={data?.results || []} isLoading={isLoading} />

          {data && totalPages > 1 && (
            <div className="mt-8 flex justify-center gap-2">
              <Button
                variant="outline"
                onClick={() => handlePageChange(filters.page - 1)}
                disabled={filters.page === 1}
              >
                Previous
              </Button>

              <div className="flex items-center gap-2">
                {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                  let pageNum: number;
                  if (totalPages <= 5) {
                    pageNum = i + 1;
                  } else if (filters.page <= 3) {
                    pageNum = i + 1;
                  } else if (filters.page >= totalPages - 2) {
                    pageNum = totalPages - 4 + i;
                  } else {
                    pageNum = filters.page - 2 + i;
                  }

                  return (
                    <Button
                      key={pageNum}
                      variant={filters.page === pageNum ? 'default' : 'outline'}
                      onClick={() => handlePageChange(pageNum)}
                    >
                      {pageNum}
                    </Button>
                  );
                })}
              </div>

              <Button
                variant="outline"
                onClick={() => handlePageChange(filters.page + 1)}
                disabled={filters.page === totalPages}
              >
                Next
              </Button>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
