from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from app.forms import CustomerLoginForm, MyPasswordResetForm, MyPasswordChange, MySetPasswordForm
from django.contrib import admin
urlpatterns = [
    path('', views.home, name='home'),
    path('category/<slug:val>', views.Category.as_view(), name='category'),
    path('product_details/<str:pk>',
         views.ProductDetail.as_view(), name='product_details'),
    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('showcart', views.showcart, name='showcart'),
    path('checkout', views.Checkout.as_view(), name='checkout'),
    path('wishlist', views.wishlist, name='wishlist'),
    path('paymentdone', views.paymentdone, name='paymentdone'),
    path('orders', views.orders, name='orders'),

    path('about', views.about, name='about'),

    path('plus_cart', views.plus_cart),
    path('minus_cart', views.minus_cart),
    path('remove_cart', views.remove_cart),


    path('plus_wishlist', views.plus_wishlist),
    path('minus_wishlist', views.minus_wishlist),

    path('profile', views.Profile.as_view(), name='profile'),
    path('address', views.address, name='address'),
    path('updateAddress/<int:pk>',
         views.updateAddress.as_view(), name='updateAddress'),

    path('registration', views.CustomerRegistrationView.as_view(), name='registration'),
    path('accounts/login/', auth_view.LoginView.as_view(template_name='login.html',
         authentication_form=CustomerLoginForm), name='login'),
    path('password_change', auth_view.PasswordChangeView.as_view(
         template_name='password_change.html',
         form_class=MyPasswordChange, success_url='password_change_done'), name='password_change'),
    path('password_change_done', auth_view.PasswordChangeDoneView.as_view(
         template_name='password_change_done.html'), name='password_change_done'),
    path('logout', auth_view.LogoutView.as_view(
        next_page='login'), name='logout'),


    path('password_reset', auth_view.PasswordResetView.as_view(
        template_name='password_reset.html',
        form_class=MyPasswordResetForm), name='password_reset'),
    path('password_reset/done', auth_view.PasswordResetDoneView.as_view(
         template_name='password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(
         template_name='password_reset_confirm.html',
         form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password_reset_complete', auth_view.PasswordResetCompleteView.as_view(
         template_name='password_reset_complete.html'),
         name='password_reset_complete'),
    path('search', views.search, name='search'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Suryam Dairy Login'
admin.site.site_title = 'Suryam Dairy'
admin.site.site_index_title = 'Suryam Dairy'
