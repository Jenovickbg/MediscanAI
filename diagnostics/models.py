from djongo import models

class BloodSmear(models.Model):
    patient_id = models.CharField(max_length=255)  # Référence au patient
    image = models.ImageField(upload_to='blood_smears/')  # Stockage de l'image
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Frottis sanguin du patient {self.patient_id}"
class BloodSmear(models.Model):
    patient_id = models.CharField(max_length=100)  # ID ou nom du patient
    image = models.ImageField(upload_to='blood_smears/')  # Stocke l'image
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Date d'upload

    def __str__(self):
        return f"Frottis de {self.patient_id} - {self.uploaded_at.strftime('%Y-%m-%d')}"
