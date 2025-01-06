from django.urls import re_path
from auction_management.consumers import AuctionConsumer

websocket_urlpatterns = [
    re_path(r'ws/auction/(?P<auction_id>\w+)/$', AuctionConsumer.as_asgi()),
]