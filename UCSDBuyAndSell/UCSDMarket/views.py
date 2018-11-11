from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from UCSDMarket.forms import SignupForm, CreateListingForm
from UCSDMarket.models import Picture, Listing


# Create your views here.
def Home(request):
    context = { } #
    return render(request, "UCSDMarket/home.html", context)

def Signup(request):
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
        form.save()
        user = authenticate(username=username, password=raw_password)
        login(request, user)
        return redirect('Home')
    return render(request, 'UCSDMarket/signup.html', {'form': form})

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
                                        "Image": image,
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
                thumbImg = False
            else:
                thumbImg = all_images[0]
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

    context = {
        "Title" : "Search and explore what you want!",
        "Description" : "Please enter the information you would like to search.",
        "Results" : "Here are the results."

    } #
    return render(request, "UCSDMarket/search_listing.html", context)

