from django.shortcuts import render, redirect
from django.contrib.auth import logout
from UCSDMarket.forms import SignupForm, ImageUploadForm
from UCSDMarket.models import Picture

# Create your views here.
def Home(request):
    context = { } #
    return render(request, "UCSDMarket/home.html", context)

def Signup(request):
	form = SignupForm();
	return render(request, 'UCSDMarket/signup.html', {'form': form})

def Signoff(request):
	logout(request);
	response = redirect('/market/login')
	return response

def Listing(request):
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