BILL_TYPES = (
    ('FIXED','FIXA'),
    ('INSTALLED','PARCELADA'),
    ('UNIQUE_INSTALLMENT','PARCELA ÚNICA'),
)

BILL_STATUSES = (
    ('UNDEFINED','INDEFINIDO'),
    ('TO_EXPIRE','A VENCER'),
    ('EXPIRED','VENCIDA'),
    ('EXPIRES_TODAY','VENCE HOJE'),
    ('WARNING','ATENÇÃO'),
    ('PAID','PAGA'),
)

BILL_ORDERING_OPTIONS = (
    ('-created_date','Criado em - mais recentes'),
    ('created_date','Criado em - mais antigas'),
    ('-expiration_date','Expira em - mais recentes'),
    ('expiration_date','Expira em - mais antigas'),
)

BILL_PAYMENT_BANKS = (
    ('BANCO_DO_BRASIL','BANCO DO BRASIL'),
    ('BRADESCO','BRADESCO'),
    ('CAIXA','CAIXA'),
    ('ITAU','ITAÚ'),
    ('ITI','ITI'),
    ('MERCADO_PAGO','MERCADO PAGO'),
    ('NUBANK','NUBANK'),
    ('OTHER','OUTRO'),
)

BILL_PAYMENT_TYPES = (
    ('MONEY','DINHEIRO'),
    ('DEBIT','DÉBITO'),
    ('CREDIT','CRÉDITO'),
    ('PIX','PIX'),
    ('ONLINE','ONLINE'),
    ('TRANSFER','TRANSFERÊNCIA'),
)
