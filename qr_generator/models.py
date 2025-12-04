from django.db import models
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile

class QRGenerate(models.Model):
    class Meta:
        db_table = 'qr_generator'  # Optional: keeps table name consistent

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    target_url = models.URLField(unique=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    deleted = models.BooleanField(default=False)  # Soft delete flag
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def generate_qr_code(self):
        qr = qrcode.make(self.target_url)
        buffer = BytesIO()
        qr.save(buffer, format='PNG')
        file_name = f"{self.name}_qr.png"
        self.qr_code.save(file_name, ContentFile(buffer.getvalue()), save=False)
        buffer.close()

    def save(self, *args, **kwargs):
        if not self.qr_code:
            self.generate_qr_code()
        super().save(*args, **kwargs)
