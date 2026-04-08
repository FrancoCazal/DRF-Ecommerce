import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import api from '@/api/client';
import { CartDetail } from '@/lib/types';
import { useUser } from './useAuth';

export function useCart() {
  const { data: user } = useUser();

  return useQuery<CartDetail>({
    queryKey: ['cart'],
    queryFn: async () => {
      const { data } = await api.get('/cart/');
      return data;
    },
    enabled: !!user,
  });
}

export function useAddToCart() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ product_id, quantity }: { product_id: number; quantity: number }) => {
      const { data } = await api.post('/cart/add/', { product_id, quantity });
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['cart'] });
    },
  });
}

export function useUpdateCartItem() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ product_id, quantity }: { product_id: number; quantity: number }) => {
      const { data } = await api.patch(`/cart/update/${product_id}/`, { quantity });
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['cart'] });
    },
  });
}

export function useRemoveCartItem() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (product_id: number) => {
      await api.delete(`/cart/remove/${product_id}/`);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['cart'] });
    },
  });
}

export function useClearCart() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async () => {
      await api.delete('/cart/clear/');
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['cart'] });
    },
  });
}
