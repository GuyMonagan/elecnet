from django.contrib import admin
from django.utils.html import format_html

from .models import BusinessUnit, Product


@admin.action(description="Очистить задолженность перед поставщиком")
def clear_debt(modeladmin, request, queryset):
    """
    Admin action to reset debt_to_supplier for selected business units.
    """
    queryset.update(debt_to_supplier=0)


@admin.register(BusinessUnit)
class BusinessUnitAdmin(admin.ModelAdmin):
    """
    Admin configuration for BusinessUnit model.
    """
    list_display = ("name", "city", "supplier_link", "debt_to_supplier", "get_level")
    list_filter = ("city",)
    actions = [clear_debt]

    def supplier_link(self, obj):
        if obj.supplier:
            return format_html(
                '<a href="/admin/network/businessunit/{}/change/">{}</a>',
                obj.supplier.id,
                obj.supplier.name,
            )
        return "-"

    supplier_link.short_description = "Поставщик"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin configuration for Product model.
    """
    list_display = ("name", "model", "release_date", "owner")
    search_fields = ("name", "model")
    list_filter = ("release_date",)
