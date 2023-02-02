from django.contrib import admin

from accounts.models import GenieUser, Network, Wallet

admin.site.register(GenieUser)
admin.site.register(Network)
admin.site.register(Wallet)

admin.site.site_header = "Genie 관리자 페이지"
admin.site.site_title = "Genie 관리자 페이지"
admin.site.index_title = "Genie 관리자 페이지"