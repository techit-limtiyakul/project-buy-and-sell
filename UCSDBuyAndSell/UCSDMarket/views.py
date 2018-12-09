from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.templatetags.static import static
from UCSDMarket.forms import SignupForm, CreateListingForm
from UCSDMarket.models import Picture, Listing
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from UCSDBuyAndSell.tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage


# Create your views here.
def Home(request):
    context = { } #
    return render(request, "UCSDMarket/home.html", context)

def Signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            if not username.endswith('ucsd.edu'):
                form.add_error('username', "Email doesn't end with ucsd.edu")
                return redirect('Signup')
            raw_password = form.cleaned_data.get('password1')
            compare_password = form.cleaned_data.get('password2')
            if raw_password != compare_password:
                form.add_error('compare_password', "Password does not match")
                return redirect('Signup')
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
                                        "Image": image.picture.url,
                                        "Number": imgCount
                                        })

                context = {
                    "id" : ThisListing.id,
                    "Title" : ThisListing.title,
                    "Seller" : ThisListing.user.username,
                    "Price" : ThisListing.price,
                    "CanDeliver" : ThisListing.canDeliver,
                    "Condition" : ThisListing.condition,
                    "Description" : ThisListing.description,
                    "ContactInformation" : ThisListing.contactInformation,
                    "Pictures": all_pictures
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
                "Price" : post.price,
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
                price = request.POST['price'],
                canDeliver = deliverable,
                condition = request.POST['condition'],
                description = request.POST['description'],
                contactInformation = request.POST['contactInformation'])

                newListing.save()
                # save uploaded picture to the database along with the id of the listing
                if request.POST.get('image', False):
                    newPic = Picture(listingKey = newListing, picture=request.FILES['image'])
                    newPic.save()
#					Upload multiple images
#					for i in range(len(request.FILES['image'])):
#						m = Picture(listingKey = newListing, picture = request.FILES['image'][i])
#						m.save()
#					else:
#						pass
#						# form = CreateListingForm();
#						# TODO give error message: form is not valid
        else:
            form = CreateListingForm()
        context = {
            "Title" : "Create my listing here!",
            "Description" : "Please fill out the following form to post your item.",
            "form" : form
        }
        return render(request, "UCSDMarket/create_listing.html", context)
    else:
        # TODO give error message: user not authenticated
        return render(request, "UCSDMarket/home.html")


def SearchListings(request):
    query_string = ''
    found_entries = None
    posts = ""
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        # entry_query = utils.get_query(query_string, ['title', 'body',])
        # posts = Post.objects.filter(entry_query).order_by('created')
        ResultListings = Listing.objects.filter(title=query_string)
        Listings = []

        for post in ResultListings:
            all_images = Picture.objects.filter(listingKey=post)
            if not all_images:
                thumbImg = static('img/NoImage.png')
            else:
                thumbImg = all_images[0].picture.url
            Listings.append({
                "id" : post.id,
                "Title" : post.title,
                "Seller" : post.user.username,
                "Price" : post.price,
                "CanDeliver" : post.canDeliver,
                "Condition" : post.condition,
                "Description" : post.description,
                "ContactInformation" : post.contactInformation,
                "Thumbnail": thumbImg
            })
        return render(request, 'UCSDMarket/search_listing.html', { 'query_string': query_string, 'posts': Listings})
    else:
        return render(request, 'UCSDMarket/search_listing.html', { 'query_string': 'Null', 'found_entries': 'Enter a search term' })

    # context = {
    #     "Title" : "Search and explore what you want!",
    #     "Description" : "Please enter the information you would like to search.",
    #     "Results" : "Here are the results."

    # } #


    # return render(request, "UCSDMarket/search_listing.html", context)

