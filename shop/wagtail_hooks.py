from wagtail.admin.panels import FieldPanel
from wagtail.admin.ui.tables import UpdatedAtColumn
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from wagtail.admin.panels import TabbedInterface, TitleFieldPanel, ObjectList

from shop.models import Order, Cart, CartItem #, OrderFilterSet
from wagtail import hooks
from .views import order_viewset


class OrderViewSet(SnippetViewSet):
    model = Order
    icon = "tasks"
    list_display = ["cart", "quantity", "price", "date","city","country", "address", UpdatedAtColumn()]
    list_export = ["cart", "quantity", "price", "date","city","country", "address"]
    list_per_page = 50
    inspect_view_enabled = True
    admin_url_namespace = "order_views"
    base_url_path = "internal/order"
    # filterset_class = OrderFilterSet

    edit_handler = TabbedInterface([
        ObjectList([FieldPanel("customer"),FieldPanel("quantity")], heading="Details"),
        # ObjectList([FieldPanel("quantity")], heading="Preferences"),
    ])

register_snippet(OrderViewSet)
# register_snippet(Order)

@hooks.register("register_admin_viewset")
def register_viewset():
    return order_viewset


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
        ObjectList([FieldPanel("product"),FieldPanel("quantity")], heading="Details"),
        # ObjectList([FieldPanel("quantity")], heading="Preferences"),
    ])

register_snippet(CartItemViewSet)


class CartViewSet(SnippetViewSet):
    model = Cart
    icon = "user"
    list_display = ["user","created_at", UpdatedAtColumn()]
    list_per_page = 50
    inspect_view_enabled = True
    admin_url_namespace = "cart_views"
    base_url_path = "internal/cart"
    # filterset_class = OrderFilterSet

    edit_handler = TabbedInterface([
        ObjectList([FieldPanel("user"), FieldPanel("items")], heading="Details"),
        # ObjectList([FieldPanel("items")], heading="Details"),
    ])

register_snippet(CartViewSet)