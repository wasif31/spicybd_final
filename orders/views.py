from django.shortcuts import render
from django.http import Http404
from django.views.generic import ListView, DetailView
from .models import Order
from billing.models import BillingProfile
from django.contrib.auth.mixins import LoginRequiredMixin


class OrderListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        my_profile = BillingProfile.objects.new_or_get(self.request)
        return Order.objects.by_request(self.request)


class OrderDetailView(LoginRequiredMixin, DetailView):
    def get_object(self):

        qs = Order.objects.by_request(self.request).filter(
            order_id=self.kwargs.get('order_id'))
        if qs.count() == 1:
            return qs.first()

        raise Http404
        # return Order.objects.get(id=self.kwargs.get('id'))
