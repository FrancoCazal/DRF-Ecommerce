# CartPro

Production-ready e-commerce API with Stripe payments, async order processing, and React frontend.

![Python](https://img.shields.io/badge/python-3.12-blue)
![Django](https://img.shields.io/badge/django-5.x-green)
![DRF](https://img.shields.io/badge/DRF-3.14+-blue)
![React](https://img.shields.io/badge/react-18-61DAFB)
![Tests](https://img.shields.io/badge/tests-59%20passed-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-91%25-brightgreen)

---

## Overview

CartPro is a full-stack e-commerce platform built with Django REST Framework (backend) and React (frontend). It features JWT authentication via HttpOnly cookies, a Redis-backed shopping cart, Stripe Checkout integration, and async order processing with Celery.

### Key Features

- **JWT Auth with HttpOnly Cookies** — Secure token storage, refresh rotation, blacklisting
- **Product Catalog** — Filtering, search, pagination, admin CRUD with soft-delete
- **Redis Shopping Cart** — Fast cart operations with 7-day TTL persistence
- **Stripe Checkout** — Hosted payment page, webhook verification, retry payment flow
- **Async Processing** — Celery tasks for order confirmation emails
- **API Documentation** — Auto-generated OpenAPI/Swagger via drf-spectacular

---

## Architecture

```
React SPA (Vite + TypeScript)
    |
    | HTTPS / REST
    v
Django REST Framework
    |
    |--- PostgreSQL
    |       Users, Products, Orders, OrderItems
    |
    |--- Redis
    |       Cart data (per-user hash, TTL 7d)
    |       Celery broker + result backend
    |
    |--- Celery Workers
    |       send_order_confirmation_email
    |
    |--- External Services
            Stripe API (Checkout Sessions + Webhooks)
```

### Checkout Flow

```
1. User adds items to cart (Redis)
2. User fills shipping address → POST /api/v1/orders/
3. Backend: atomic transaction (validate stock → create order → decrement stock → clear cart)
4. Backend: create Stripe Checkout Session → return checkout_url
5. Frontend: redirect to Stripe hosted checkout
6. User pays with card
7. Stripe webhook → backend updates order to PROCESSING → sends confirmation email
```

---

## Tech Stack

### Backend

| Technology | Purpose |
|---|---|
| Django 5.x | Web framework |
| Django REST Framework | API toolkit |
| PostgreSQL | Primary database |
| Redis | Cart storage + Celery broker |
| Celery | Async task processing |
| Stripe | Payment processing |
| SimpleJWT | JWT authentication |
| drf-spectacular | OpenAPI documentation |
| django-filter | Filtering support |
| Pillow | Image handling |

### Frontend

| Technology | Purpose |
|---|---|
| React 18 | UI library |
| TypeScript | Type safety |
| Vite | Build tool |
| TanStack Query | Server state management |
| Zustand | Client state |
| React Router v7 | Routing |
| React Hook Form + Zod | Form validation |
| Tailwind CSS | Styling |
| Axios | HTTP client |

### Infrastructure

| Technology | Purpose |
|---|---|
| Docker + Compose | Local development (6 services) |
| pytest + factory-boy | Testing (59 tests, 91% coverage) |

---

## API Endpoints

```
/api/v1/
├── auth/
│   ├── register/              POST    User registration
│   ├── login/                 POST    JWT login (sets HttpOnly cookies)
│   ├── refresh/               POST    Refresh access token
│   ├── logout/                POST    Blacklist token + clear cookies
│   └── me/                    GET/PATCH  User profile
│
├── categories/                GET     List active categories
│
├── products/
│   ├── /                      GET     List (paginated, filterable, searchable)
│   ├── /{slug}/               GET     Product detail
│   ├── /                      POST    Create (admin only)
│   ├── /{slug}/               PATCH   Update (admin only)
│   └── /{slug}/               DELETE  Soft-delete (admin only)
│
├── cart/
│   ├── /                      GET     Get cart details
│   ├── /add/                  POST    Add item
│   ├── /update/{product_id}/  PATCH   Update quantity
│   ├── /remove/{product_id}/  DELETE  Remove item
│   └── /clear/                DELETE  Clear cart
│
├── orders/
│   ├── /                      GET     List user's orders
│   ├── /                      POST    Create order from cart + Stripe session
│   ├── /{id}/                 GET     Order detail
│   ├── /{id}/cancel/          POST    Cancel pending order (restores stock)
│   ├── /{id}/checkout-session/ POST   Retry payment for pending order
│   └── webhook/stripe/        POST    Stripe webhook handler
│
├── schema/                    GET     OpenAPI schema
└── docs/                      GET     Swagger UI
```

### Filtering & Search (Products)

| Parameter | Example |
|---|---|
| `search` | `?search=headphones` |
| `category` | `?category=electronics` |
| `min_price` | `?min_price=20` |
| `max_price` | `?max_price=100` |
| `ordering` | `?ordering=-price,name` |

---

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Stripe account ([dashboard.stripe.com](https://dashboard.stripe.com)) for payment testing

### Setup

```bash
# Clone the repository
git clone https://github.com/FrancoCazal/DRF-Ecommerce.git
cd DRF-Ecommerce

# Configure environment variables
cp backend/.env.example backend/.env.docker
# Edit backend/.env.docker with your Stripe test keys

# Start all services
docker compose up --build

# In a new terminal: run migrations and seed data
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py seed
```

### Access

| Service | URL |
|---|---|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| Swagger Docs | http://localhost:8000/api/docs/ |
| Flower (Celery) | http://localhost:5555 |

### Demo Accounts (created by seed)

| Role | Email | Password |
|---|---|---|
| Admin | admin@cartpro.com | admin1234 |
| User | demo@cartpro.com | demo1234 |

### Testing Stripe Payments

```bash
# Install Stripe CLI: https://docs.stripe.com/stripe-cli
stripe login
stripe listen --forward-to localhost:8000/api/v1/orders/webhook/stripe/
# Copy the whsec_... secret to your .env as STRIPE_WEBHOOK_SECRET

# Use test card: 4242 4242 4242 4242 (any future expiry, any CVC)
```

---

## Running Tests

```bash
# Local (requires PostgreSQL running)
cd backend
pytest

# Docker
docker compose exec backend pytest
```

**Results:** 59 tests, 91% coverage

| Module | Tests | Coverage |
|---|---|---|
| Users (models + API) | 12 | 68-100% |
| Products (models + API) | 12 | 93-100% |
| Cart (services) | 10 | 99-100% |
| Orders (models + services + API) | 12 | 75-100% |

---

## Project Structure

```
DRF-Ecommerce/
├── backend/
│   ├── apps/
│   │   ├── core/           # Base model, seed command
│   │   ├── users/          # Custom user, JWT auth, middleware
│   │   ├── products/       # Catalog: categories, products
│   │   ├── cart/           # Redis-backed cart service
│   │   └── orders/         # Orders, checkout, Stripe, Celery tasks
│   ├── config/
│   │   ├── settings/       # base, local, production
│   │   ├── urls.py
│   │   └── celery.py
│   ├── conftest.py         # Global test fixtures
│   ├── pytest.ini
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/            # Axios client
│   │   ├── components/     # UI components (shadcn/ui)
│   │   ├── hooks/          # React Query hooks
│   │   ├── lib/            # Types, utils
│   │   └── pages/          # Route pages
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml
└── README.md
```

---

## Design Decisions

### Why HttpOnly Cookies for JWT?

Storing tokens in `localStorage` is vulnerable to XSS attacks. HttpOnly cookies are inaccessible to JavaScript, providing better security. A custom middleware reads the cookie and injects the `Authorization` header so SimpleJWT works transparently.

### Why Redis for Cart?

Cart data is ephemeral and accessed frequently. Redis provides sub-millisecond operations and built-in TTL expiration. Each user's cart is a Redis hash (`cart:user:{id}`) where fields are product IDs and values are quantities.

### Why Stripe Checkout (Hosted) Instead of Elements?

Stripe's hosted checkout page handles all PCI compliance, 3D Secure, and payment methods. No card data touches our server. Simpler to implement and maintain than embedded Elements, with the same security guarantees.

### Why Create Order Before Payment?

Stock is decremented atomically at order creation (inside `transaction.atomic()` with `select_for_update()`). This prevents overselling even under concurrent requests. The order starts as PENDING and transitions to PROCESSING only after Stripe webhook confirms payment.

---

## License

MIT
