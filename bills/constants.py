BILL_TYPES = (
    ('INSTALLED','Parcelada'),
    ('UNIQUE_INSTALLMENT','Parcela Única'),
)

BILL_STATUSES = (
    ('UNDEFINED','Indefinido'),
    ('TO_EXPIRE','A Vencer'),
    ('EXPIRED','Vencida'),
    ('EXPIRES_TODAY','Vence Hoje'),
    ('WARNING','Atenção'),
    ('PAID','Paga'),
)

BILL_ORDERING_OPTIONS = (
    ('-created_date','Criado em - mais recentes'),
    ('created_date','Criado em - mais antigas'),
    ('-expiration_date','Expira em - mais recentes'),
    ('expiration_date','Expira em - mais antigas'),
)

BILL_PAYMENT_BANKS = (
    ('BANCO_DO_BRASIL','Banco do Brasil'),
    ('BANCO_CORA','Banco Cora'),
    ('BRADESCO','Bradesco'),
    ('CAIXA','Caixa'),
    ('ITAU','Itaú'),
    ('ITI','Iti'),
    ('MERCADO_PAGO','Mercado Pago'),
    ('NUBANK','Nubank'),
    ('PAG_SEGURO','Pag Seguro'),
    ('PAY_PAL','Pay Pal'),
    ('PIC_PAY','Pic Pay'),
    ('SANTANDER','Santander'),
    ('OTHER','Outro'),
)

BILL_PAYMENT_TYPES = (
    ('MONEY','Dinheiro'),
    ('DEBIT','Débito'),
    ('CREDIT','Crédito'),
    ('PIX','Pix'),
    ('ONLINE','Online'),
    ('TRANSFER','Transferência'),
)
