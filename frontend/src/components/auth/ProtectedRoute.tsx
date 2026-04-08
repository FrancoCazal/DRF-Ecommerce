import { Navigate, useLocation } from 'react-router-dom';
import { useUser } from '@/hooks/useAuth';
import { Skeleton } from '@/components/ui/skeleton';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

export function ProtectedRoute({ children }: ProtectedRouteProps) {
  const { data: user, isLoading, isError } = useUser();
  const location = useLocation();

  if (isLoading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="space-y-4">
          <Skeleton className="h-8 w-64" />
          <Skeleton className="h-64 w-full" />
        </div>
      </div>
    );
  }

  if (isError || !user) {
    return <Navigate to="/login" state={{ returnUrl: location.pathname + location.search }} replace />;
  }

  return <>{children}</>;
}
