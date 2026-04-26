from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from .models import *
import json, decimal
from datetime import date, timedelta


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def _features():
    return [
        {'icon':'🛒','name':'FarmConnect',  'url':'/marketplace/','bg':'#dcfce7','desc_en':'Buy & sell farm produce directly','desc_ta':'நேரடியாக பண்ணை விளைபொருட்களை வாங்கவும் விற்கவும்'},
        {'icon':'🔬','name':'CropDoc',      'url':'/crop-doc/','bg':'#fff7ed','desc_en':'AI crop disease detection','desc_ta':'AI மூலம் பயிர் நோய் கண்டறிதல்'},
        {'icon':'📊','name':'LiveMandi',    'url':'/mandi/','bg':'#eff6ff','desc_en':'Real-time market prices','desc_ta':'நேரலை சந்தை விலைகள்'},
        {'icon':'🌦️','name':'AgroWeather',  'url':'/weather/','bg':'#f0f9ff','desc_en':'Hyper-local farm weather','desc_ta':'விவசாயிகளுக்கான வானிலை அறிக்கை'},
        {'icon':'🏦','name':'FarmLoan',     'url':'/loan/','bg':'#fefce8','desc_en':'Government schemes & loans','desc_ta':'அரசு திட்டங்கள் மற்றும் கடன்கள்'},
        {'icon':'📔','name':'KisanDiary',   'url':'/diary/','bg':'#fdf4ff','desc_en':'Farm income & expense tracker','desc_ta':'வருமானம் மற்றும் செலவு கணக்கு'},
        {'icon':'🎓','name':'AgriLearn',    'url':'/learn/','bg':'#fff1f2','desc_en':'Farming tutorials & guides','desc_ta':'விவசாய பயிற்சி வழிகாட்டிகள்'},
        {'icon':'🧪','name':'SoilDoc',      'url':'/soil/','bg':'#f7fee7','desc_en':'Soil health analysis tool','desc_ta':'மண் ஆரோக்கிய பகுப்பாய்வு'},
        {'icon':'🚜','name':'RentFarm',     'url':'/rent/','bg':'#fff8f0','desc_en':'Rent tractors & equipment','desc_ta':'டிராக்டர் மற்றும் இயந்திரங்கள் வாடகைக்கு'},
    ]

def _ctx(request, **kwargs):
    ctx = {'features': _features(), 'user_name': request.session.get('user_name',''), 'user_role': request.session.get('user_role','')}
    ctx.update(kwargs)
    return ctx


# ─────────────────────────────────────────────
# PUBLIC VIEWS
# ─────────────────────────────────────────────
def home(request):
    return render(request, 'home.html', _ctx(request))

def login_view(request):
    if request.session.get('user_id'):
        return redirect('/')
    error = None
    if request.method == 'POST':
        uname = request.POST.get('username','').strip()
        pwd   = request.POST.get('password','')
        user  = authenticate(request, username=uname, password=pwd)
        if user:
            login(request, user)
            request.session['user_id']   = user.id
            request.session['user_name'] = user.get_full_name() or user.username
            request.session['user_role'] = user.role
            nxt = request.GET.get('next','/')
            return redirect(nxt)
        else:
            error = 'Invalid username or password. Please try again.'
    return render(request, 'login.html', {'error': error})

def register_view(request):
    if request.session.get('user_id'):
        return redirect('/')
    error = None
    if request.method == 'POST':
        p = request.POST
        if p.get('password') != p.get('confirm_password'):
            error = 'Passwords do not match!'
        elif User.objects.filter(username=p.get('phone','')).exists():
            error = 'Mobile number already registered. Please login.'
        else:
            try:
                user = User.objects.create_user(
                    username   = p.get('phone',''),
                    password   = p.get('password',''),
                    first_name = p.get('first_name',''),
                    last_name  = p.get('last_name',''),
                    phone      = p.get('phone',''),
                    role       = p.get('role','farmer'),
                    district   = p.get('district',''),
                    land_area  = p.get('land_area') or None,
                )
                login(request, user)
                request.session['user_id']   = user.id
                request.session['user_name'] = user.get_full_name() or user.username
                request.session['user_role'] = user.role
                return redirect('/')
            except Exception as e:
                error = f'Registration error: {e}'
    return render(request, 'register.html', {'error': error})

def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('/login/')


# ─────────────────────────────────────────────
# LOGIN REQUIRED VIEWS
# ─────────────────────────────────────────────
@login_required
def crops(request):
    crop_list = Crop.objects.all().order_by('category','name')
    category  = request.GET.get('cat','')
    if category:
        crop_list = crop_list.filter(category=category)
    return render(request, 'crops.html', _ctx(request, crops=crop_list, active_cat=category))

@login_required
def crop_detail(request, pk):
    crop       = get_object_or_404(Crop, pk=pk)
    varieties  = crop.varieties.all()
    harvest    = getattr(crop, 'harvest', None)
    diseases   = crop.diseases.all()
    other_crops = Crop.objects.exclude(pk=pk)[:6]
    return render(request, 'crop_detail.html', _ctx(request,
        crop=crop, varieties=varieties, harvest=harvest,
        diseases=diseases, other_crops=other_crops))

@login_required
def fertilizer(request):
    ftype = request.GET.get('type','')
    ferts = Fertilizer.objects.all()
    if ftype:
        ferts = ferts.filter(ftype=ftype)
    return render(request, 'fertilizer.html', _ctx(request, fertilizers=ferts, active_type=ftype))

@login_required
def pesticide(request):
    ptype = request.GET.get('type','')
    pests = Pesticide.objects.all()
    if ptype:
        pests = pests.filter(ptype=ptype)
    return render(request, 'pesticide.html', _ctx(request, pesticides=pests, active_type=ptype))

@login_required
def marketplace(request):
    from .models import MandiPrice
    prices = MandiPrice.objects.all()[:20]
    return render(request, 'marketplace.html', _ctx(request, prices=prices))

@login_required
def crop_doc(request):
    crops_list = Crop.objects.all()
    result     = None
    if request.method == 'POST':
        crop_id  = request.POST.get('crop_id')
        symptoms = request.POST.get('symptoms','').lower()
        if crop_id:
            crop = get_object_or_404(Crop, pk=crop_id)
            diseases = crop.diseases.all()
            result = {'crop': crop, 'diseases': diseases, 'symptoms': symptoms}
    return render(request, 'crop_doc.html', _ctx(request, crops_list=crops_list, result=result))

@login_required
def mandi(request):
    prices = MandiPrice.objects.all().order_by('-date','crop_name')
    if not prices.exists():
        prices = _demo_mandi()
    return render(request, 'mandi.html', _ctx(request, prices=prices))

@login_required
def weather(request):
    return render(request, 'weather.html', _ctx(request))

@login_required
def loan(request):
    schemes = LoanScheme.objects.all()
    return render(request, 'loan.html', _ctx(request, schemes=schemes))

@login_required
def diary(request):
    user    = request.user
    entries = FarmDiary.objects.filter(user=user).order_by('-date')
    income  = entries.filter(dtype='income').aggregate(t=Sum('amount'))['t'] or 0
    expense = entries.filter(dtype='expense').aggregate(t=Sum('amount'))['t'] or 0
    profit  = income - expense
    error   = None
    if request.method == 'POST':
        try:
            FarmDiary.objects.create(
                user       = user,
                date       = request.POST.get('date', date.today()),
                dtype      = request.POST.get('dtype','income'),
                category   = request.POST.get('category',''),
                amount     = decimal.Decimal(request.POST.get('amount','0')),
                description= request.POST.get('description',''),
            )
        except Exception as e:
            error = str(e)
    return render(request, 'diary.html', _ctx(request,
        entries=entries, income=income, expense=expense, profit=profit, error=error))

@login_required
def learn(request):
    content = LearnContent.objects.all()
    ctype   = request.GET.get('type','')
    if ctype:
        content = content.filter(ctype=ctype)
    return render(request, 'learn.html', _ctx(request, content=content, active_type=ctype))

@login_required
def soil(request):
    return render(request, 'soil.html', _ctx(request))

@login_required
def rent(request):
    return render(request, 'rent.html', _ctx(request))

# Demo fallback for mandi
def _demo_mandi():
    data = [
        {'crop_name':'Tomato','emoji':'🍅','district':'Salem','min_price':35,'max_price':55,'modal_price':42,'trend':'up'},
        {'crop_name':'Onion','emoji':'🧅','district':'Erode','min_price':20,'max_price':38,'modal_price':28,'trend':'down'},
        {'crop_name':'Paddy (Raw)','emoji':'🌾','district':'Thanjavur','min_price':1850,'max_price':2050,'modal_price':1950,'unit':'quintal','trend':'stable'},
        {'crop_name':'Sugarcane','emoji':'🎋','district':'Coimbatore','min_price':280,'max_price':320,'modal_price':295,'unit':'quintal','trend':'up'},
        {'crop_name':'Banana','emoji':'🍌','district':'Trichy','min_price':15,'max_price':30,'modal_price':22,'trend':'stable'},
        {'crop_name':'Groundnut','emoji':'🥜','district':'Vellore','min_price':55,'max_price':75,'modal_price':65,'trend':'up'},
        {'crop_name':'Turmeric','emoji':'🟡','district':'Erode','min_price':100,'max_price':150,'modal_price':128,'trend':'up'},
        {'crop_name':'Chilli (Dry)','emoji':'🌶️','district':'Madurai','min_price':85,'max_price':130,'modal_price':110,'trend':'down'},
    ]
    class MP:
        def __init__(self,d):
            for k,v in d.items(): setattr(self,k,v)
            if not hasattr(self,'unit'): self.unit='kg'
    return [MP(d) for d in data]
