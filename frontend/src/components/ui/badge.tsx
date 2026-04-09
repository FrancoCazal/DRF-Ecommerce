import * as React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const badgeVariants = cva(
  'inline-flex items-center border px-2.5 py-0.5 text-xs font-bold uppercase font-headline tracking-wider transition-colors focus:outline-none focus:ring-2 focus:ring-on-surface focus:ring-offset-2',
  {
    variants: {
      variant: {
        default:
          'border-transparent bg-on-surface text-surface',
        secondary:
          'border-transparent bg-surface-container-high text-on-surface',
        destructive:
          'border-transparent bg-primary text-on-primary',
        outline: 'text-on-surface border-on-surface',
        success: 'border-transparent bg-green-700 text-white',
        warning: 'border-transparent bg-amber-600 text-white',
        info: 'border-transparent bg-blue-700 text-white',
      },
    },
    defaultVariants: {
      variant: 'default',
    },
  }
);

export interface BadgeProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> {}

function Badge({ className, variant, ...props }: BadgeProps) {
  return (
    <div className={cn(badgeVariants({ variant }), className)} {...props} />
  );
}

export { Badge, badgeVariants };
