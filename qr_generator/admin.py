from django.contrib import admin
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import redirect, get_object_or_404
from .models import QRGenerate

@admin.register(QRGenerate)
class QRGenerateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'target_url', 'created_at', 'qr_preview', 'regenerate_qr_button')
    readonly_fields = ('qr_preview',)

    def qr_preview(self, obj):
        if obj.qr_code:
            return format_html('<img src="{}" width="150" height="150" />', obj.qr_code.url)
        return "No QR Code"
    qr_preview.short_description = "QR Code"

    def regenerate_qr_button(self, obj):
        return format_html(
            '<a class="button" href="regenerate_qr/{}/">Regenerate QR</a>', obj.id
        )
    regenerate_qr_button.short_description = 'Regenerate QR'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('regenerate_qr/<int:pk>/', self.admin_site.admin_view(self.regenerate_qr), name='regenerate_qr'),
        ]
        return custom_urls + urls

    def regenerate_qr(self, request, pk):
        config = get_object_or_404(QRGenerate, pk=pk)
        config.generate_qr_code()
        config.save()
        self.message_user(request, f'QR Code regenerated for "{config.name}".')
        return redirect(f'/admin/qr_generator/qrgenerate/{pk}/change/')
