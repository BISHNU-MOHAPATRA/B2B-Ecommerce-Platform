# ----------------------------------------
# Product Base Class
# ----------------------------------------
class Product:

    def __init__(self, product_id, name, base_price, stock_count):
        # Private attributes (Encapsulation)
        self.__product_id = product_id
        self.__name = name

        # Using setters for validation
        self.set_base_price(base_price)
        self.set_stock_count(stock_count)

    # -----------------------------
    # Getter Methods
    # -----------------------------
    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_base_price(self):
        return self.__base_price

    def get_stock_count(self):
        return self.__stock_count

    # -----------------------------
    # Setter Methods with Validation
    # -----------------------------
    def set_base_price(self, price):
        if price < 0:
            raise ValueError("Price cannot be negative")
        self.__base_price = price

    def set_stock_count(self, stock):
        if stock < 0:
            raise ValueError("Stock count cannot be negative")
        self.__stock_count = stock

    # Returns actual product price
    def get_effective_price(self):
        return self.__base_price

    # Updates inventory after order
    def reduce_stock(self, quantity):
        if quantity > self.__stock_count:
            raise ValueError("Insufficient stock available")
        self.__stock_count -= quantity


# ----------------------------------------
# Derived Class : PerishableProduct
# ----------------------------------------
class PerishableProduct(Product):

    def __init__(self, product_id, name, base_price,
                 stock_count, days_to_expiration):

        # Calling parent constructor
        super().__init__(
            product_id,
            name,
            base_price,
            stock_count
        )

        self.days_to_expiration = days_to_expiration

    # Method Overriding
    # Apply 20% discount if product expires in 3 days or less
    def get_effective_price(self):

        if self.days_to_expiration <= 3:
            return self.get_base_price() * 0.80

        return self.get_base_price()


# ----------------------------------------
# Order Processor Class
# ----------------------------------------
class OrderProcessor:

    def process_order(self, order_items, coupon_code=""):

        subtotal = 0

        # --------------------------------
        # Step 1 : Stock Verification
        # --------------------------------
        for product, quantity in order_items:

            if quantity > product.get_stock_count():
                raise ValueError(
                    f"Insufficient stock for {product.get_name()}"
                )

        print("Verification: Inventory validation checks successful.")

        # --------------------------------
        # Step 2 : Price Calculation
        # --------------------------------
        for product, quantity in order_items:

            price = product.get_effective_price()

            line_total = price * quantity

            # Bulk Discount (10%)
            if quantity > 5:
                line_total *= 0.90

            subtotal += line_total

        print(f"Raw Order Basket Subtotal: ${subtotal:.2f}")

        # --------------------------------
        # Step 3 : Coupon Discount
        # --------------------------------
        coupon_discount = 0

        if coupon_code == "SUPERINTELLECT":
            coupon_discount = subtotal * 0.15

            print(
                f'Coupon "{coupon_code}" Applied: '
                f'-${coupon_discount:.2f}'
            )

        # Final Bill Amount
        final_total = subtotal - coupon_discount

        print(
            f"Final Net Processing Invoice Due: "
            f"${final_total:.2f}"
        )

        # --------------------------------
        # Step 4 : Inventory Update
        # --------------------------------
        for product, quantity in order_items:
            product.reduce_stock(quantity)

        # Display remaining inventory
        print("Post-Transaction Inventory Count Update:")

        for product, quantity in order_items:
            print(
                f"{product.get_name()} Remaining: "
                f"{product.get_stock_count()}"
            )


# ----------------------------------------
# Sample Product Catalog
# ----------------------------------------

item1 = Product(
    "P101",
    "Item 1",
    10.0,
    20
)

item2 = PerishableProduct(
    "P102",
    "Item 2",
    50.0,
    10,
    2
)

# ----------------------------------------
# Incoming Order
# ----------------------------------------

order_items = [
    (item1, 6),
    (item2, 2)
]

# ----------------------------------------
# Process Order
# ----------------------------------------

processor = OrderProcessor()

processor.process_order(
    order_items,
    "SUPERINTELLECT"
)