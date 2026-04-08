from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from apps.users.models import User
from apps.products.models import Category, Product

CATEGORIES = {
    'Electronics': [
        {
            'name': 'Wireless Noise-Cancelling Headphones',
            'description': 'Premium over-ear headphones with active noise cancellation, 30-hour battery life, and Hi-Res Audio support. Foldable design with memory foam ear cushions for all-day comfort.',
            'price': Decimal('149.99'),
            'stock': 45,
        },
        {
            'name': 'Mechanical Gaming Keyboard',
            'description': 'RGB backlit mechanical keyboard with Cherry MX Brown switches. Full N-key rollover, detachable USB-C cable, and aircraft-grade aluminum frame.',
            'price': Decimal('89.99'),
            'stock': 30,
        },
        {
            'name': '4K Webcam with Ring Light',
            'description': 'Ultra HD webcam with built-in adjustable ring light, auto-focus, and dual noise-cancelling microphones. Perfect for streaming and video calls.',
            'price': Decimal('79.99'),
            'stock': 60,
        },
        {
            'name': 'Portable Bluetooth Speaker',
            'description': 'Waterproof IPX7 portable speaker with 360-degree sound, 20-hour playtime, and built-in power bank. Pairs with up to 3 devices simultaneously.',
            'price': Decimal('59.99'),
            'stock': 80,
        },
        {
            'name': 'USB-C Fast Charging Hub',
            'description': '7-in-1 USB-C hub with 100W power delivery, 4K HDMI output, SD card reader, and 3 USB 3.0 ports. Compatible with all USB-C laptops and tablets.',
            'price': Decimal('45.99'),
            'stock': 100,
        },
    ],
    'Clothing': [
        {
            'name': 'Classic Fit Cotton T-Shirt',
            'description': '100% organic cotton crew neck t-shirt. Pre-shrunk, breathable fabric with reinforced stitching. Available in multiple colors.',
            'price': Decimal('24.99'),
            'stock': 200,
        },
        {
            'name': 'Slim Fit Stretch Jeans',
            'description': 'Modern slim fit jeans with 2% elastane for comfortable stretch. Dark indigo wash, 5-pocket design, and durable YKK zipper.',
            'price': Decimal('59.99'),
            'stock': 120,
        },
        {
            'name': 'Lightweight Puffer Jacket',
            'description': 'Water-resistant puffer jacket with synthetic down insulation. Packable into its own pocket, weighs under 400g. Ideal for layering.',
            'price': Decimal('89.99'),
            'stock': 75,
        },
        {
            'name': 'Running Sneakers Pro',
            'description': 'Engineered mesh upper with responsive foam midsole for maximum energy return. Rubber outsole with multi-directional traction pattern.',
            'price': Decimal('119.99'),
            'stock': 90,
        },
        {
            'name': 'Merino Wool Crew Socks (3-Pack)',
            'description': 'Temperature-regulating merino wool blend socks with arch support and reinforced heel and toe. Naturally odor-resistant.',
            'price': Decimal('29.99'),
            'stock': 300,
        },
    ],
    'Home & Kitchen': [
        {
            'name': 'Programmable Drip Coffee Maker',
            'description': '12-cup coffee maker with programmable timer, adjustable brew strength, and auto-shutoff. Includes reusable mesh filter and thermal carafe.',
            'price': Decimal('69.99'),
            'stock': 40,
        },
        {
            'name': 'Cast Iron Skillet 12-Inch',
            'description': 'Pre-seasoned cast iron skillet with helper handle. Oven safe up to 500F, compatible with all cooktops including induction. Lifetime warranty.',
            'price': Decimal('34.99'),
            'stock': 55,
        },
        {
            'name': 'Adjustable LED Desk Lamp',
            'description': 'Eye-caring LED desk lamp with 5 color modes and 7 brightness levels. USB charging port, 1-hour auto timer, and flexible gooseneck.',
            'price': Decimal('39.99'),
            'stock': 70,
        },
        {
            'name': 'Bamboo Drawer Organizer Set',
            'description': 'Expandable bamboo organizer with 8 compartments. Fits standard kitchen drawers. Natural antimicrobial properties and water-resistant finish.',
            'price': Decimal('22.99'),
            'stock': 110,
        },
        {
            'name': 'Stainless Steel Water Bottle',
            'description': 'Double-wall vacuum insulated bottle keeps drinks cold 24h or hot 12h. BPA-free, leak-proof lid, and wide mouth for easy cleaning. 750ml capacity.',
            'price': Decimal('27.99'),
            'stock': 150,
        },
    ],
    'Books': [
        {
            'name': 'Clean Code: A Handbook of Agile Software Craftsmanship',
            'description': 'Robert C. Martin\'s classic guide to writing readable, maintainable code. Covers naming conventions, functions, error handling, and testing with real-world examples.',
            'price': Decimal('39.99'),
            'stock': 85,
        },
        {
            'name': 'Designing Data-Intensive Applications',
            'description': 'Martin Kleppmann\'s deep dive into the principles behind reliable, scalable, and maintainable systems. Covers databases, stream processing, and distributed systems.',
            'price': Decimal('44.99'),
            'stock': 60,
        },
        {
            'name': 'The Pragmatic Programmer (20th Anniversary Edition)',
            'description': 'Updated edition of the timeless classic. Practical advice on software craftsmanship, from personal responsibility to architectural techniques.',
            'price': Decimal('42.99'),
            'stock': 70,
        },
        {
            'name': 'Atomic Habits',
            'description': 'James Clear\'s proven framework for building good habits and breaking bad ones. Backed by scientific research and real-world examples.',
            'price': Decimal('16.99'),
            'stock': 200,
        },
    ],
    'Sports & Outdoors': [
        {
            'name': 'Non-Slip Yoga Mat 6mm',
            'description': 'Extra thick TPE yoga mat with dual-layer non-slip texture. Eco-friendly, lightweight, and includes carrying strap. 183cm x 61cm.',
            'price': Decimal('32.99'),
            'stock': 95,
        },
        {
            'name': 'Adjustable Dumbbell Set (2-20kg)',
            'description': 'Space-saving adjustable dumbbells with quick-lock mechanism. Replace 10 pairs of dumbbells. Ergonomic grip with anti-roll design.',
            'price': Decimal('189.99'),
            'stock': 25,
        },
        {
            'name': 'Resistance Bands Set (5 Levels)',
            'description': 'Natural latex resistance bands with door anchor, handles, and ankle straps. 5 resistance levels from 5 to 50 lbs. Includes carrying bag.',
            'price': Decimal('24.99'),
            'stock': 140,
        },
        {
            'name': 'Insulated Hiking Backpack 30L',
            'description': 'Lightweight hiking backpack with hydration bladder compartment, rain cover, and ventilated back panel. Multiple pockets and compression straps.',
            'price': Decimal('64.99'),
            'stock': 50,
        },
        {
            'name': 'Digital Jump Rope with Counter',
            'description': 'Weighted jump rope with LCD display showing calories, timer, and jump count. Adjustable length, ball-bearing handles for smooth rotation.',
            'price': Decimal('19.99'),
            'stock': 180,
        },
    ],
}

DEMO_USER = {
    'email': 'demo@cartpro.com',
    'first_name': 'Demo',
    'last_name': 'User',
    'password': 'demo1234',
}

ADMIN_USER = {
    'email': 'admin@cartpro.com',
    'first_name': 'Admin',
    'last_name': 'CartPro',
    'password': 'admin1234',
}


class Command(BaseCommand):
    help = 'Seed database with demo data for CartPro'

    def add_arguments(self, parser):
        parser.add_argument(
            '--flush',
            action='store_true',
            help='Delete existing products and categories before seeding',
        )

    def handle(self, *args, **options):
        if options['flush']:
            self.stdout.write('Flushing existing products and categories...')
            Product.objects.all().delete()
            Category.objects.all().delete()

        # Create users
        admin, created = User.objects.get_or_create(
            email=ADMIN_USER['email'],
            defaults={
                'first_name': ADMIN_USER['first_name'],
                'last_name': ADMIN_USER['last_name'],
                'is_staff': True,
                'is_superuser': True,
            },
        )
        if created:
            admin.set_password(ADMIN_USER['password'])
            admin.save()
            self.stdout.write(self.style.SUCCESS(
                f'  Admin created: {ADMIN_USER["email"]} / {ADMIN_USER["password"]}'
            ))
        else:
            self.stdout.write(f'  Admin already exists: {admin.email}')

        demo, created = User.objects.get_or_create(
            email=DEMO_USER['email'],
            defaults={
                'first_name': DEMO_USER['first_name'],
                'last_name': DEMO_USER['last_name'],
            },
        )
        if created:
            demo.set_password(DEMO_USER['password'])
            demo.save()
            self.stdout.write(self.style.SUCCESS(
                f'  Demo user created: {DEMO_USER["email"]} / {DEMO_USER["password"]}'
            ))
        else:
            self.stdout.write(f'  Demo user already exists: {demo.email}')

        # Create categories and products
        total_products = 0
        for category_name, products in CATEGORIES.items():
            slug = slugify(category_name)
            category, created = Category.objects.get_or_create(
                slug=slug,
                defaults={'name': category_name},
            )
            action = 'Created' if created else 'Exists'
            self.stdout.write(f'  {action} category: {category_name}')

            for product_data in products:
                product_slug = slugify(product_data['name'])
                _, created = Product.objects.get_or_create(
                    slug=product_slug,
                    defaults={
                        'name': product_data['name'],
                        'description': product_data['description'],
                        'price': product_data['price'],
                        'stock': product_data['stock'],
                        'category': category,
                    },
                )
                if created:
                    total_products += 1

        self.stdout.write(self.style.SUCCESS(
            f'\nDone! Created {total_products} products across '
            f'{len(CATEGORIES)} categories.'
        ))
        self.stdout.write(self.style.SUCCESS(
            '\nDemo accounts:'
            f'\n  Admin: {ADMIN_USER["email"]} / {ADMIN_USER["password"]}'
            f'\n  User:  {DEMO_USER["email"]} / {DEMO_USER["password"]}'
        ))
