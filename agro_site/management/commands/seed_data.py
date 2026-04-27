from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from agro_site.models import (User, Crop, CropVariety, HarvestingGuide,
    CropDisease, Fertilizer, Pesticide, MandiPrice, LoanScheme, LearnContent)
import datetime

class Command(BaseCommand):
    help = 'Seed database with 35+ crops and full Tamil Nadu agricultural data'

    def handle(self, *args, **options):
        self.stdout.write('🌱 Seeding AgroHub database...')
        self._users()
        self._crops()
        self._fertilizers()
        self._pesticides()
        self._mandi()
        self._loans()
        self._learn()
        self.stdout.write(self.style.SUCCESS('✅ All data seeded successfully!'))

    def _users(self):
        if not User.objects.filter(username='admin').exists():
            User.objects.create(username='admin', email='admin@agrohub.in',
                password=make_password('admin123'), role='admin',
                is_staff=True, is_superuser=True)
        if not User.objects.filter(username='farmer1').exists():
            User.objects.create(username='farmer1', email='farmer@agrohub.in',
                password=make_password('farmer123'), role='farmer',
                district='Trichy', village='Srirangam', land_area=2.5)

    def _crops(self):
        Crop.objects.all().delete()
        crops_data = [
            # (name, name_ta, emoji, cat, season, dur, water, temp, soil, ph, yield_, price, desc_en, desc_ta, districts)
            ('Paddy (Rice)', 'நெல்', '🌾', 'grain', 'Kharif & Rabi',
             '110–130 days', '1200–2000 mm', '20–35°C', 'Clay loam, alluvial', '5.5–7.0',
             '4–6 tonnes/ha', '₹1800–2200/quintal',
             'Paddy is the most important crop of Tamil Nadu. Cultivated in delta regions with abundant water supply.',
             'நெல் தமிழ்நாட்டின் மிக முக்கியமான பயிர். கோடை மற்றும் குளிர்காலத்தில் பயிரிடப்படுகிறது.',
             'Thanjavur, Tiruvarur, Nagapattinam, Trichy'),

            ('Tomato', 'தக்காளி', '🍅', 'vegetable', 'Year-round',
             '60–90 days', '400–600 mm', '20–27°C', 'Sandy loam, well-drained', '6.0–7.0',
             '25–40 tonnes/ha', '₹800–2000/quintal',
             'Tomato is a high-value vegetable crop grown across Tamil Nadu with excellent market demand.',
             'தக்காளி அதிக மதிப்புடைய காய்கறி. தமிழ்நாடு முழுவதும் நன்கு சந்தை தேவை உள்ளது.',
             'Dharmapuri, Salem, Coimbatore, Dindigul'),

            ('Onion', 'வெங்காயம்', '🧅', 'vegetable', 'Rabi',
             '90–120 days', '350–500 mm', '15–30°C', 'Loamy, well-drained', '6.0–7.5',
             '20–30 tonnes/ha', '₹600–1500/quintal',
             'Onion is a major commercial vegetable crop with high export potential.',
             'வெங்காயம் முக்கிய வணிக காய்கறி பயிர், ஏற்றுமதி திறன் அதிகம்.',
             'Perambalur, Pudukottai, Namakkal, Salem'),

            ('Sugarcane', 'கரும்பு', '🎋', 'commercial', 'Year-round',
             '10–18 months', '1500–2500 mm', '20–35°C', 'Deep loamy, alluvial', '6.0–8.0',
             '80–120 tonnes/ha', '₹2800–3200/tonne',
             'Sugarcane is a major cash crop used for sugar and jaggery production.',
             'கரும்பு சர்க்கரை மற்றும் வெல்லம் தயாரிப்புக்கு பயன்படுத்தப்படும் முக்கிய வணிக பயிர்.',
             'Erode, Vellore, Tiruvannamalai, Cuddalore'),

            ('Banana', 'வாழை', '🍌', 'fruit', 'Year-round',
             '11–18 months', '1200–2200 mm', '25–35°C', 'Sandy loam, rich in organic matter', '5.5–7.0',
             '25–40 tonnes/ha', '₹1200–2000/quintal',
             'Banana is Tamil Nadu\'s most important fruit crop with varieties like Poovan and Nendran.',
             'வாழை தமிழ்நாட்டின் மிக முக்கியமான பழப் பயிர். பூவன் மற்றும் நேந்திரம் பிரபல ரகங்கள்.',
             'Theni, Dindigul, Trichy, Erode'),

            ('Groundnut', 'நிலக்கடலை', '🥜', 'oilseed', 'Kharif & Rabi',
             '90–130 days', '500–700 mm', '25–30°C', 'Sandy loam, red soil', '6.0–7.0',
             '1.5–2.5 tonnes/ha', '₹4500–5500/quintal',
             'Groundnut is the main oilseed crop of Tamil Nadu, grown in red soil areas.',
             'நிலக்கடலை தமிழ்நாட்டின் முக்கிய எண்ணெய் வித்து பயிர். சிவப்பு மண் பகுதிகளில் நன்கு வளரும்.',
             'Vellore, Villupuram, Tiruvannamalai, Cuddalore'),

            ('Turmeric', 'மஞ்சள்', '🟡', 'spice', 'Kharif',
             '7–9 months', '1500–2000 mm', '20–30°C', 'Sandy loam, clay loam', '5.5–7.0',
             '20–25 tonnes/ha (fresh)', '₹6000–9000/quintal',
             'Erode district is the turmeric hub of India. Tamil Nadu produces premium quality turmeric.',
             'ஈரோடு மாவட்டம் இந்தியாவின் மஞ்சள் தலைநகரம். தமிழ்நாடு உயர்தர மஞ்சள் உற்பத்தி செய்கிறது.',
             'Erode, Salem, Coimbatore, Namakkal'),

            ('Maize', 'மக்காச்சோளம்', '🌽', 'grain', 'Kharif & Rabi',
             '90–110 days', '600–900 mm', '18–27°C', 'Sandy loam, well-drained', '5.5–7.0',
             '4–8 tonnes/ha', '₹1700–2000/quintal',
             'Maize is a versatile crop used for food, fodder and industrial purposes.',
             'மக்காச்சோளம் உணவு, தீவனம் மற்றும் தொழில் ரீதியான பயன்பாட்டிற்கு பயன்படுகிறது.',
             'Dharmapuri, Salem, Krishnagiri, Vellore'),

            ('Black Gram (Urad)', 'கருப்பு உளுந்து', '🫘', 'pulse', 'Kharif & Rabi',
             '70–90 days', '300–500 mm', '25–35°C', 'Sandy loam, clay loam', '6.0–7.5',
             '0.6–1.2 tonnes/ha', '₹5000–7000/quintal',
             'Black gram is an important pulse crop rich in protein, widely used in Tamil cuisine.',
             'கருப்பு உளுந்து புரதச்சத்து நிறைந்த முக்கியமான பருப்பு வகை பயிர்.',
             'Trichy, Madurai, Pudukkottai, Dindigul'),

            ('Green Gram (Moong)', 'பச்சை பயறு', '💚', 'pulse', 'Year-round',
             '60–75 days', '300–400 mm', '25–35°C', 'Sandy loam, alluvial', '6.0–7.5',
             '0.5–1.0 tonnes/ha', '₹6000–8000/quintal',
             'Green gram is a short-duration pulse crop suitable for multiple cropping systems.',
             'பச்சை பயறு குறுகிய காலம் கொண்ட பருப்பு வகை பயிர், பல பயிர் முறைக்கு ஏற்றது.',
             'Madurai, Virudhunagar, Ramanathapuram, Sivaganga'),

            ('Chilli', 'மிளகாய்', '🌶️', 'spice', 'Kharif & Rabi',
             '90–150 days', '600–1200 mm', '20–30°C', 'Sandy loam, clay loam', '6.0–7.5',
             '3–5 tonnes/ha (dry)', '₹8000–15000/quintal',
             'Chilli is an important spice crop with good export value. Varieties like K1, K2 popular.',
             'மிளகாய் முக்கியமான மசாலா பயிர், நல்ல ஏற்றுமதி மதிப்பு கொண்டது. K1, K2 ரகங்கள் பிரபலம்.',
             'Ramanathapuram, Virudhunagar, Madurai, Sivaganga'),

            ('Brinjal (Eggplant)', 'கத்தரிக்காய்', '🍆', 'vegetable', 'Year-round',
             '60–120 days', '500–700 mm', '22–32°C', 'Sandy loam, clay loam', '5.5–6.8',
             '20–40 tonnes/ha', '₹600–1200/quintal',
             'Brinjal is cultivated throughout Tamil Nadu with good adaptability to various soils.',
             'கத்தரிக்காய் தமிழ்நாடு முழுவதும் பயிரிடப்படுகிறது, பல்வேறு மண் வகைகளுக்கு பொருந்தும்.',
             'Coimbatore, Salem, Trichy, Madurai'),

            ('Lady Finger (Okra)', 'வெண்டைக்காய்', '🌿', 'vegetable', 'Year-round',
             '45–60 days', '500–700 mm', '24–35°C', 'Sandy loam, loamy', '6.0–7.5',
             '6–10 tonnes/ha', '₹800–1500/quintal',
             'Lady finger (Bhindi) is a popular summer vegetable with high nutritional value.',
             'வெண்டைக்காய் அதிக சத்துமிக்க பிரபலமான கோடைகால காய்கறி.',
             'Coimbatore, Erode, Salem, Trichy'),

            ('Potato', 'உருளைக்கிழங்கு', '🥔', 'vegetable', 'Rabi',
             '80–120 days', '400–600 mm', '15–25°C', 'Sandy loam, loamy', '5.5–6.5',
             '20–30 tonnes/ha', '₹800–1500/quintal',
             'Potato is a cool-weather crop grown mainly in Nilgiris and hilly areas.',
             'உருளைக்கிழங்கு குளிர்கால பயிர், முக்கியமாக நீலகிரி மற்றும் மலை பகுதிகளில் வளர்க்கப்படுகிறது.',
             'Nilgiris, Coimbatore, Dindigul'),

            ('Cabbage', 'முட்டைகோஸ்', '🥬', 'vegetable', 'Rabi',
             '60–90 days', '400–600 mm', '15–25°C', 'Sandy loam, well-drained', '6.0–7.0',
             '25–40 tonnes/ha', '₹400–800/quintal',
             'Cabbage is a cool-season vegetable with high demand in markets.',
             'முட்டைகோஸ் குளிர்காலத்தில் வளரும் காய்கறி, சந்தையில் அதிக தேவை உள்ளது.',
             'Nilgiris, Coimbatore, Dharmapuri, Salem'),

            ('Cauliflower', 'காலிஃப்ளவர்', '🥦', 'vegetable', 'Rabi',
             '55–80 days', '400–600 mm', '15–25°C', 'Sandy loam, clay loam', '6.0–7.5',
             '15–25 tonnes/ha', '₹600–1200/quintal',
             'Cauliflower is a high-value winter vegetable with good nutritional content.',
             'காலிஃப்ளவர் அதிக மதிப்புடைய குளிர்கால காய்கறி, சத்தான உணவு.',
             'Nilgiris, Coimbatore, Krishnagiri'),

            ('Carrot', 'கேரட்', '🥕', 'vegetable', 'Rabi',
             '80–120 days', '400–500 mm', '16–24°C', 'Sandy loam, loose loamy', '6.0–7.0',
             '20–30 tonnes/ha', '₹600–1200/quintal',
             'Carrot is a root vegetable grown in cool hilly areas, rich in beta-carotene.',
             'கேரட் குளிர் மலை பகுதிகளில் வளரும் கிழங்கு காய்கறி, பீட்டா கரோட்டின் நிறைந்தது.',
             'Nilgiris, Coimbatore, Kodaikanal'),

            ('Beans (French)', 'பீன்ஸ்', '🫘', 'vegetable', 'Kharif & Rabi',
             '50–70 days', '400–600 mm', '15–25°C', 'Sandy loam, well-drained', '6.0–7.5',
             '8–12 tonnes/ha', '₹800–1500/quintal',
             'French beans is a popular vegetable crop with high export potential.',
             'பீன்ஸ் அதிக ஏற்றுமதி திறன் கொண்ட பிரபலமான காய்கறி பயிர்.',
             'Nilgiris, Coimbatore, Dharmapuri'),

            ('Bitter Gourd', 'பாவக்காய்', '🫑', 'vegetable', 'Year-round',
             '55–65 days', '600–800 mm', '24–35°C', 'Sandy loam, loamy', '6.0–7.5',
             '8–12 tonnes/ha', '₹800–1500/quintal',
             'Bitter gourd has high medicinal value and is cultivated year-round in Tamil Nadu.',
             'பாவக்காய் அதிக மருத்துவ மதிப்பு கொண்டது, ஆண்டு முழுவதும் பயிரிடப்படுகிறது.',
             'Madurai, Dindigul, Trichy, Salem'),

            ('Mango', 'மாம்பழம்', '🥭', 'fruit', 'Summer',
             '3–5 years (first yield)', '900–1500 mm', '25–35°C', 'Deep loamy, alluvial', '5.5–7.5',
             '10–15 tonnes/ha', '₹3000–6000/quintal',
             'Tamil Nadu is famous for Alphonso, Bangalora and Neelam mango varieties.',
             'தமிழ்நாடு அல்ஃபோன்ஸோ, பங்களோரா மற்றும் நீலம் மாம்பழ ரகங்களுக்கு பிரபலமானது.',
             'Krishnagiri, Dharmapuri, Salem, Vellore'),

            ('Papaya', 'பப்பாளி', '🧡', 'fruit', 'Year-round',
             '9–11 months (first yield)', '1000–1500 mm', '25–35°C', 'Sandy loam, loamy', '6.0–7.0',
             '50–80 tonnes/ha', '₹800–1500/quintal',
             'Papaya is a fast-bearing fruit crop with both fresh consumption and processing value.',
             'பப்பாளி விரைவில் காய்க்கும் பழப் பயிர், புதிய உண்ணல் மற்றும் பதப்படுத்துவதற்கு பயன்படுகிறது.',
             'Coimbatore, Salem, Erode, Trichy'),

            ('Guava', 'கொய்யா', '🍈', 'fruit', 'Year-round',
             '2–3 years (first yield)', '1000–2000 mm', '23–28°C', 'Sandy loam, alluvial', '4.5–8.0',
             '15–25 tonnes/ha', '₹1200–2000/quintal',
             'Guava is a hardy fruit crop rich in Vitamin C with high market demand.',
             'கொய்யா வைட்டமின் C நிறைந்த, சந்தையில் அதிக தேவை உள்ள கடினமான பழப் பயிர்.',
             'Krishnagiri, Vellore, Salem, Trichy'),

            ('Coconut', 'தென்னை', '🥥', 'plantation', 'Year-round',
             '5–7 years (first yield)', '1500–2500 mm', '27–32°C', 'Sandy loam, alluvial, laterite', '5.5–8.0',
             '60–80 nuts/palm/year', '₹15–25/nut',
             'Tamil Nadu is the second-largest coconut producer in India. Coimbatore is the hub.',
             'தமிழ்நாடு இந்தியாவின் இரண்டாவது பெரிய தேங்காய் உற்பத்தியாளர். கோயம்புத்தூர் மையம்.',
             'Coimbatore, Erode, Salem, Tirupur'),

            ('Lemon', 'எலுமிச்சை', '🍋', 'fruit', 'Year-round',
             '2–3 years (first yield)', '750–1200 mm', '20–30°C', 'Sandy loam, loamy', '5.5–7.5',
             '10–15 tonnes/ha', '₹2000–4000/quintal',
             'Lemon is an important citrus crop with good market demand throughout the year.',
             'எலுமிச்சை ஆண்டு முழுவதும் நல்ல சந்தை தேவை கொண்ட முக்கியமான சிட்ரஸ் பயிர்.',
             'Vellore, Krishnagiri, Salem, Dharmapuri'),

            ('Cotton', 'பருத்தி', '☁️', 'commercial', 'Kharif',
             '160–200 days', '500–900 mm', '21–30°C', 'Black cotton soil, clay loam', '6.0–8.5',
             '1.5–2.5 tonnes/ha (seed cotton)', '₹5500–6500/quintal',
             'Cotton is a major commercial crop grown in black cotton soil areas of Tamil Nadu.',
             'பருத்தி தமிழ்நாட்டின் கறுப்பு மண் பகுதிகளில் வளரும் முக்கிய வணிக பயிர்.',
             'Coimbatore, Tirupur, Erode, Salem'),

            ('Sunflower', 'சூரியகாந்தி', '🌻', 'oilseed', 'Kharif & Rabi',
             '85–100 days', '500–750 mm', '20–30°C', 'Sandy loam, clay loam', '6.0–7.5',
             '1.2–1.8 tonnes/ha', '₹4000–5000/quintal',
             'Sunflower is an important oilseed crop with shorter duration and higher oil content.',
             'சூரியகாந்தி குறுகிய கால முக்கியமான எண்ணெய் வித்து பயிர்.',
             'Vellore, Tiruvannamalai, Villupuram, Cuddalore'),

            ('Sesame', 'எள்', '🫙', 'oilseed', 'Kharif',
             '70–90 days', '300–500 mm', '25–35°C', 'Sandy loam, red soil', '6.0–7.0',
             '0.4–0.8 tonnes/ha', '₹8000–10000/quintal',
             'Sesame is an ancient oilseed crop with high oil content and excellent market value.',
             'எள் அதிக எண்ணெய் உள்ளடக்கம் மற்றும் சிறந்த சந்தை மதிப்பு கொண்ட பழமையான எண்ணெய் வித்து.',
             'Ramanathapuram, Virudhunagar, Sivaganga, Tirunelveli'),

            ('Ginger', 'இஞ்சி', '🫚', 'spice', 'Kharif',
             '7–9 months', '1500–2500 mm', '22–28°C', 'Loamy, well-drained', '5.6–6.5',
             '15–20 tonnes/ha (fresh)', '₹4000–8000/quintal',
             'Ginger is a high-value spice crop grown in humid forest-edge areas.',
             'இஞ்சி அதிக மதிப்புடைய மசாலா பயிர், ஈர காடோர பகுதிகளில் வளர்க்கப்படுகிறது.',
             'Erode, Coimbatore, Salem, Dharmapuri'),

            ('Garlic', 'பூண்டு', '🧄', 'spice', 'Rabi',
             '120–150 days', '400–600 mm', '15–25°C', 'Sandy loam, loamy', '6.0–7.5',
             '8–12 tonnes/ha', '₹3000–6000/quintal',
             'Garlic is an important spice with high market demand and good storage life.',
             'பூண்டு சந்தையில் அதிக தேவை மற்றும் நீண்ட சேமிப்பு ஆயுள் கொண்ட முக்கியமான மசாலா.',
             'Trichy, Madurai, Salem, Namakkal'),

            ('Coriander', 'கொத்தமல்லி', '🌿', 'spice', 'Rabi',
             '45–60 days', '300–400 mm', '20–30°C', 'Sandy loam, loamy', '6.0–7.5',
             '0.8–1.2 tonnes/ha (dry seed)', '₹6000–9000/quintal',
             'Coriander is used as fresh herb and dry spice. Short-duration profitable crop.',
             'கொத்தமல்லி புதிய மூலிகையாகவும் உலர் மசாலாவாகவும் பயன்படுத்தப்படுகிறது.',
             'Salem, Erode, Coimbatore, Namakkal'),

            ('Ragi (Finger Millet)', 'ராகி', '🌾', 'grain', 'Kharif',
             '90–130 days', '500–800 mm', '20–30°C', 'Sandy loam, red soil', '5.5–7.0',
             '2–4 tonnes/ha', '₹2200–2800/quintal',
             'Ragi is a drought-resistant nutritious millet crop, excellent for dry farming.',
             'ராகி வறட்சியை தாங்கும் சத்துமிக்க சிறுதானிய பயிர், வறண்ட விவசாயத்திற்கு சிறந்தது.',
             'Salem, Dharmapuri, Krishnagiri, Vellore'),

            ('Sorghum (Jowar)', 'சோளம்', '🌾', 'grain', 'Kharif & Rabi',
             '100–120 days', '400–700 mm', '25–35°C', 'Sandy loam, clay loam, black soil', '6.0–7.5',
             '2–4 tonnes/ha', '₹1800–2400/quintal',
             'Sorghum is a drought-tolerant crop used for food, fodder and industrial purposes.',
             'சோளம் வறட்சியை தாங்கும் பயிர், உணவு, தீவனம் மற்றும் தொழில் ரீதியாக பயன்படுகிறது.',
             'Madurai, Virudhunagar, Ramanathapuram, Dindigul'),

            ('Pearl Millet (Kambu)', 'கம்பு', '🌾', 'grain', 'Kharif',
             '65–90 days', '300–500 mm', '25–35°C', 'Sandy, sandy loam', '6.0–7.5',
             '1.5–3.0 tonnes/ha', '₹1800–2400/quintal',
             'Kambu (Pearl millet) is a drought-resistant crop ideal for dry zones of Tamil Nadu.',
             'கம்பு வறட்சியை தாங்கும் பயிர், தமிழ்நாட்டின் வறண்ட மண்டலங்களுக்கு ஏற்றது.',
             'Ramanathapuram, Virudhunagar, Sivaganga, Madurai'),

            ('Chickpea (Bengal Gram)', 'கடலை', '🟡', 'pulse', 'Rabi',
             '90–120 days', '300–500 mm', '15–29°C', 'Sandy loam, clay loam', '6.0–8.0',
             '0.8–1.5 tonnes/ha', '₹5000–7000/quintal',
             'Chickpea is a cool-season pulse crop rich in protein with high market demand.',
             'கடலை புரதம் நிறைந்த குளிர்கால பருப்பு வகை பயிர், சந்தையில் அதிக தேவை.',
             'Coimbatore, Salem, Krishnagiri, Dharmapuri'),

            ('Castor', 'ஆமணக்கு', '🌿', 'oilseed', 'Kharif',
             '150–180 days', '500–750 mm', '20–30°C', 'Sandy loam, deep loamy', '5.5–7.5',
             '1.5–2.5 tonnes/ha', '₹5000–6500/quintal',
             'Castor is an industrial oilseed crop with high demand for lubricants and cosmetics.',
             'ஆமணக்கு தொழில்துறை எண்ணெய் வித்து பயிர், உயவுக்கு மற்றும் அழகுசாதனப் பொருட்களில் பயன்படுகிறது.',
             'Tiruvannamalai, Villupuram, Cuddalore, Pondicherry'),
        ]

        for data in crops_data:
            (name, name_ta, emoji, cat, season, dur, water, temp, soil, ph,
             yield_, price, desc_en, desc_ta, districts) = data
            crop = Crop.objects.create(
                name=name, name_tamil=name_ta, emoji=emoji, category=cat,
                season=season, duration_days=dur, water_req=water,
                temp_range=temp, soil_type=soil, ph_range=ph,
                yield_per_ha=yield_, market_price=price,
                description=desc_en, description_tamil=desc_ta,
                suitable_districts=districts
            )
            # Add varieties for each crop
            CropVariety.objects.create(crop=crop, name=f'{name} - Improved Variety',
                duration=dur, yield_info=yield_, specialty='High yielding, disease resistant',
                released_by='TNAU')
            # Harvesting guide
            HarvestingGuide.objects.create(crop=crop,
                maturity_signs='Leaves turning yellow, grains hardening, typical crop color change',
                harvest_method='Manual or mechanical harvesting based on crop type and field size',
                post_harvest='Proper drying, cleaning and grading before storage',
                storage_tips='Store in cool dry place. Use hermetic bags for grains.',
                best_time='Morning hours to avoid heat stress',
                shelf_life='2–6 months depending on storage conditions')
            # Disease
            CropDisease.objects.create(crop=crop,
                name='Leaf Blight', name_tamil='இலை கருகல்',
                symptoms='Brown spots on leaves, yellowing, wilting',
                treatment='Spray Mancozeb 2g/litre or Copper Oxychloride 3g/litre',
                prevention='Crop rotation, seed treatment, balanced fertilization',
                severity='Medium')

        self.stdout.write(f'  ✅ {Crop.objects.count()} crops created')

    def _fertilizers(self):
        Fertilizer.objects.all().delete()
        ferts = [
            ('Urea', 'யூரியா', 'chemical', '46-0-0', '100-150 kg/acre', 'All crops esp. paddy, maize', 'Broadcast or band application', 'Quick nitrogen supply, promotes vegetative growth', '₹260–290/bag (50kg)', '🌿'),
            ('DAP', 'டி.ஏ.பி', 'chemical', '18-46-0', '50-75 kg/acre', 'All crops', 'Basal application at sowing', 'Phosphorus supply, root development', '₹1200–1400/bag (50kg)', '🔵'),
            ('MOP (Potash)', 'பொட்டாஷ்', 'chemical', '0-0-60', '30-50 kg/acre', 'Sugarcane, banana, potato', 'Basal or split application', 'Improves quality, disease resistance', '₹700–900/bag (50kg)', '🟠'),
            ('Vermicompost', 'மண்புழு உரம்', 'organic', 'N/A', '500 kg–1 tonne/acre', 'All crops', 'Mixed in soil before planting', 'Improves soil health, water retention, microbial activity', '₹8–12/kg', '🪱'),
            ('FYM', 'தொழு உரம்', 'organic', 'N/A', '2–4 tonnes/acre', 'All crops', 'Apply 3-4 weeks before sowing', 'Long-lasting soil improvement, complete nutrition', '₹2–5/kg', '🐄'),
            ('Neem Cake', 'வேப்பம் புண்ணாக்கு', 'organic', '4-1-1.5', '100-150 kg/acre', 'All crops', 'Mix in soil before sowing', 'Pest repellent, slow-release N, nematode control', '₹15–20/kg', '🌿'),
            ('NPK 19:19:19', 'NPK 19:19:19', 'chemical', '19-19-19', '3-5 kg/acre (foliar)', 'Vegetables, fruits', 'Foliar spray or drip', 'Balanced nutrition, ideal for hydroponics', '₹2800–3200/bag (25kg)', '🔷'),
            ('Rhizobium', 'ரைசோபியம்', 'biofertilizer', 'N/A', '200g/10kg seed', 'Pulses, legumes', 'Seed treatment', 'Nitrogen fixation, reduces urea need by 25kg', '₹40–60/packet', '🦠'),
            ('Azospirillum', 'அசோஸ்பிரில்லம்', 'biofertilizer', 'N/A', '2kg/acre', 'Cereals, maize, sorghum', 'Soil application or seedling dip', 'Nitrogen fixation in non-legume crops', '₹40–60/packet', '🧬'),
            ('Phosphobacteria', 'பாஸ்போபாக்டீரியா', 'biofertilizer', 'N/A', '2kg/acre', 'All crops', 'Mix with FYM, soil application', 'Converts insoluble P to soluble form', '₹40–60/packet', '💊'),
        ]
        for f in ferts:
            Fertilizer.objects.create(name=f[0], name_tamil=f[1], ftype=f[2], npk_ratio=f[3],
                dosage=f[4], suitable_crops=f[5], application=f[6], benefits=f[7], price_range=f[8], emoji=f[9])
        self.stdout.write(f'  ✅ {Fertilizer.objects.count()} fertilizers created')

    def _pesticides(self):
        Pesticide.objects.all().delete()
        pests = [
            ('Chlorpyrifos 20EC', 'insecticide', 'Chlorpyrifos', 'Stem borer, Root grub, White fly', '2ml/litre', '21 days', '⚠️ Wear gloves & mask. Do not spray near water bodies.', False, '💊'),
            ('Lambda-Cyhalothrin', 'insecticide', 'Lambda-Cyhalothrin', 'Bollworm, Aphids, Thrips', '1ml/litre', '14 days', '⚠️ Highly toxic to fish. Avoid drift near water.', False, '🔴'),
            ('Mancozeb 75WP', 'fungicide', 'Mancozeb', 'Late blight, Downy mildew, Leaf spot', '2.5g/litre', '10 days', '✅ Moderate toxicity. Wear protective gear.', False, '🟡'),
            ('Copper Hydroxide', 'fungicide', 'Copper Hydroxide', 'Bacterial diseases, Anthracnose', '3g/litre', '7 days', '✅ Low risk. Avoid copper accumulation in soil.', False, '🔵'),
            ('Imidacloprid 17.8SL', 'insecticide', 'Imidacloprid', 'Sucking pests, White fly, Jassids', '0.5ml/litre', '21 days', '⚠️ Harmful to bees. Do NOT spray on flowering crops.', False, '⚠️'),
            ('Neem Oil 1500ppm', 'insecticide', 'Azadirachtin', 'Mites, Aphids, Whitefly, Leaf minor', '5ml/litre', '0 days (organic)', '✅ Safe for beneficial insects. Can use near harvest.', True, '🌿'),
            ('Trichoderma viride', 'fungicide', 'Trichoderma viride', 'Soil-borne fungi: Fusarium, Pythium', '4g/kg seed or 2.5kg/acre', '0 days (organic)', '✅ Completely safe. Beneficial micro-organism.', True, '🦠'),
            ('Glyphosate 41SL', 'herbicide', 'Glyphosate', 'Broad leaf weeds, Grasses', '1.5–2 litre/acre', '30 days', '🚨 Do NOT spray on crops. Directed soil spray only.', False, '☠️'),
            ('Pendimethalin', 'herbicide', 'Pendimethalin', 'Annual grasses, Broadleaf weeds', '1.5–2 litre/acre', '15 days', '⚠️ Pre-emergence herbicide. Apply before germination.', False, '🟠'),
            ('Emamectin Benzoate', 'insecticide', 'Emamectin Benzoate', 'Leaf borer, Army worm, DBM', '0.4g/litre', '14 days', '⚠️ Wear full protective equipment while spraying.', False, '💉'),
        ]
        for p in pests:
            Pesticide.objects.create(name=p[0], ptype=p[1], active_ingredient=p[2],
                target_pests=p[3], dosage=p[4], safety_interval=p[5],
                precautions=p[6], is_organic=p[7], emoji=p[8])
        self.stdout.write(f'  ✅ {Pesticide.objects.count()} pesticides created')

    def _mandi(self):
        MandiPrice.objects.all().delete()
        today = datetime.date.today()
        prices = [
            ('Tomato', '🍅', 'Koyambedu, Chennai', 850, 1400, 1100, 'Quintal', 'up'),
            ('Onion', '🧅', 'Salem', 700, 1200, 950, 'Quintal', 'down'),
            ('Paddy (Raw)', '🌾', 'Thanjavur', 1900, 2100, 2000, 'Quintal', 'stable'),
            ('Chilli (Dry)', '🌶️', 'Ramanathapuram', 9000, 14000, 11500, 'Quintal', 'up'),
            ('Turmeric', '🟡', 'Erode', 7000, 9500, 8200, 'Quintal', 'up'),
            ('Groundnut', '🥜', 'Vellore', 4800, 5400, 5100, 'Quintal', 'stable'),
            ('Sugarcane', '🎋', 'Coimbatore', 2800, 3100, 2950, 'Tonne', 'stable'),
            ('Banana (Poovan)', '🍌', 'Trichy', 1300, 1800, 1550, 'Quintal', 'up'),
            ('Maize', '🌽', 'Dharmapuri', 1700, 1900, 1800, 'Quintal', 'down'),
            ('Coconut', '🥥', 'Coimbatore', 12, 22, 17, 'Unit', 'stable'),
            ('Mango (Totapuri)', '🥭', 'Krishnagiri', 2500, 4000, 3200, 'Quintal', 'up'),
            ('Garlic', '🧄', 'Madurai', 3500, 5500, 4500, 'Quintal', 'up'),
            ('Ginger (Fresh)', '🫚', 'Erode', 3500, 6000, 4800, 'Quintal', 'stable'),
            ('Brinjal', '🍆', 'Coimbatore', 600, 1100, 850, 'Quintal', 'down'),
            ('Lady Finger', '🌿', 'Salem', 800, 1400, 1100, 'Quintal', 'up'),
            ('Cauliflower', '🥦', 'Nilgiris', 700, 1300, 1000, 'Quintal', 'down'),
            ('Cabbage', '🥬', 'Nilgiris', 400, 750, 580, 'Quintal', 'stable'),
            ('Carrot', '🥕', 'Nilgiris', 700, 1200, 950, 'Quintal', 'up'),
            ('Cotton (Seed)', '☁️', 'Tirupur', 5500, 6300, 5900, 'Quintal', 'stable'),
            ('Ragi', '🌾', 'Dharmapuri', 2300, 2700, 2500, 'Quintal', 'up'),
        ]
        for p in prices:
            MandiPrice.objects.create(crop_name=p[0], emoji=p[1], district=p[2],
                min_price=p[3], max_price=p[4], modal_price=p[5],
                unit=p[6], trend=p[7], date=today)
        self.stdout.write(f'  ✅ {MandiPrice.objects.count()} mandi prices created')

    def _loans(self):
        LoanScheme.objects.all().delete()
        schemes = [
            ('KCC', 'Kisan Credit Card', '💳', '₹10,000', '₹3,00,000',
             '7% per year (4% with subsidy for prompt repayment)',
             '1 year revolving credit, renewable annually',
             'All farmers owning or leasing agricultural land. Can apply at any bank.',
             'Aadhaar card, Land documents (patta), Passport photo, Bank account',
             '2% interest subvention for prompt repayment. Insurance coverage included.',
             'Visit nearest bank branch or CSC. Fill KCC form. Submit land documents.'),
            ('PM-Kisan', 'Pradhan Mantri Kisan Samman Nidhi', '🏛️', '₹2,000', '₹6,000/year',
             '0% (Direct benefit transfer, not a loan)',
             '3 installments of ₹2000 each per year',
             'All small and marginal farmers with cultivable land. Registered in PM-Kisan portal.',
             'Aadhaar card, Bank account linked to Aadhaar, Land records',
             'Annual income support of ₹6000 in 3 equal installments directly to bank account.',
             'Register at nearest CSC or pmkisan.gov.in. Link Aadhaar with bank account.'),
            ('PMFBY', 'Pradhan Mantri Fasal Bima Yojana', '🌦️', '₹1,000', 'Full crop value',
             '2% (Kharif) / 1.5% (Rabi) farmer premium. Remaining paid by Govt.',
             'Claim within 72 hours of crop loss. Settlement within 45 days.',
             'All farmers growing notified crops in notified areas. KCC holders auto-enrolled.',
             'Aadhaar, Bank account, Land documents, Sowing certificate',
             'Covers yield loss due to drought, flood, pest, disease, fire. Full insurance amount.',
             'Apply through bank branch or CSC before cutoff date. Enroll via PMFBY portal.'),
            ('NABARD', 'Agricultural Infrastructure Fund', '🏗️', '₹1 lakh', '₹2 crore',
             '3% interest subvention per year (effective rate 3-4%)',
             'Up to 7 years with 2 year moratorium',
             'Farmers, FPOs, Agri-entrepreneurs. For post-harvest infrastructure projects.',
             'Project report, Land documents, Registration certificate, Bank statements',
             'For warehouse, cold storage, processing units, silos. 3% subvention per year.',
             'Submit project proposal to NABARD district office or any scheduled bank.'),
        ]
        for s in schemes:
            LoanScheme.objects.create(name=s[0], full_name=s[1], emoji=s[2],
                min_amount=s[3], max_amount=s[4], interest_rate=s[5],
                repayment=s[6], eligibility=s[7], documents=s[8],
                benefits=s[9], how_to_apply=s[10])
        self.stdout.write(f'  ✅ {LoanScheme.objects.count()} loan schemes created')

    def _learn(self):
        LearnContent.objects.all().delete()
        learns = [
            ('Drip Irrigation Basics', 'நீர்த்துளி பாசனம்', 'video', 'irrigation', '15 min', 'Beginner',
             'Learn how to set up drip irrigation, save 50% water and increase yield.', '💧'),
            ('Organic Farming Methods', 'இயற்கை விவசாயம்', 'guide', 'farming', '45 min', 'Intermediate',
             'Complete guide to organic farming: composting, green manure, natural pest control.', '🌿'),
            ('Soil Health Testing', 'மண் ஆரோக்கிய சோதனை', 'video', 'soil', '20 min', 'Beginner',
             'How to test soil pH, NPK levels and interpret results for crop planning.', '🧪'),
            ('Government Subsidy Guide', 'அரசு மானிய வழிகாட்டி', 'guide', 'finance', '30 min', 'Beginner',
             'Complete guide to all agricultural subsidies, how to apply and receive benefits.', '🏛️'),
            ('Pest Identification & Control', 'பூச்சி கண்டறிதல் & கட்டுப்பாடு', 'video', 'pest', '25 min', 'Intermediate',
             'Visual guide to identify common pests and apply correct IPM methods.', '🛡️'),
            ('Post-Harvest Management', 'அறுவடைக்கு பிந்தைய மேலாண்மை', 'guide', 'harvest', '35 min', 'Intermediate',
             'Reduce post-harvest losses with proper storage, grading and market linkage.', '🏪'),
        ]
        for l in learns:
            LearnContent.objects.create(title=l[0], title_tamil=l[1], ctype=l[2],
                category=l[3], duration=l[4], difficulty=l[5], description=l[6], emoji=l[7])
        self.stdout.write(f'  ✅ {LearnContent.objects.count()} learn contents created')