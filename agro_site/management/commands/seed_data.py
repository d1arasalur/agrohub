from django.core.management.base import BaseCommand
from agro_site.models import *

class Command(BaseCommand):
    help = 'Seed all agricultural data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')
        self._crops()
        self._fertilizers()
        self._pesticides()
        self._mandi()
        self._loans()
        self._learn()
        self.stdout.write(self.style.SUCCESS('✅ All data seeded successfully!'))

    def _crops(self):
        Crop.objects.all().delete()

        crops_data = [
            {
                'name':'Paddy','name_tamil':'நெல்','emoji':'🌾','category':'grain','season':'kharif',
                'duration_days':'105–140 days','water_req':'1200–2000 mm (irrigated)','temp_range':'20–35°C',
                'soil_type':'Clay loam, silty clay loam — good water retention','ph_range':'5.5 – 7.0',
                'yield_per_ha':'4–6 tonnes/ha (irrigated), 2–3 tonnes/ha (rainfed)',
                'market_price':'₹1850–2100 per quintal (MSP ₹2183)',
                'description':'Paddy (Oryza sativa) is the primary staple crop of Tamil Nadu. It thrives in standing water conditions and is cultivated in two major seasons — Kuruvai (June–September) and Samba (October–February).',
                'description_tamil':'நெல் (Oryza sativa) தமிழ்நாட்டின் முக்கிய உணவு தானியம். குருவை (ஜூன்–செப்.) மற்றும் சம்பா (அக்.–பிப்.) என இரு பருவங்களில் பயிரிடப்படுகிறது.',
                'suitable_districts':'Thanjavur, Tiruvarur, Nagapattinam, Trichy, Pudukkottai, Cuddalore, Villupuram',
                'varieties':[
                    {'name':'ADT 43','duration':'110–115 days','yield_info':'6.5 t/ha','specialty':'High yield, blast resistant, suitable for irrigated conditions','released_by':'TNAU, Aduthurai'},
                    {'name':'CO 51','duration':'115–120 days','yield_info':'5.8 t/ha','specialty':'Fine grain, good taste, drought tolerant','released_by':'TNAU Coimbatore'},
                    {'name':'BPT 5204 (Samba Mahsuri)','duration':'140–145 days','yield_info':'5.5 t/ha','specialty':'Long slender grain, premium market price, aromatic','released_by':'ANGRAU'},
                    {'name':'CR 1009 (Swarna)','duration':'135–140 days','yield_info':'4.8 t/ha','specialty':'Semi-dwarf, flood tolerant, excellent cooking quality','released_by':'CRRI Cuttack'},
                ],
                'harvest':{
                    'maturity_signs':'Grains turn golden yellow, 80% panicles ripe, grain moisture 20–25%, leaves dry up',
                    'harvest_method':'Use combine harvester or manual sickle cutting at base. Harvest in morning to avoid grain shattering. Thresh immediately or within 24 hours.',
                    'post_harvest':'Dry paddy to 14% moisture for milling or 12% for storage. Avoid delays to prevent fungal growth.',
                    'storage_tips':'Store in clean, dry gunny bags or metal bins. Maintain 12–14% moisture. Use neem leaves or phosphine tablets for pest control. Check every 15 days.',
                    'best_time':'Morning hours (6–10 AM) to avoid grain shattering and heat damage',
                    'shelf_life':'6–12 months with proper storage'
                },
                'diseases':[
                    {'name':'Paddy Blast','name_tamil':'கதிர் கருகல் நோய்','severity':'critical',
                     'symptoms':'Diamond-shaped gray spots with brown borders on leaves. Lesions on neck cause "neck blast" — panicle breaks. Severe infection kills entire tillers.',
                     'treatment':'Spray Tricyclazole 75WP @ 0.6g/L or Carbendazim 50WP @ 1g/L. Apply 2 sprays at 10-day intervals starting at boot stage. Use Propiconazole for neck blast.',
                     'prevention':'Use resistant varieties (ADT 43, CO 51). Avoid excess nitrogen. Don\'t spray water from blast-affected fields. Burn crop debris.'},
                    {'name':'Brown Plant Hopper (BPH)','name_tamil':'பழுப்பு நெல் தத்துப்பூச்சி','severity':'high',
                     'symptoms':'Hopper burn — circular yellowing and drying patches in field (like scorched areas). Hoppers found at base of tillers near water level.',
                     'treatment':'Imidacloprid 17.8SL @ 0.25 ml/L or Buprofezin 25SC @ 1.6 ml/L. Drain field before spraying for better penetration.',
                     'prevention':'Avoid close planting. Don\'t use excess nitrogen. Conserve natural enemies (spiders, beetles). Use light traps to monitor.'},
                ],
            },
            {
                'name':'Tomato','name_tamil':'தக்காளி','emoji':'🍅','category':'vegetable','season':'rabi',
                'duration_days':'70–90 days (transplanting to harvest)','water_req':'400–600 mm',
                'temp_range':'20–27°C (optimum); avoid >35°C during flowering',
                'soil_type':'Well-drained sandy loam to clay loam, rich in organic matter',
                'ph_range':'6.0 – 7.0',
                'yield_per_ha':'25–40 tonnes/ha (hybrid varieties up to 60 t/ha)',
                'market_price':'₹15–80/kg (highly variable, average ₹30–45/kg)',
                'description':'Tomato is Tamil Nadu\'s most important vegetable crop. It is grown year-round in Krishnagiri, Dharmapuri, Dindigul and Salem districts. Hybrid varieties have transformed yields significantly.',
                'description_tamil':'தக்காளி தமிழ்நாட்டின் மிக முக்கியமான காய்கறி பயிர். கிருஷ்ணகிரி, தர்மபுரி, திண்டுக்கல் மற்றும் சேலம் மாவட்டங்களில் ஆண்டு முழுவதும் சாகுபடி செய்யப்படுகிறது.',
                'suitable_districts':'Krishnagiri, Dharmapuri, Dindigul, Salem, Coimbatore, Namakkal',
                'varieties':[
                    {'name':'PKM 1','duration':'75–80 days','yield_info':'27 t/ha','specialty':'Determinate, firm fruits good for transport, tolerates high temperature','released_by':'TNAU Periyakulam'},
                    {'name':'CO 3','duration':'80–85 days','yield_info':'30 t/ha','specialty':'Semi-determinate, tolerant to TYLCV virus, good shelf life','released_by':'TNAU'},
                    {'name':'Arka Rakshak (Hybrid)','duration':'70–75 days','yield_info':'55–60 t/ha','specialty':'Triple disease resistant, extra large fruits 80–90g, best for open field','released_by':'IIHR Bangalore'},
                    {'name':'US 440 (Hybrid)','duration':'75 days','yield_info':'50–55 t/ha','specialty':'Indeterminate, excellent packing quality, widely grown commercially','released_by':'US Agri Seeds'},
                ],
                'harvest':{
                    'maturity_signs':'Fruits turn from green to yellowish-green (for transport) or full red (local market). Blossom end softens slightly.',
                    'harvest_method':'Hand pick individually. For distant markets, harvest at mature green or pink stage. For local, harvest red-ripe. Pick every 3–4 days.',
                    'post_harvest':'Grade by size and colour. Pack in single layer in crates with cushioning material. Precool if possible.',
                    'storage_tips':'Store at 12–13°C (mature green) or 8–10°C (ripe). Do not refrigerate below 8°C — causes chilling injury. Shelf life 2–3 weeks at cool temperature.',
                    'best_time':'Morning hours before heat of the day. Avoid harvesting in rain.',
                    'shelf_life':'7–14 days at room temperature; up to 3 weeks in cold storage'
                },
                'diseases':[
                    {'name':'Early Blight (Alternaria)','name_tamil':'ஆரம்ப இலை கருகல்','severity':'medium',
                     'symptoms':'Concentric ring spots (target-board pattern) on older leaves, dark brown with yellow halo. Moves from lower to upper leaves. Defoliation in severe cases.',
                     'treatment':'Mancozeb 75WP @ 2.5g/L or Chlorothalonil 75WP @ 2g/L. Apply every 7–10 days. Copper oxychloride is also effective.',
                     'prevention':'Crop rotation with non-solanaceous crops. Remove infected leaves. Avoid overhead irrigation. Use disease-free transplants.'},
                    {'name':'Tomato Leaf Curl Virus (TYLCV)','name_tamil':'தக்காளி இலை சுருள் நோய்','severity':'high',
                     'symptoms':'Upward curling and cupping of leaves, stunted growth, yellowing of leaf margins, reduced fruit set. Transmitted by whitefly (Bemisia tabaci).',
                     'treatment':'No direct cure for virus. Control whitefly vector: Imidacloprid 17.8SL @ 0.3 ml/L or Thiamethoxam 25WG @ 0.3g/L. Remove and destroy infected plants.',
                     'prevention':'Use virus-resistant varieties (CO 3, Arka Rakshak). Install yellow sticky traps. Spray neem oil 3% to repel whiteflies. Avoid planting near infected fields.'},
                ],
            },
            {
                'name':'Onion','name_tamil':'வெங்காயம்','emoji':'🧅','category':'vegetable','season':'rabi',
                'duration_days':'110–130 days (from transplanting)','water_req':'350–550 mm',
                'temp_range':'15–25°C; bulb development needs 20–25°C',
                'soil_type':'Well-drained loamy to sandy loam; avoid waterlogging','ph_range':'6.0 – 7.5',
                'yield_per_ha':'20–30 tonnes/ha','market_price':'₹8–45/kg (average ₹15–25/kg)',
                'description':'Onion is a major commercial crop in Tamil Nadu. Erode, Tiruppur and Dindigul are major producing districts. Tamil Nadu is the second largest onion producing state in India.',
                'description_tamil':'வெங்காயம் தமிழ்நாட்டின் முக்கிய வணிக பயிர். ஈரோடு, திருப்பூர் மற்றும் திண்டுக்கல் முக்கிய உற்பத்தி மாவட்டங்கள்.',
                'suitable_districts':'Erode, Tiruppur, Dindigul, Coimbatore, Salem, Namakkal',
                'varieties':[
                    {'name':'CO 4','duration':'110–115 days','yield_info':'28 t/ha','specialty':'Deep red colour, pungent, excellent keeping quality, widely preferred','released_by':'TNAU'},
                    {'name':'Arka Kalyan','duration':'120–130 days','yield_info':'30 t/ha','specialty':'Globe shaped, mild pungency, good for export, late kharif','released_by':'IIHR'},
                    {'name':'Bhima Kiran','duration':'110 days','yield_info':'26 t/ha','specialty':'Light red, attractive appearance, high dry matter, TSS 14–15%','released_by':'DOGR Pune'},
                ],
                'harvest':{
                    'maturity_signs':'50–70% tops fall over naturally. Outer 2–3 leaves turn dry. Bulbs reach full size. Neck softens.',
                    'harvest_method':'Lift bulbs with fork or mechanically. Do not pull by tops — causes neck break and rot. Cure in field for 7–10 days.',
                    'post_harvest':'Cure bulbs in shade for 2–3 weeks to harden outer skins. Top and root trim after curing.',
                    'storage_tips':'Store in well-ventilated ZECC (Zero Energy Cool Chamber) or cold storage at 0–2°C, 65–70% RH. Spread in single or double layer in bamboo/wooden crates.',
                    'best_time':'Harvest in dry weather. Avoid harvesting in wet conditions to prevent rot.',
                    'shelf_life':'2–3 months at room temp; 5–6 months in cold storage'
                },
                'diseases':[
                    {'name':'Purple Blotch','name_tamil':'ஊதா புள்ளி நோய்','severity':'high',
                     'symptoms':'Small white spots with purple centre on leaves and seed stalks. Spots enlarge with yellow halo. Severe infection causes complete leaf dry-up.',
                     'treatment':'Mancozeb 75WP @ 2.5g/L or Iprodione 50WP @ 1g/L. Apply 3–4 sprays at 10-day intervals from 45 days after transplanting.',
                     'prevention':'Crop rotation. Avoid dense planting. Remove infected plant debris. Avoid sprinkler irrigation.'},
                ],
            },
            {
                'name':'Sugarcane','name_tamil':'கரும்பு','emoji':'🎋','category':'cash','season':'annual',
                'duration_days':'10–14 months','water_req':'1500–2500 mm (requires regular irrigation)',
                'temp_range':'24–38°C; needs warm days and cool nights for sugar accumulation',
                'soil_type':'Deep, well-drained loamy soil; pH 6.5–7.5','ph_range':'6.5 – 8.0',
                'yield_per_ha':'80–120 tonnes/ha (ratoon crop 60–80 t/ha)',
                'market_price':'₹280–320 per quintal (State Advised Price)',
                'description':'Sugarcane is the most important cash crop of Tamil Nadu. The state is among the top sugar producers in India. Coimbatore, Erode and Tiruppur are major growing districts.',
                'description_tamil':'கரும்பு தமிழ்நாட்டின் மிக முக்கியமான பண பயிர். கோயம்புத்தூர், ஈரோடு மற்றும் திருப்பூர் முக்கிய சாகுபடி மாவட்டங்கள்.',
                'suitable_districts':'Coimbatore, Erode, Tiruppur, Salem, Vellore, Krishnagiri',
                'varieties':[
                    {'name':'Co 86032','duration':'12 months','yield_info':'100–110 t/ha','specialty':'High sugar content (CCS 12–13%), erect growth, widely adapted','released_by':'SUGARCANE BREEDING INST.'},
                    {'name':'Co 0238','duration':'11–12 months','yield_info':'95–105 t/ha','specialty':'Early maturing, high sucrose, resistant to red rot','released_by':'SBI Coimbatore'},
                    {'name':'CoC 671','duration':'12–13 months','yield_info':'85–95 t/ha','specialty':'Drought tolerant, suitable for drip irrigation, mid-late maturity','released_by':'TNAU/SBI'},
                ],
                'harvest':{
                    'maturity_signs':'Brix% of juice reaches 18–20° (test with refractometer). Canes turn yellow-green. Eye buds on internodes become prominent.',
                    'harvest_method':'Cut at ground level with sharp cane knife or mechanical harvester. Remove trash (dry leaves) before cutting. Top-cutting at last green internode.',
                    'post_harvest':'Deliver to sugar mill within 24 hours of harvest. Delay causes juice quality loss (sucrose inversion).',
                    'storage_tips':'Keep cut canes in shade. Do not stack in sun. Transport same day to mill.',
                    'best_time':'Early morning. Harvest Oct–March for best sugar content.',
                    'shelf_life':'Process within 24–48 hours of cutting'
                },
                'diseases':[
                    {'name':'Red Rot','name_tamil':'சிவப்பு அழுகல் நோய்','severity':'critical',
                     'symptoms':'Reddening of internal cane tissue. White spots with red patches alternating inside stalk. Vinegary/alcohol smell from infected canes. Wilting and drying of upper leaves.',
                     'treatment':'No effective chemical control after infection. Rogue out infected plants immediately. Sett treatment: Carbendazim 50WP 0.1% + Mancozeb 0.25% solution for 30 min before planting.',
                     'prevention':'Use disease-free seed material. Select resistant varieties (CoC 671). Avoid waterlogging. Crop rotation. Collect and burn infected debris.'},
                ],
            },
            {
                'name':'Banana','name_tamil':'வாழை','emoji':'🍌','category':'fruit','season':'annual',
                'duration_days':'11–14 months','water_req':'1200–2200 mm (drip irrigation ideal)',
                'temp_range':'26–30°C optimum; below 12°C causes chilling injury',
                'soil_type':'Deep, well-drained fertile loamy soil with high organic matter','ph_range':'6.0 – 7.5',
                'yield_per_ha':'30–60 tonnes/ha','market_price':'₹12–35/kg',
                'description':'Banana is Tamil Nadu\'s most important fruit crop. The state ranks first in banana production in India. Trichy, Thanjavur, Erode and Dindigul are major growing regions.',
                'description_tamil':'வாழை தமிழ்நாட்டின் மிக முக்கியமான பழ பயிர். தமிழ்நாடு இந்தியாவில் வாழை உற்பத்தியில் முதல் இடம் பிடிக்கிறது.',
                'suitable_districts':'Trichy, Thanjavur, Erode, Dindigul, Coimbatore, Theni',
                'varieties':[
                    {'name':'Rasthali (Silk)','duration':'13–14 months','yield_info':'20–25 t/ha','specialty':'Premium flavour, short fingers, sweet-tangy taste, high market value','released_by':'Traditional variety'},
                    {'name':'Grand Naine (G9)','duration':'11–12 months','yield_info':'55–60 t/ha','specialty':'Export quality Cavendish, uniform bunch, excellent shelf life','released_by':'Tissue culture'},
                    {'name':'Poovan (Mysore)','duration':'13–15 months','yield_info':'18–22 t/ha','specialty':'Disease resistant, excellent taste, popular in local markets','released_by':'Traditional variety'},
                    {'name':'Red Banana','duration':'14–16 months','yield_info':'15–18 t/ha','specialty':'Premium price, unique taste, rich in beta-carotene, export demand','released_by':'Traditional variety'},
                ],
                'harvest':{
                    'maturity_signs':'Angularity of fingers becomes round. Fingers turn from dark green to light green. 75–80 days after bunch emergence. Leaf indicator — 2–3 leaves left on plant.',
                    'harvest_method':'Cut bunch with sharp knife leaving 30–40 cm of stalk. Support bunch to prevent bruising. Handle with care — one person cuts, one holds bunch.',
                    'post_harvest':'Ripen in cool room using ethylene @ 100 ppm at 18°C for 24–48 hours. Grade by finger count and bunch weight.',
                    'storage_tips':'Store green bananas at 13–14°C. Ripened bananas at 12–13°C. Never store below 12°C — chilling injury. Ethylene ripening in sealed room for uniform ripening.',
                    'best_time':'Early morning, avoid afternoon heat.',
                    'shelf_life':'Green: 3–4 weeks at 13°C; Ripe: 5–7 days at room temp'
                },
                'diseases':[
                    {'name':'Panama Wilt (Fusarium Wilt)','name_tamil':'பனாமா வாட்ட நோய்','severity':'critical',
                     'symptoms':'Yellowing starts from outer leaves and progresses inward. Leaves droop and hang down. Brown-purple discoloration inside the pseudostem. Plant wilts and dies before harvest.',
                     'treatment':'No cure once infected. Remove and destroy infected plants including rhizomes. Drench soil with Carbendazim 0.2%. Solarize soil before replanting.',
                     'prevention':'Use resistant varieties (G9, Poovan). Use disease-free tissue-cultured planting material. Avoid movement of soil from infected fields. Long crop rotation (4+ years).'},
                    {'name':'Sigatoka Leaf Spot','name_tamil':'சிகடோகா இலை புள்ளி','severity':'medium',
                     'symptoms':'Small pale yellow streaks on leaves that enlarge into brown oval spots with grey-white centre and dark brown border. Severe defoliation reduces bunch weight.',
                     'treatment':'Propiconazole 25EC @ 1 ml/L or Mancozeb 75WP @ 2.5g/L. Apply 6–8 sprays per season alternating fungicides.',
                     'prevention':'Prune affected leaves. Maintain proper plant spacing. Avoid overhead irrigation. Apply oil-based mineral sprays.'},
                ],
            },
            {
                'name':'Groundnut','name_tamil':'நிலக்கடலை','emoji':'🥜','category':'cash','season':'kharif',
                'duration_days':'90–130 days','water_req':'500–700 mm',
                'temp_range':'25–30°C; warm dry weather at maturity','soil_type':'Well-drained sandy loam; must have good calcium','ph_range':'6.0 – 7.0',
                'yield_per_ha':'1.5–3 tonnes/ha (pod yield)','market_price':'₹55–80/kg',
                'description':'Groundnut is a major oilseed and cash crop in Tamil Nadu. Vellore, Tiruvannamalai, Salem and Dharmapuri are major producing districts. It is grown in both Kharif and Rabi seasons.',
                'description_tamil':'நிலக்கடலை தமிழ்நாட்டின் முக்கிய எண்ணெய் விதை பயிர். வேலூர், திருவண்ணாமலை, சேலம் மாவட்டங்கள் முக்கிய உற்பத்தி பகுதிகள்.',
                'suitable_districts':'Vellore, Tiruvannamalai, Salem, Dharmapuri, Krishnagiri, Cuddalore',
                'varieties':[
                    {'name':'TMV 7','duration':'100–105 days','yield_info':'1800–2000 kg/ha','specialty':'Bold seeded, high oil content 48%, tolerant to tikka leaf spot','released_by':'TNAU'},
                    {'name':'VRI 2','duration':'95–100 days','yield_info':'1900–2100 kg/ha','specialty':'Short duration, resistant to bud necrosis, suitable for summer','released_by':'TNAU'},
                    {'name':'K 6','duration':'110–115 days','yield_info':'2000–2200 kg/ha','specialty':'High shelling percentage 73%, good for oil extraction','released_by':'TNAU'},
                ],
                'harvest':{
                    'maturity_signs':'Inner pod wall turns dark (check by peeling sample pods). 70–75% pods mature. Leaves turn yellow. Test by pressing pod — sounds hollow.',
                    'harvest_method':'Dig plants with hand hoe or mechanical digger. Shake off soil. Windrow for 2–3 days in field. Then stack for further drying.',
                    'post_harvest':'Dry pods to 10% moisture for storage or 8% for seed. Thresh by hand beating or thresher.',
                    'storage_tips':'Store in jute bags or bins at cool, dry place. Maintain 8–9% moisture. Treat with sulphur dust to prevent aflatoxin. Do not store wet pods.',
                    'best_time':'Harvest in dry weather — wet conditions cause aflatoxin contamination.',
                    'shelf_life':'6–8 months with 8% moisture in dry storage'
                },
                'diseases':[
                    {'name':'Tikka Leaf Spot (Early & Late Blight)','name_tamil':'டிக்கா இலை புள்ளி நோய்','severity':'high',
                     'symptoms':'Small circular brown spots on leaflets. Early blight: brown spots with yellow halo. Late blight: dark brown spots without yellow ring. Defoliation in severe cases.',
                     'treatment':'Mancozeb 75WP @ 2.5g/L or Chlorothalonil 75WP @ 2g/L. 3–4 sprays at 10–14 day intervals from 30 days after sowing.',
                     'prevention':'Use resistant varieties. Crop rotation. Avoid excess irrigation. Remove and burn infected crop debris.'},
                ],
            },
            {
                'name':'Turmeric','name_tamil':'மஞ்சள்','emoji':'🟡','category':'spice','season':'kharif',
                'duration_days':'210–270 days','water_req':'1500–2250 mm',
                'temp_range':'20–30°C; warm humid climate preferred','soil_type':'Well-drained loamy soil rich in organic matter; avoid waterlogging','ph_range':'5.5 – 7.0',
                'yield_per_ha':'20–30 tonnes/ha fresh rhizomes (5–7 t/ha dry)','market_price':'₹100–180/kg (dry)',
                'description':'Erode turmeric is world-famous for its high curcumin content. Tamil Nadu produces about 35% of India\'s turmeric. Erode, Nilgiris and Salem are major growing areas.',
                'description_tamil':'ஈரோடு மஞ்சள் அதன் அதிக குர்குமின் உள்ளடக்கத்திற்காக உலகப் புகழ் பெற்றது. தமிழ்நாடு இந்தியாவின் மஞ்சள் உற்பத்தியில் சுமார் 35% உற்பத்தி செய்கிறது.',
                'suitable_districts':'Erode, Salem, Nilgiris, Coimbatore, Tiruppur, Dindigul',
                'varieties':[
                    {'name':'BSR 1 (Erode Local)','duration':'270 days','yield_info':'30–35 t/ha fresh','specialty':'Very high curcumin (6–7%), bright yellow colour, Erode market premium','released_by':'TNAU'},
                    {'name':'CO 2','duration':'240 days','yield_info':'28 t/ha fresh','specialty':'Early maturing, medium curcumin, suitable for both fresh and dry','released_by':'TNAU Coimbatore'},
                    {'name':'Salem','duration':'255 days','yield_info':'22–25 t/ha fresh','specialty':'Long fingers, golden yellow after curing, moderate curcumin','released_by':'Traditional'},
                ],
                'harvest':{
                    'maturity_signs':'Leaves turn yellow and dry. Pseudostems fall. Rhizomes when dug show fully developed fingers. Skin becomes rough.',
                    'harvest_method':'Dig with spade or country plough. Pull out rhizomes carefully. Separate seed rhizomes (mother) from finger rhizomes for next planting.',
                    'post_harvest':'Boiling (curing): Boil fresh rhizomes in water for 45–60 min until soft. Dry in sun for 10–15 days. Polish to get smooth finish.',
                    'storage_tips':'Store dried turmeric in jute bags in cool, dry, well-ventilated store. Protect from moisture (absorbs moisture easily). Fumigate storage against insects.',
                    'best_time':'January to March depending on variety.',
                    'shelf_life':'12–18 months as dry turmeric powder; 24+ months as whole fingers'
                },
                'diseases':[
                    {'name':'Rhizome Rot (Pythium)','name_tamil':'கிழங்கு அழுகல் நோய்','severity':'critical',
                     'symptoms':'Yellowing and wilting of leaves from lower portion. Collar region near soil shows brown-black water-soaked lesions. Rhizomes become soft and rotten with foul smell.',
                     'treatment':'Drench soil with Metalaxyl 8% + Mancozeb 64% WP @ 3g/L. Treat seed rhizomes with Trichoderma @ 10g/kg before planting.',
                     'prevention':'Avoid waterlogging — provide drainage. Use healthy seed rhizomes. Treat with Trichoderma viride. Crop rotation with cereals.'},
                ],
            },
        ]

        for cd in crops_data:
            crop = Crop.objects.create(
                name=cd['name'], name_tamil=cd['name_tamil'], emoji=cd['emoji'],
                category=cd['category'], season=cd['season'], duration_days=cd['duration_days'],
                water_req=cd['water_req'], temp_range=cd['temp_range'], soil_type=cd['soil_type'],
                ph_range=cd['ph_range'], yield_per_ha=cd['yield_per_ha'], market_price=cd['market_price'],
                description=cd['description'], description_tamil=cd.get('description_tamil',''),
                suitable_districts=cd.get('suitable_districts',''),
            )
            for v in cd.get('varieties',[]):
                CropVariety.objects.create(crop=crop, **v)
            h = cd.get('harvest',{})
            if h:
                HarvestingGuide.objects.create(crop=crop, **h)
            for d in cd.get('diseases',[]):
                CropDisease.objects.create(crop=crop, **d)

        self.stdout.write(f'  ✅ {len(crops_data)} crops seeded')

    def _fertilizers(self):
        Fertilizer.objects.all().delete()
        data = [
            {'name':'Urea','name_tamil':'யூரியா','emoji':'⚗️','ftype':'inorganic','npk_ratio':'46-0-0',
             'dosage':'120–150 kg/ha for paddy; 60–80 kg/ha for vegetables. Split in 2–3 doses.',
             'suitable_crops':'All crops especially paddy, maize, sugarcane, vegetables',
             'application':'Broadcast or band placement at basal, tillering and panicle initiation stages. Avoid applying before rain to prevent leaching.',
             'benefits':'Fast acting nitrogen source. Promotes lush vegetative growth, deep green colour, and high yield. Most economical N fertilizer.',
             'price_range':'₹266/bag (45 kg) — subsidised rate'},
            {'name':'DAP (Di-Ammonium Phosphate)','name_tamil':'டி.ஏ.பி','emoji':'🔵','ftype':'inorganic','npk_ratio':'18-46-0',
             'dosage':'100–125 kg/ha as basal dose. Apply before transplanting/sowing.',
             'suitable_crops':'Paddy, wheat, pulses, oilseeds, vegetables at basal application',
             'application':'Mix into soil during last ploughing as basal dose. Do not mix with urea directly — ammonium loss.',
             'benefits':'Supplies both nitrogen and phosphorus at planting. Promotes root development, early establishment and flowering.',
             'price_range':'₹1350/bag (50 kg) — subsidised rate'},
            {'name':'MOP (Muriate of Potash)','name_tamil':'பொட்டாஷ்','emoji':'🟠','ftype':'inorganic','npk_ratio':'0-0-60',
             'dosage':'50–80 kg/ha. Apply as basal or first split. Avoid in saline soils.',
             'suitable_crops':'Potato, banana, sugarcane, tomato, all tuber and fruit crops',
             'application':'Mix into soil before planting. Can be applied as top-dress at 30 days.',
             'benefits':'Improves fruit quality, disease resistance, drought tolerance and shelf life. Essential for starch and sugar synthesis.',
             'price_range':'₹1700/bag (50 kg) — subsidised rate'},
            {'name':'Vermicompost','name_tamil':'மண்புழு உரம்','emoji':'🪱','ftype':'organic','npk_ratio':'1.5-0.5-1.0 + micronutrients',
             'dosage':'2–4 tonnes/ha as basal. Excellent when mixed into transplanting holes.',
             'suitable_crops':'All crops — especially vegetables, fruit crops, flowers, nursery plants',
             'application':'Apply in furrows or mix into top 15cm soil. Use as pit filling for perennial crops.',
             'benefits':'Improves soil structure, water holding capacity, microbial activity. Slow release nutrition. Makes plant disease resistant naturally.',
             'price_range':'₹6–10/kg'},
            {'name':'FYM (Farmyard Manure)','name_tamil':'தொழு உரம்','emoji':'🌿','ftype':'organic','npk_ratio':'0.5-0.25-0.5',
             'dosage':'10–25 tonnes/ha. Well decomposed FYM for best results.',
             'suitable_crops':'All crops, especially beneficial for light sandy soils',
             'application':'Apply and incorporate into soil 3–4 weeks before planting to allow decomposition.',
             'benefits':'Improves soil structure, provides humus, feeds soil microorganisms, improves drainage in clay soils and water retention in sandy soils.',
             'price_range':'₹500–1500/tonne'},
            {'name':'Neem Cake','name_tamil':'வேப்பம் புண்ணாக்கு','emoji':'🌱','ftype':'organic','npk_ratio':'5-1-1.5 + azadirachtin',
             'dosage':'200–400 kg/ha as basal. Mix into soil before planting.',
             'suitable_crops':'Vegetables, paddy, turmeric, groundnut — excellent for soil pest control',
             'application':'Apply in furrows or broadcast and incorporate before transplanting. Also used as nursery medium amendment.',
             'benefits':'Suppresses soil-borne pests and nematodes. Nitrification inhibitor — slows urea breakdown. Natural insect repellent.',
             'price_range':'₹12–18/kg'},
            {'name':'Rhizobium (Bio-fertilizer)','name_tamil':'ரைசோபியம் உயிர் உரம்','emoji':'🦠','ftype':'bio','npk_ratio':'Nitrogen fixation 20–30 kg N/ha',
             'dosage':'Seed treatment: 200g culture + 200ml water per 10 kg seed. Soil application: 2 kg culture + 25 kg FYM/ha.',
             'suitable_crops':'All leguminous crops: Groundnut, green gram, black gram, soybean, cowpea, chickpea',
             'application':'Mix culture with seeds just before sowing in shade. Dry briefly. Do not expose to direct sunlight. Do not mix with fungicides.',
             'benefits':'Fixes atmospheric nitrogen — saves 25–30 kg N/ha (equal to 60 kg urea). Increases yield 15–20%. Cost-effective. Eco-friendly.',
             'price_range':'₹40–60/packet (200g)'},
            {'name':'NPK 19:19:19','name_tamil':'NPK 19:19:19','emoji':'🧪','ftype':'npk','npk_ratio':'19-19-19',
             'dosage':'3–5 g/L water for foliar spray. 150–200 kg/ha for soil application.',
             'suitable_crops':'All crops — especially for foliar feeding in deficient conditions',
             'application':'Foliar spray in early morning or evening. Soil application through drip irrigation or fertigation.',
             'benefits':'Balanced nutrition in single product. Quick correction of NPK deficiencies. Highly soluble — ideal for fertigation in drip-irrigated crops.',
             'price_range':'₹80–120/kg'},
        ]
        for d in data:
            Fertilizer.objects.create(**d)
        self.stdout.write(f'  ✅ {len(data)} fertilizers seeded')

    def _pesticides(self):
        Pesticide.objects.all().delete()
        data = [
            {'name':'Chlorpyrifos 20EC','emoji':'🛡️','ptype':'insecticide','is_organic':False,
             'active_ingredient':'Chlorpyrifos 20% EC',
             'target_pests':'Stem borer in paddy, cutworm, aphids, white grub, termites, leaf miner',
             'dosage':'2.5 ml/L water for foliar spray; 3–4 L/ha for soil drenching',
             'safety_interval':'15 days before harvest (PHI)',
             'precautions':'Wear full PPE — gloves, mask, goggles. Highly toxic to fish and aquatic organisms. Do not spray near water bodies. Avoid during flowering — harmful to bees.'},
            {'name':'Lambda-Cyhalothrin 5EC','emoji':'⚔️','ptype':'insecticide','is_organic':False,
             'active_ingredient':'Lambda-Cyhalothrin 5% EC',
             'target_pests':'Bollworm, pod borer, aphids, thrips, whitefly, leaf eating caterpillars',
             'dosage':'0.5–0.75 ml/L water for foliar spray',
             'safety_interval':'7 days before harvest',
             'precautions':'Wear PPE. Highly toxic to fish and beneficial insects. Do not apply near flowering crops. Rotate with other chemical groups to prevent resistance.'},
            {'name':'Mancozeb 75WP','emoji':'🍄','ptype':'fungicide','is_organic':False,
             'active_ingredient':'Mancozeb 75% WP (Dithiocarbamate group)',
             'target_pests':'Early blight, late blight, leaf spot, downy mildew, anthracnose, rust diseases',
             'dosage':'2.5 g/L water. Apply 3–5 sprays at 7–10 day intervals',
             'safety_interval':'7 days before harvest',
             'precautions':'Wear mask during mixing — fine dust. Avoid skin contact. Do not mix with copper-based fungicides. Rotate with systemic fungicides to prevent resistance.'},
            {'name':'Copper Hydroxide 77WP','emoji':'🔵','ptype':'fungicide','is_organic':False,
             'active_ingredient':'Copper Hydroxide 77% WP',
             'target_pests':'Bacterial blight, leaf spot, downy mildew, citrus canker, fire blight',
             'dosage':'3 g/L water. Spray thoroughly to cover all leaf surfaces',
             'safety_interval':'7 days before harvest',
             'precautions':'Avoid repeated use — causes copper toxicity in soil. Do not mix with lime. Not compatible with EDTA-based pesticides. Wear gloves — skin irritant.'},
            {'name':'Imidacloprid 17.8SL','emoji':'🐜','ptype':'insecticide','is_organic':False,
             'active_ingredient':'Imidacloprid 17.8% SL (Neonicotinoid)',
             'target_pests':'Brown plant hopper, whitefly, aphids, jassids, mealybug, thrips',
             'dosage':'0.25–0.3 ml/L for foliar; 250–300 ml/ha for soil application',
             'safety_interval':'21 days before harvest',
             'precautions':'HIGHLY TOXIC TO BEES — do not apply during flowering. Systemic action through plant. Wear full PPE. Toxic to soil organisms. Use as seed treatment for best results.'},
            {'name':'Neem Oil 1500ppm','emoji':'🌿','ptype':'insecticide','is_organic':True,
             'active_ingredient':'Azadirachtin 1500 ppm from Azadirachta indica',
             'target_pests':'Aphids, whiteflies, mites, thrips, leaf miners, fungus gnats, caterpillars (IGR action)',
             'dosage':'5 ml/L water + 1 ml liquid soap (as emulsifier). Spray under leaves.',
             'safety_interval':'0 days — safe to harvest same day',
             'precautions':'Completely safe for humans, birds, mammals. Harmful to fish in large quantities. Best applied in evening — UV degrades it. Shake well before use. Reapply every 5–7 days.'},
            {'name':'Trichoderma viride (Bio-fungicide)','emoji':'🦠','ptype':'fungicide','is_organic':True,
             'active_ingredient':'Trichoderma viride 1.5% WP (viable spores 2×10⁶ CFU/g)',
             'target_pests':'Damping off, root rot, wilt (Fusarium, Pythium, Phytophthora, Sclerotinia)',
             'dosage':'Seed treatment: 4g/kg seed. Soil application: 2.5 kg/ha mixed with 50 kg FYM.',
             'safety_interval':'0 days — completely safe',
             'precautions':'Do not mix with chemical fungicides or antibiotics — kills beneficial fungus. Store at cool temperature below 30°C away from sunlight. Use before expiry.'},
            {'name':'Glyphosate 41SL','emoji':'🌾','ptype':'herbicide','is_organic':False,
             'active_ingredient':'Glyphosate Isopropylamine Salt 41% SL',
             'target_pests':'All annual and perennial weeds — especially grasses, sedges, broadleaf weeds',
             'dosage':'1.6–2.0 L/ha in 200L water. Apply on actively growing green weeds.',
             'safety_interval':'Do not spray on or near crops — non-selective, kills all plants',
             'precautions':'NON-SELECTIVE — kills all vegetation. Never spray on crops. Apply only on weeds in field bunds, roadsides, fallow fields. Use blue-dye nozzle guard. Wear full PPE. Avoid spray drift.'},
        ]
        for d in data:
            Pesticide.objects.create(**d)
        self.stdout.write(f'  ✅ {len(data)} pesticides seeded')

    def _mandi(self):
        MandiPrice.objects.all().delete()
        from datetime import date
        data = [
            ('Tomato','🍅','Salem',35,55,42,'kg','up'),
            ('Onion','🧅','Erode',20,38,28,'kg','down'),
            ('Paddy (Raw)','🌾','Thanjavur',1850,2050,1950,'quintal','stable'),
            ('Sugarcane','🎋','Coimbatore',280,320,295,'quintal','up'),
            ('Banana','🍌','Trichy',15,30,22,'kg','stable'),
            ('Groundnut','🥜','Vellore',55,75,65,'kg','up'),
            ('Turmeric','🟡','Erode',100,150,128,'kg','up'),
            ('Chilli (Dry)','🌶️','Madurai',85,130,110,'kg','down'),
            ('Green Gram','🫘','Namakkal',80,105,92,'kg','up'),
            ('Coconut','🥥','Coimbatore',25,38,30,'piece','stable'),
        ]
        for d in data:
            MandiPrice.objects.create(
                crop_name=d[0],emoji=d[1],district=d[2],
                min_price=d[3],max_price=d[4],modal_price=d[5],
                unit=d[6],trend=d[7])
        self.stdout.write(f'  ✅ {len(data)} mandi prices seeded')

    def _loans(self):
        LoanScheme.objects.all().delete()
        data = [
            {'name':'KCC','full_name':'Kisan Credit Card','emoji':'💳',
             'min_amount':'₹10,000','max_amount':'₹3,00,000+',
             'interest_rate':'7% per annum (2% subvention = effective 5%)',
             'repayment':'Within 12 months (crop loan). Term loan up to 5 years.',
             'eligibility':'All farmers — small, marginal, tenant farmers, SHG members. Valid land documents required.',
             'documents':'Land records (Patta/Chitta), identity proof, photo, bank passbook',
             'benefits':'Flexible ATM withdrawals, insurance coverage, crop insurance included, no collateral up to ₹1.6 lakh',
             'how_to_apply':'Apply at nearest SBI/Nationalised bank/Co-operative bank branch with land documents. Online at KCC portal or PM-Kisan portal.'},
            {'name':'PM-Kisan','full_name':'Pradhan Mantri Kisan Samman Nidhi','emoji':'🏛️',
             'min_amount':'₹2,000 (per installment)','max_amount':'₹6,000/year (3 installments)',
             'interest_rate':'Direct benefit — no interest',
             'repayment':'No repayment — direct benefit transfer',
             'eligibility':'All landholding farmers. Excludes institutional landholders, government employees, income tax payers above ₹10,000/month.',
             'documents':'Aadhaar card, bank account linked to Aadhaar, land records',
             'benefits':'₹6,000/year direct to bank account in 3 installments of ₹2,000. No need to visit bank.',
             'how_to_apply':'Register at pmkisan.gov.in or through Common Service Centre (CSC). Aadhaar must be linked to bank account.'},
            {'name':'PMFBY','full_name':'Pradhan Mantri Fasal Bima Yojana','emoji':'🛡️',
             'min_amount':'Full crop value insured','max_amount':'Based on area and crop value',
             'interest_rate':'Premium: 2% for Kharif, 1.5% for Rabi, 5% for horticulture',
             'repayment':'No repayment — insurance scheme',
             'eligibility':'All farmers growing notified crops. Both loanee and non-loanee farmers eligible.',
             'documents':'Land records, bank account, Aadhaar, sowing certificate',
             'benefits':'Full crop value compensated for losses due to natural calamities, pests, diseases. Covers sowing to post-harvest losses.',
             'how_to_apply':'Apply through bank where KCC loan taken, or at Agriculture Department office before cut-off date. Online at pmfby.gov.in'},
            {'name':'NABARD TL','full_name':'NABARD Farm Mechanisation Term Loan','emoji':'🚜',
             'min_amount':'₹50,000','max_amount':'₹25 lakh',
             'interest_rate':'9–12% depending on bank and purpose',
             'repayment':'3–7 years with 6–12 months moratorium',
             'eligibility':'Individual farmers, farmer groups, FPOs for purchasing tractors, power tillers, threshers, irrigation equipment',
             'documents':'Land records, quotation from equipment supplier, income proof, bank statements',
             'benefits':'Subsidy available: SC/ST farmers 50%, General 25% under SMAM scheme. Low down payment.',
             'how_to_apply':'Apply at Commercial banks, RRBs, Co-operative banks. NABARD refinances these loans. Submit dealer quotation with application.'},
        ]
        for d in data:
            LoanScheme.objects.create(**d)
        self.stdout.write(f'  ✅ {len(data)} loan schemes seeded')

    def _learn(self):
        LearnContent.objects.all().delete()
        data = [
            {'title':'Drip Irrigation Setup Guide','title_tamil':'நீர்த்துளி பாசன அமைப்பு வழிகாட்டி','ctype':'guide','category':'Irrigation','duration':'45 min read','difficulty':'beginner','emoji':'💧','description':'Complete guide to setting up drip irrigation for vegetable and fruit crops. Covers laterals, drippers, pressure regulation and maintenance.'},
            {'title':'Organic Pest Management','title_tamil':'இயற்கை பூச்சி மேலாண்மை','ctype':'article','category':'Pest Management','duration':'20 min read','difficulty':'beginner','emoji':'🌿','description':'Natural methods to control pests using neem oil, neem cake, yellow sticky traps, biopesticides and companion planting without chemicals.'},
            {'title':'Soil Testing & Interpretation','title_tamil':'மண் பரிசோதனை & விளக்கம்','ctype':'guide','category':'Soil Science','duration':'30 min read','difficulty':'intermediate','emoji':'🧪','description':'How to collect soil samples, send to lab, read the report and apply correct fertilizers based on soil test results.'},
            {'title':'PM-Kisan & KCC Application Process','title_tamil':'PM-கிசான் & KCC விண்ணப்ப வழிமுறை','ctype':'guide','category':'Government Schemes','duration':'15 min read','difficulty':'beginner','emoji':'🏛️','description':'Step-by-step process to register for PM-Kisan ₹6000/year benefit and apply for Kisan Credit Card with 5% interest rate.'},
            {'title':'Paddy Integrated Pest Management','title_tamil':'நெல் ஒருங்கிணைந்த பூச்சி மேலாண்மை','ctype':'article','category':'Crop Protection','duration':'35 min read','difficulty':'intermediate','emoji':'🌾','description':'IPM practices for paddy — BPH monitoring, light traps, pheromone traps, biological control and chemical last resort approach.'},
            {'title':'Vegetable Nursery Raising','title_tamil':'காய்கறி நாற்றங்கால் அமைத்தல்','ctype':'guide','category':'Horticulture','duration':'25 min read','difficulty':'beginner','emoji':'🌱','description':'How to raise healthy tomato, brinjal, chilli and gourd seedlings in pro-trays with coco peat media for better survival rate.'},
        ]
        for d in data:
            LearnContent.objects.create(**d)
        self.stdout.write(f'  ✅ {len(data)} learn contents seeded')
