BILL_TYPES = (
    ('INSTALLED','Parcelada'),
    ('UNIQUE_INSTALLMENT','Parcela única'),
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
    ('BANCO_DO_BRASIL','Banco do Brasil'),
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
