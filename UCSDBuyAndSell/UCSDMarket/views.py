from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.templatetags.static import static
from UCSDMarket.forms import SignupForm, CreateListingForm
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from UCSDBuyAndSell.tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from UCSDMarket.models import Picture, Listing, Favorite
from django.db.models import Q
from django.http import HttpResponse
from decimal import Decimal

# Create your views here.
def Home(request):
    if request.user.is_authenticated:
        return redirect("MyListings")
    else:
        return render(request, 'UCSDMarket/home.html')

def Signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            if not username.endswith('ucsd.edu'):
                form.add_error('username', "Email doesn't end with ucsd.edu")
                return render(request, 'UCSDMarket/signup.html', {'form': form})
            raw_password = form.cleaned_data.get('password1')
            compare_password = form.cleaned_data.get('password2')
            if raw_password != compare_password:
                form.add_error('compare_password', "Password does not match")
                return render(request, 'UCSDMarket/signup.html', {'form': form})
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your UCSD Market account.'
            message = render_to_string('UCSDMarket/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('username')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'UCSDMarket/signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

def Signoff(request):
    logout(request)
    response = redirect('/market/login')
    return response

def ListingPage(request):
    if request.method=='GET':
        listingID = request.GET.get('listing')
        if not listingID:
            return render(request, 'UCSDMarket/home.html')
        else:
            ThisListing = Listing.objects.filter(id=int(listingID))
            if (len(ThisListing) == 1):
                ThisListing = ThisListing[0]

                images = Picture.objects.filter(listingKey=ThisListing)
                imgCount = 0
                all_pictures = []
                for image in images:
                    imgCount = imgCount + 1
                    all_pictures.append({
                                        "id": image.id,
                                        "Image": image.picture.url,
                                        "Number": imgCount
                                        })

                Favd = False
                if request.user.is_authenticated and Favorite.objects.filter(user=request.user, listingKey=ThisListing.id).exists():
                    Favd = True

                context = {
                    "id" : ThisListing.id,
                    "Title" : ThisListing.title,
                    "Seller" : ThisListing.user.username,
                    "Price" : ThisListing.Price,
                    "CanDeliver" : ThisListing.canDeliver,
                    "Condition" : ThisListing.condition,
                    "Description" : ThisListing.description,
                    "ContactInformation" : ThisListing.contactInformation,
                    "Pictures": all_pictures,
                    "Favd": Favd,
                    "isOwner": ThisListing.user == request.user
                }
                return render(request, "UCSDMarket/listing.html", context)
            else:
                #Something has gone wrong!
                return render(request, 'UCSDMarket/home.html')

def MyListings(request):

    if request.user.is_authenticated:
        # Get listings from user
        MyListings = Listing.objects.filter(user=request.user)
        Listings = []

        for post in MyListings:
            all_images = Picture.objects.filter(listingKey=post)
            if not all_images:
                thumbImg = static('img/NoImage.png')
            else:
                thumbImg = all_images[0].picture.url
            Listings.append({
                "id" : post.id,
                "Title" : post.title,
                "Seller" : post.user.username,
                "Price" : post.Price,
                "CanDeliver" : post.canDeliver,
                "Condition" : post.condition,
                "Description" : post.description,
                "ContactInformation" : post.contactInformation,
                "Thumbnail": thumbImg
            })

        context = {
            "Listings" : Listings,
        }
        return render(request, "UCSDMarket/my_listings.html", context)
    else:
        return render(request, "UCSDMarket/home.html")

def Favorites(request):
    if request.user.is_authenticated:
        # Get listings from user
        Favorites = Favorite.objects.filter(user=request.user)
        Listings = []

        for FavPost in Favorites:
            post = FavPost.listingKey
            all_images = Picture.objects.filter(listingKey=post)
            if not all_images:
                thumbImg = static('img/NoImage.png')
            else:
                thumbImg = all_images[0].picture.url
            Favd = False
            if request.user.is_authenticated and Favorite.objects.filter(user=request.user, listingKey=post.id).exists():
                Favd = True
            Listings.append({
                "id" : post.id,
                "Title" : post.title,
                "Seller" : post.user.username,
                "Price" : post.Price,
                "CanDeliver" : post.canDeliver,
                "Condition" : post.condition,
                "Description" : post.description,
                "ContactInformation" : post.contactInformation,
                "Thumbnail": thumbImg,
				"Favd": Favd
            })

        context = {
            "Listings" : Listings,
        }
        return render(request, "UCSDMarket/favorites.html", context)
    else:
        return render(request, "UCSDMarket/home.html")

@login_required
def Like(request):
	listing_id = None
	if request.method == 'GET':
		listing_id = request.GET['listing_id']
	
	listing = Listing.objects.get(id=listing_id)
	if Favorite.objects.filter(user=request.user, listingKey=listing).exists():
		Favorite.objects.filter(user=request.user, listingKey=listing).delete()
	else:
		Favorite.objects.create(user=request.user, listingKey=listing)
	return render(request, "UCSDMarket/home.html")

def DeleteUser(request):
	if request.user.is_authenticated:
		try:
			currUserName = request.user.username
			logout(request)
			u = User.objects.get(username = currUserName)
			u.delete()
			messages.success(request, "Current User Deleted")
			return render(request, 'UCSDMarket/home.html')
		except Exception as e:
			messages.error(request, "Issue has occured while attempting to delete User. Contact support.")
			return render(request, 'UCSDMarket/home.html')
	else:
		messages.error(request, 'User Not Authenticated')
		return render(request, 'UCSDMarket/home.html')


def Profile(request):
    if request.user.is_authenticated:
        try:
            if 'q_password1' in request.GET and 'q_password2' in request.GET:
                pass1 = request.GET['q_password1']
                pass2 = request.GET['q_password2']
                if pass1 == pass2 and pass1 != '':
                    u = User.objects.get(username=request.user.username)
                    u.set_password(pass1)
                    u.save()
                    logout(request)
                    messages.success(request, 'Password changed. Please Relogin.')
                    return render(request, 'UCSDMarket/home.html')
                else:
                    messages.error(request, 'Passwords did not match.')
            return render(request, 'UCSDMarket/profile.html')
        except Exception as e:
            messages.error(request, "Issue has occured while attempting to delete User. Contact support.")
            return render(request, 'UCSDMarket/home.html')
    else:
        messages.error(request, 'User Not Authenticated')
        return render(request, 'UCSDMarket/home.html')


def CreateListings(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CreateListingForm(request.POST, request.FILES)
            if form.is_valid():

                deliverable = False
                if request.POST.get('canDeliver', False):
                    deliverable = True

                newListing = Listing(
                user = request.user,
                title = request.POST['title'],
                Price = request.POST['Price'],
                canDeliver = deliverable,
                condition = request.POST['condition'],
                description = request.POST['description'],
                contactInformation = request.POST['contactInformation'])

                newListing.save()
                # save uploaded picture to the database along with the id of the listing
                if request.POST.get('image', True):
                    newPic = Picture(listingKey = newListing, picture=request.FILES['image'])
                    newPic.save()
                messages.success(request, 'Listing Successfully Created')
                return redirect("MyListings")
        else:
            form = CreateListingForm()
            context = {
                "Title" : "Create my listing here!",
                "Description" : "Please fill out the following form to post your item.",
                "form" : form
            }
            return render(request, "UCSDMarket/create_listing.html", context)
    else:
        messages.error(request, 'User Not Authenticated')
        return render(request, "UCSDMarket/home.html")

def EditListings(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            listingId = request.POST['id'];

            existingListing = Listing.objects.get(id=listingId)

            if request.user != existingListing.user:
                messages.error(request, 'User Not Authenticated')
                return render(request, "UCSDMarket/home.html")

            if request.POST.get('canDeliver', False):
                canDeliver = True
            else:
                canDeliver = False

            existingListing.title = request.POST['title']
            existingListing.Price = request.POST['price']
            existingListing.canDeliver = canDeliver
            existingListing.condition = request.POST['condition']
            existingListing.description = request.POST['description']
            existingListing.contactInformation = request.POST['contactInformation']

            existingListing.save()
            
            # delete images
            for key in request.POST:
                if key.startswith('deleteImage'):
                    id = key[12:]
                    picToDel = Picture.objects.get(id=id)
                    picToDel.delete()

            if request.POST.get('image', True):
                for img in  request.FILES.getlist('image'):
                    newPic = Picture(listingKey = existingListing, picture=img)
                    newPic.save()


            return redirect("/market/listing/?listing="+listingId)
        else:
            messages.error(request, 'Unexpected error')
            return render(request, "UCSDMarket/home.html")
    else:
        messages.error(request, 'User Not Authenticated')
        return render(request, "UCSDMarket/home.html")

def SearchListings(request):
    template = "UCSDMarket/my_listings.html"
    query = request.GET.get('q')
    results = Listing.objects.filter(
        Q(title__startswith='b') &~ Q(price__endswith='1'))
    #a = Listing.objects.filter(results)
    # print(results)
    # print(request.path)
    # print(request.get_full_path())
    # print(request.META)



    Listings = []

    for post in results:
        all_images = Picture.objects.filter(listingKey=post)
        if not all_images:
            thumbImg = static('img/NoImage.png')
        else:
            thumbImg = all_images[0].picture.url
        Favd = False
        if request.user.is_authenticated and Favorite.objects.filter(user=request.user, listingKey=post.id).exists():
            Favd = True
        Listings.append({
            "id" : post.id,
            "Title" : post.title,
            "Seller" : post.user.username,
            "Price" : post.Price,
            "CanDeliver" : post.canDeliver,
            "Condition" : post.condition,
            "Description" : post.description,
            "ContactInformation" : post.contactInformation,
            "Thumbnail": thumbImg,
            "Favd": Favd
        })
    return render(request, 'UCSDMarket/search_listing.html', { 'query_string': query, 'posts': Listings})

    # context = {
    #     "Title" : "Search and explore what you want!",
    #     "Description" : "Please enter the information you would like to search.",
    #     "Results" : "Here are the results."

    # } #


    # return render(request, "UCSDMarket/search_listing.html", context)

def search(request):
    empty_query = True

    title_words = ""
    price_words = ""
    canDeliver_words = True
    condition = ""
    description = ""

    LowPrice = "NoLowPrice"
    HighPrice = "NoHighPrice"

    if 'q_lowprice' in request.GET:
        lowprice_words = request.GET['q_lowprice']
        if lowprice_words:
            try:
                float(lowprice_words)
                LowPrice = lowprice_words
                empty_query = False
            except ValueError:
                LowPrice = "NoLowPrice"
    if 'q_highprice' in request.GET:
        highprice_words = request.GET['q_highprice']
        if highprice_words:
            try:
                float(highprice_words)
                HighPrice = highprice_words
                empty_query = False
            except ValueError:
                HighPrice = "NoHighPrice"

    filters = {}

    if 'q_title' in request.GET:
        message = 'You searched for: %r' % request.GET['q_title']
        title_words = request.GET['q_title']

        if title_words:
            empty_query = False
            filters['title__contains'] = title_words


    if 'q_canDeliver' in request.GET:
        if request.GET['q_canDeliver'] == "on":
            canDeliver_words = True
            filters['canDeliver'] = True
        else:
            canDeliver_words = False

    if 'q_condition' in request.GET:
        condition = request.GET['q_condition']
        if condition:
            empty_query = False
            filters['condition__contains'] = condition

    if 'q_description' in request.GET:
        description = request.GET['q_description']
        if description:
            empty_query = False
            filters['description__contains'] = description
  

    if not empty_query:
        listings = Listing.objects.filter(**filters)

        if LowPrice != "NoLowPrice":
            listings = listings.filter(Price__gt=Decimal(LowPrice))
        if HighPrice != "NoHighPrice":
            listings = listings.filter(Price__lt=Decimal(HighPrice))
        Listings = []

        for post in listings:
            all_images = Picture.objects.filter(listingKey=post)
            if not all_images:
                thumbImg = static('img/NoImage.png')
            else:
                thumbImg = all_images[0].picture.url
            Favd = False
            if request.user.is_authenticated and Favorite.objects.filter(user=request.user, listingKey=post.id).exists():
                Favd = True
            Listings.append({
                "id" : post.id,
                "Title" : post.title,
                "Seller" : post.user.username,
                "Price" : post.Price,
                "CanDeliver" : post.canDeliver,
                "Condition" : post.condition,
                "Description" : post.description,
                "ContactInformation" : post.contactInformation,
                "Thumbnail": thumbImg,
				"Favd": Favd
            })

        context = {
            "Listings" : Listings,
        }    


        return render(request, 'UCSDMarket/search_results.html',
                    {'posts': Listings, 'query': title_words})

    # print("request.GET is ",request.GET)
    if len(request.GET) == 0:
        empty_query = False

    return render(request, 'UCSDMarket/search_form.html', {'error': empty_query})

def DeleteListing(request):
    if request.user.is_authenticated:
        try:
            listingID = request.GET.get('listing')
            if not listingID:
                return render(request, 'UCSDMarket/home.html')
            else:
                ThisListing = Listing.objects.filter(id=int(listingID))
                if (len(ThisListing) == 1):
                    ThisListing.delete()
                    messages.success(request, "Listing Deleted")
        except Exception as e:
            messages.error(request, "Issue has occured while attempting to delete listing. Contact support.")
    return redirect("MyListings")

