from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from UCSDMarket.forms import SignupForm, ImageUploadForm, CreateListingForm
from UCSDMarket.models import Picture, Listing

# Create your views here.
def Home(request):
    context = { } #
    return render(request, "UCSDMarket/home.html", context)

def Signup(request):
    form = SignupForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        compare_password = form.cleaned_data.get('password2')
        if raw_password != compare_password:
            form.add_error('compare_password', "Password does not match")
            return redirect('signup')
        user = authenticate(username=username, password=raw_password)
        login(request, user)
        return redirect('Home')
    return render(request, 'UCSDMarket/signup.html', {'form': form})

def Signoff(request):
    logout(request)
    response = redirect('/market/login')
    return response

def ListingPage(request):
	all_entries = Picture.objects.all()

	all_pictures = []

	imgCount = 0
	for entry in all_entries:
		imgCount = imgCount + 1
		all_pictures.append({
							"Image": entry,
							"Number": imgCount
							})

	context = {
		"Title" : "IKEA full size bed",
		"Seller" : "John Doe",
		"Price" : 50,
		"CanDeliver" : True,
		"Condition" : "Used",
		"Description" : "Need this gone by Oct 31. Great condition. Can deliver for some extra fee. Original price was $129Need this gone by Oct 31. Great condition. Can deliver for some extra fee. Original price was $129Need this gone by Oct 31. Great condition. Can deliver for some extra fee. Original price was $129Need this gone by Oct 31. Great condition. Can deliver for some extra fee. Original price was $129Need this gone by Oct 31. Great condition. Can deliver for some extra fee. Original price was $129Need this gone by Oct 31. Great condition. Can deliver for some extra fee. Original price was $129Need this gone by Oct 31. Great condition. Can deliver for some extra fee. Original price was $129",
		"ContactInformation" : "858 - 888 - 8888",
		"Pictures": all_pictures
	}

	return render(request, "UCSDMarket/listing.html", context)

def MyListings(request):

	if request.user.is_authenticated:
		# Get listings from user
		Listings = []

		all_entries = Picture.objects.all()
		thumbImg = all_entries[:1].get()

		Listings.append({
			"Title" : "IKEA full size bed",
			"Seller" : "John Doe",
			"Price" : 50,
			"CanDeliver" : True,
			"Condition" : "Used",
			"Description" : "Need this gone by Oct 31. Great condition. Can deliver for some extra fee. Original price was $129",
			"ContactInformation" : "858 - 888 - 8888",
			"Thumbnail": thumbImg
		})

		Listings.append({
			"Title" : "King Sized Bed",
			"Seller" : "Reggie Smiles",
			"Price" : 150,
			"CanDeliver" : False,
			"Condition" : "New",
			"Description" : "Need this gone by Oct 31. Great condition. Can deliver for some extra fee. Original price was $129",
			"ContactInformation" : "858 - 888 - 8888",
			"Thumbnail": thumbImg
		})

		Listings.append({
			"Title" : "Comfy Cot",
			"Seller" : "John Doe",
			"Price" : 30,
			"CanDeliver" : True,
			"Condition" : "Used",
			"Description" : "Need this gone by Oct 31. Great condition. Can deliver for some extra fee. Original price was $129",
			"ContactInformation" : "858 - 888 - 8888",
			"Thumbnail": thumbImg
		})

		context = {
			"Listings" : Listings,
		} #
		return render(request, "UCSDMarket/my_listings.html", context)
	else:
		return render(request, "UCSDMarket/home.html")

def CreateListings(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			form = CreateListingForm(request.POST, request.FILES)
			if form.is_valid():
				newListing = Listing(
				userID = form.userID,
				# TODO maybe the form should not have userID and it should come from somewhere else?
				title = form.title,
				seller = form.seller,
				price = form.price,
				canDeliver = form.canDeliver,
				condition = form.condition,
				description = form.description,
				contactInformation = form.contactInformation)
		
				newListing.save()
                
                			# save uploaded picture to the database along with the id of the listing
				for i in range(len(request.FILES['image'])):
					m = Picture(ListingID = newListing.id, picture = request.FILES['image'][i])
					m.save()
				else:
					pass
					# form = CreateListingForm();
					# TODO give error message: form is not valid
	else:
		# TODO give error message: user not authenticated
		pass

	context = {
		"Title" : "Create my listing here!",
		"Description" : "Please fill out the following form to post your item."

	} #
	return render(request, "UCSDMarket/create_listing.html", context)


def SearchListings(request):
	
	context = {
		"Title" : "Search and explore what you want!",
		"Description" : "Please enter the information you would like to search.", 
		"Results" : "Here are the results."

	} #
	return render(request, "UCSDMarket/search_listing.html", context)

