from django.urls import path

from .views import (
    taxas_pagamentos,
    editar_pagamento,
    criar_pagamento,
    delete_pagamento,
    criar_contribuinte,
    contribuintes_list,
    edit_contribuinte,
    delete_contribuinte,
    search_pagamentos,
    dashboard,
    grafico_pagamentos_mes
)

app_name = "gupagamentos"

urlpatterns = [
    path("", taxas_pagamentos, name="taxas"),
    path("taxa/", criar_pagamento, name="criar"),
    path("taxa/<int:pk>/", delete_pagamento, name="delete_pagamento"),
    path('taxa/<int:pk>/editar/', editar_pagamento, name='editar_pagamento'),
    path("contribuintes/", contribuintes_list, name="contribuintes"),
    path("criarcontribuinte/", criar_contribuinte, name="criarcont"),
    path("contribuinte/<int:pk>/editar/", edit_contribuinte, name="editar_contribuinte"),
    path("contribuintes/<int:pk>/", delete_contribuinte, name="delete_contribuinte"),
    path("dashboard/", dashboard, name="dashboard"),
    path("dashboard/grafico/", grafico_pagamentos_mes, name="grafico_pagamentos_mes"),
    path("search/", search_pagamentos, name="search_pagamentos"),
]
