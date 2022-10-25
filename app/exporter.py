from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from app.models import Invoice, Company


def exporter(invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)
    company = Company.objects.get(id=int(invoice.company))
    # name of the invoice
    name = '{}_{}.pdf'.format(invoice.destination, invoice.id)

    # all items are separated by " ,"
    items_value = []  # values of items
    invoice_item = invoice.item.split(', ')
    invoice_quatity = invoice.quantity.split(', ')
    invoice_unite_price = invoice.unite_price.split(', ')
    invoice_total = 0
    for i in range(int(invoice.field_number)):
        sub_total = int(invoice_quatity[i]) * int(invoice_unite_price[i])
        invoice_total += sub_total

        # field = item, quantity, unite price + unity, sub_total + unity
        field = "{},{},{} {},{} {}".format(str(invoice_item[i]),
                                           invoice_quatity[i],
                                           invoice_unite_price[i],
                                           invoice.unity,
                                           sub_total,
                                           invoice.unity)
        items_value.append(field.split(','))
    total = int(invoice_total - ((invoice_total * invoice.tax) / 100))

    # ____________BUILDING PDF FILE___________
    doc = SimpleDocTemplate(name, pagesize=letter)

    # container for the 'Flowable' objects
    elements = []
    data = [

        # head of the table
        ['Compagnie : {}'.format(company.name), '', '', 'Date : {}'.format(invoice.date)],
        ['Nif Stat        : {}'.format(company.number), '', '', 'Facture n° : {}'.format(invoice.number)],
        ['Addresse    : {}'.format(company.address), '', '', ''],
        [company.mail, '', '', 'à : {}'.format(invoice.destination)],
        ['', '', '', ''],
        ['Objets', 'Quantités', 'Prix Unitaire', 'Total'],

        # items
    ]
    # body of the table
    for i in range(len(items_value)):
        data.append(items_value[i])

    # foot of the table
    data.append(['', '', 'Sous Total', '{} {}'.format(invoice_total, invoice.unity)],)
    data.append(['', '', 'Tax', '{} %'.format(invoice.tax)],)
    data.append(['', '', 'Total', '{} {}'.format(total, invoice.unity)],)

    table = Table(data, 130, 20)
    table.setStyle(
        TableStyle(
            [
                ('BACKGROUND', (0, 5), (3, 5), colors.gray),
                ('BACKGROUND', (-2, -3), (-2, -1), colors.gray),
                ('INNERGRID', (0, 5), (-1, -4), 0.25, colors.black),
                ('BOX', (0, 5), (-1, -4), 0.25, colors.black),
                ('INNERGRID', (-2, -3), (-1, -1), 0.25, colors.black),
                ('BOX', (-2, -3), (-1, -1), 0.25, colors.black),
            ]
        )
    )

    elements.append(table)

    # writting doc
    doc.build(elements)

    return name
