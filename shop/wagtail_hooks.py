from wagtail.admin.panels import FieldPanel
from wagtail.admin.ui.tables import UpdatedAtColumn
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from wagtail.admin.panels import TabbedInterface, TitleFieldPanel, ObjectList

from shop.models import Order, Cart, CartItem #, OrderFilterSet

class OrderViewSet(SnippetViewSet):
    model = Order
    icon = "tasks"
    list_display = ["cart_item", "quantity", "price", "date","city","country", "address", UpdatedAtColumn()]
    list_export = ["cart_item", "quantity", "price", "date","city","country", "address"]
    list_per_page = 50
    inspect_view_enabled = True
    admin_url_namespace = "order_views"
    base_url_path = "internal/order"
    # filterset_class = OrderFilterSet

    edit_handler = TabbedInterface([
        ObjectList([FieldPanel("customer")], heading="Details"),
        ObjectList([FieldPanel("quantity")], heading="Preferences"),
    ])

register_snippet(OrderViewSet)
# register_snippet(Order)


class CartItemViewSet(SnippetViewSet):
    model = CartItem
    icon = "user"
    list_display = ["cart", "product", "quantity", UpdatedAtColumn()]
    list_per_page = 50
    inspect_view_enabled = True
    admin_url_namespace = "cartitem_views"
    base_url_path = "internal/cart_item"
    # filterset_class = OrderFilterSet

    edit_handler = TabbedInterface([
        ObjectList([FieldPanel("product")], heading="Details"),
        ObjectList([FieldPanel("quantity")], heading="Preferences"),
    ])

register_snippet(CartItemViewSet)


class CartViewSet(SnippetViewSet):
    model = Cart
    icon = "user"
    list_display = ["user", UpdatedAtColumn()]
    list_per_page = 50
    inspect_view_enabled = True
    admin_url_namespace = "cart_views"
    base_url_path = "internal/cart"
    # filterset_class = OrderFilterSet

    edit_handler = TabbedInterface([
        ObjectList([FieldPanel("user")], heading="Details"),
        # ObjectList([FieldPanel("items")], heading="Preferences"),
    ])

register_snippet(CartViewSet)