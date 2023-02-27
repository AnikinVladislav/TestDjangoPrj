from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>', views.spendigs_view, name='spendings'),
    path('add_spending', views.add_spending, name='add_spending'),
    path('edit_spending/<int:id>', views.editspending, name='edit_spending'),
    path('delete_spending/<int:id>', views.deletespending, name='delete_spending'),
    path('spendings_csv', views.spendingscsv, name='spendingscsv'),
    path('add_category', views.add_category, name='add_category'),
    path('delete_category/<int:id>', views.delete_category, name='delete_category'),
    path('charts_spendings', views.charts_spendings, name='charts_spendings'),
    path('prediction', views.prediction, name='prediction'),
]
