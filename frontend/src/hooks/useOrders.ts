import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import api from '@/api/client';
import { OrderListItem, OrderDetail, CreateOrderResponse, PaginatedResponse } from '@/lib/types';

interface CreateOrderData {
  shipping_address?: string;
  notes?: string;
}

export function useOrders(page: number = 1) {
  return useQuery<PaginatedResponse<OrderListItem>>({
    queryKey: ['orders', page],
    queryFn: async () => {
      const { data } = await api.get(`/orders/?page=${page}`);
      return data;
    },
  });
}

export function useOrder(id: number) {
  return useQuery<OrderDetail>({
    queryKey: ['order', id],
    queryFn: async () => {
      const { data } = await api.get(`/orders/${id}/`);
      return data;
    },
    enabled: !!id,
  });
}

export function useCreateOrder() {
  const queryClient = useQueryClient();

  return useMutation<CreateOrderResponse, Error, CreateOrderData>({
    mutationFn: async (orderData: CreateOrderData) => {
      const { data } = await api.post('/orders/', orderData);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['cart'] });
      queryClient.invalidateQueries({ queryKey: ['orders'] });
    },
  });
}

export function useCreateCheckoutSession() {
  return useMutation<{ checkout_url: string }, Error, number>({
    mutationFn: async (orderId: number) => {
      const { data } = await api.post(`/orders/${orderId}/checkout-session/`);
      return data;
    },
  });
}

export function useCancelOrder() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (id: number) => {
      const { data } = await api.post(`/orders/${id}/cancel/`);
      return data;
    },
    onSuccess: (_, id) => {
      queryClient.invalidateQueries({ queryKey: ['orders'] });
      queryClient.invalidateQueries({ queryKey: ['order', id] });
    },
  });
}
