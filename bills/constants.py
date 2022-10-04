BILL_TYPES = (
    ('FIXED','FIXA'),
    ('INSTALLED','PARCELADA'),
    ('UNIQUE_INSTALLMENT','PARCELA ÚNICA')
)

BILL_STATUSES = (
    ('UNDEFINED','INDEFINIDO'),
    ('TO_EXPIRE','A VENCER'),
    ('EXPIRED','EXPIRADA'),
    ('WARNING','ATENÇÃO'),
    ('PAID','PAGA')
)

BILL_ORDERING_OPTIONS = (
    ('-created_date','Criado em - mais recentes'),
    ('created_date','Criado em - mais antigas'),
    ('-expiration_date','Expira em - mais recentes'),
    ('expiration_date','Expira em - mais antigas'),
)