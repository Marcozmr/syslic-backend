from django.db import migrations, models
from django.db.models import Sum, F

def get_total_items(apps, obj):
    OrderCommitmentItem = apps.get_model('order', 'OrderCommitmentItem')

    total = OrderCommitmentItem.objects.filter(
        commitment=obj.commitment,
        items_delivery__delivery=obj.delivery
    ).aggregate(
        total=Sum(F('quantity') * F('item__price'), output_field=models.FloatField())
    )['total'] or 0.0

    return total

def get_total_nf(apps, obj):
    OrderDeliveryItem = apps.get_model('order', 'OrderDeliveryItem')

    total = OrderDeliveryItem.objects.filter(
            delivery=obj.delivery,
            item__commitment=obj.commitment
    ).aggregate(
        total=Sum(F('quantity') * F('item__item__price'), output_field=models.FloatField())
    )['total'] or 0.0

    return total

def get_liquid_margin(apps, obj):
    OrderDeliveryItem = apps.get_model('order', 'OrderDeliveryItem')
    ContractItem = apps.get_model('contract', 'ContractItem')
    OrderCommitmentItemProduct = apps.get_model('order', 'OrderCommitmentItemProduct')
    OrderDeliveryFreightCotation = apps.get_model('order', 'OrderDeliveryFreightCotation')

    total_invoicing = get_total_nf(apps, obj)

    item_delivery_queryset = OrderDeliveryItem.objects.filter(delivery=obj.delivery)

    total_delivery = 0

    for item_delivery in item_delivery_queryset:
        total_delivery += float(item_delivery.quantity) * float(item_delivery.item.item.price)

    delivery_items_queryset = OrderDeliveryItem.objects.filter(delivery=obj.delivery, item__commitment=obj.commitment)
    delivery_item_first = delivery_items_queryset.first()


    contract_item = ContractItem.objects.filter(contract=delivery_item_first.item.commitment.order.contract).first()

    tax = float(contract_item.tax)/100 * total_invoicing

    fixed_cost = float(contract_item.fixed_cost)/100 * total_invoicing

    item_cost = 0
    item_fob = 0

    for item in delivery_items_queryset:
        unit_cost = 0
        unit_fob = 0

        products = OrderCommitmentItemProduct.objects.filter(item=item.item)
        for item_commitment in products:
            unit_fob += float(item_commitment.fob_freight)
            unit_cost += float(item_commitment.product.quantity) * float(item_commitment.cost)

        item_cost += unit_cost * float(item.quantity)
        item_fob += unit_fob * float(item.quantity)


    freight = 0
    freight_queryset = OrderDeliveryFreightCotation.objects.filter(delivery=obj.delivery, accepted=True)
    if not freight_queryset.exists():
        return None

    delivery_freight = freight_queryset.first()
    freight = float(delivery_freight.cost) * (total_invoicing/total_delivery)
   
    total_margin = ((total_invoicing - (item_cost + item_fob + freight + tax + fixed_cost)) / total_invoicing) * 100

    return total_margin

def populate_invoicing(apps, schema_editor):
    OrderInvoicing = apps.get_model('order', 'OrderInvoicing')

    for invoicing in OrderInvoicing.objects.all():
        invoicing.total_items = get_total_items(apps, invoicing)
        invoicing.total_nf = get_total_nf(apps, invoicing)
        invoicing.liquid_margin = get_liquid_margin(apps, invoicing)
        invoicing.save()

class Migration(migrations.Migration):

    dependencies = [
        ('order', '0058_auto_20240412_2139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalorderinvoicing',
            name='liquid_margin',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='orderinvoicing',
            name='liquid_margin',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=20, null=True),
        ),
        migrations.RunPython(populate_invoicing),
    ]
