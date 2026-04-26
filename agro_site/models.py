from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [('farmer','Farmer'),('buyer','Buyer'),('merchant','Merchant')]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='farmer')
    phone = models.CharField(max_length=15, blank=True)
    district = models.CharField(max_length=100, blank=True)
    village = models.CharField(max_length=100, blank=True)
    land_area = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    def __str__(self): return f"{self.get_full_name() or self.username} ({self.role})"

class Crop(models.Model):
    CATEGORY = [('vegetable','Vegetable'),('fruit','Fruit'),('grain','Grain'),('cash','Cash Crop'),('spice','Spice')]
    SEASON = [('kharif','Kharif (Jun–Nov)'),('rabi','Rabi (Nov–Apr)'),('zaid','Zaid (Apr–Jun)'),('annual','Annual')]
    name             = models.CharField(max_length=100)
    name_tamil       = models.CharField(max_length=100, blank=True)
    emoji            = models.CharField(max_length=10, default='🌱')
    category         = models.CharField(max_length=20, choices=CATEGORY)
    season           = models.CharField(max_length=20, choices=SEASON)
    duration_days    = models.TextField()
    water_req        = models.TextField()
    temp_range       = models.TextField()
    soil_type        = models.TextField()
    ph_range         = models.CharField(max_length=50)
    yield_per_ha     = models.TextField()
    market_price     = models.TextField()
    description      = models.TextField()
    description_tamil= models.TextField(blank=True)
    suitable_districts = models.TextField(blank=True)
    def __str__(self): return self.name

class CropVariety(models.Model):
    crop        = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='varieties')
    name        = models.CharField(max_length=100)
    duration    = models.TextField()
    yield_info  = models.TextField()
    specialty   = models.TextField()
    released_by = models.CharField(max_length=200, blank=True)
    def __str__(self): return f"{self.crop.name} — {self.name}"

class HarvestingGuide(models.Model):
    crop           = models.OneToOneField(Crop, on_delete=models.CASCADE, related_name='harvest')
    maturity_signs = models.TextField()
    harvest_method = models.TextField()
    post_harvest   = models.TextField()
    storage_tips   = models.TextField()
    best_time      = models.TextField()
    shelf_life     = models.TextField()
    def __str__(self): return f"Harvest: {self.crop.name}"

class CropDisease(models.Model):
    SEVERITY = [('low','Low'),('medium','Medium'),('high','High'),('critical','Critical')]
    crop       = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='diseases')
    name       = models.CharField(max_length=200)
    name_tamil = models.CharField(max_length=200, blank=True)
    symptoms   = models.TextField()
    treatment  = models.TextField()
    prevention = models.TextField()
    severity   = models.CharField(max_length=10, choices=SEVERITY, default='medium')
    def __str__(self): return f"{self.crop.name} — {self.name}"

class Fertilizer(models.Model):
    FTYPE = [('organic','Organic'),('inorganic','Inorganic'),('bio','Bio-Fertilizer'),('npk','NPK Complex')]
    name          = models.CharField(max_length=200)
    name_tamil    = models.CharField(max_length=200, blank=True)
    ftype         = models.CharField(max_length=20, choices=FTYPE)
    npk_ratio     = models.CharField(max_length=100, blank=True)
    dosage        = models.TextField()
    suitable_crops= models.TextField()
    application   = models.TextField()
    benefits      = models.TextField()
    price_range   = models.CharField(max_length=200)
    emoji         = models.CharField(max_length=10, default='🧪')
    def __str__(self): return self.name

class Pesticide(models.Model):
    PTYPE = [('insecticide','Insecticide'),('fungicide','Fungicide'),('herbicide','Herbicide'),('organic','Organic')]
    name              = models.CharField(max_length=200)
    ptype             = models.CharField(max_length=20, choices=PTYPE)
    active_ingredient = models.TextField()
    target_pests      = models.TextField()
    dosage            = models.TextField()
    safety_interval   = models.TextField()
    precautions       = models.TextField()
    is_organic        = models.BooleanField(default=False)
    emoji             = models.CharField(max_length=10, default='🛡️')
    def __str__(self): return self.name

class MandiPrice(models.Model):
    crop_name   = models.CharField(max_length=100)
    emoji       = models.CharField(max_length=10, default='🌾')
    district    = models.CharField(max_length=100)
    min_price   = models.DecimalField(max_digits=8, decimal_places=2)
    max_price   = models.DecimalField(max_digits=8, decimal_places=2)
    modal_price = models.DecimalField(max_digits=8, decimal_places=2)
    unit        = models.CharField(max_length=20, default='kg')
    trend       = models.CharField(max_length=10, default='stable', choices=[('up','Up'),('down','Down'),('stable','Stable')])
    date        = models.DateField(auto_now_add=True)
    def __str__(self): return f"{self.crop_name} — {self.district}"

class LoanScheme(models.Model):
    name          = models.CharField(max_length=200)
    full_name     = models.CharField(max_length=300)
    emoji         = models.CharField(max_length=10, default='🏦')
    min_amount    = models.CharField(max_length=200)
    max_amount    = models.CharField(max_length=200)
    interest_rate = models.TextField()
    repayment     = models.TextField()
    eligibility   = models.TextField()
    documents     = models.TextField()
    benefits      = models.TextField()
    how_to_apply  = models.TextField()
    def __str__(self): return self.name

class FarmDiary(models.Model):
    TYPE = [('income','Income'),('expense','Expense')]
    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='diary_entries')
    date        = models.DateField()
    dtype       = models.CharField(max_length=10, choices=TYPE)
    category    = models.CharField(max_length=100)
    amount      = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=300)
    created_at  = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"{self.user} — {self.dtype} ₹{self.amount}"

class LearnContent(models.Model):
    CTYPE = [('video','Video'),('article','Article'),('guide','Guide')]
    title       = models.CharField(max_length=200)
    title_tamil = models.CharField(max_length=200, blank=True)
    ctype       = models.CharField(max_length=20, choices=CTYPE)
    category    = models.CharField(max_length=100)
    duration    = models.CharField(max_length=50)
    difficulty  = models.CharField(max_length=20, choices=[('beginner','Beginner'),('intermediate','Intermediate'),('advanced','Advanced')])
    description = models.TextField()
    emoji       = models.CharField(max_length=10, default='📚')
    def __str__(self): return self.title
