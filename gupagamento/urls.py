from django.urls import path

from .views import (
    taxas_pagamentos,
    criar_pagamento,
    criar_contribuinte,
    contribuintes_list,
    search_pagamentos,
)

app_name = "gupagamentos"

urlpatterns = [
    path("", taxas_pagamentos, name="taxas"),
    path("taxa/", criar_pagamento, name="criar"),
    path("contribuintes/", contribuintes_list, name="contribuintes"),
    path("criarcontribuinte/", criar_contribuinte, name="criarcont"),
    path("search/", search_pagamentos, name="search_pagamentos"),
]
