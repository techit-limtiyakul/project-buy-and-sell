from django.shortcuts import render

# Create your views here.
def Home(request):
    context = { } #
    return render(request, "UCSDMarket/home.html", context)

def Listing(request):
	
	context = {
		"Title" : "IKEA full size bed",
		"Seller" : "John Doe",
		"Price" : 50,
		"CanDeliver" : True,
		"Condition" : "Used",
		"Description" : "Need this gone by Oct 31. Great condition. Can deliver for some extra fee. Original price was $129",
		"ContactInformation" : "858 - 888 - 8888"
	} #
	return render(request, "UCSDMarket/listing.html", context)

def MyListings(request):
	
	Listings = []
	
	Listings.append({
		"Title" : "IKEA full size bed",
		"Seller" : "John Doe",
		"Price" : 50,
		"CanDeliver" : True,
		"Condition" : "Used",
		"Description" : "Need this gone by Oct 31. Great condition. Can deliver for some extra fee. Original price was $129",
		"ContactInformation" : "858 - 888 - 8888"
	})
	
	Listings.append({
		"Title" : "King Sized Bed",
		"Seller" : "Reggie Smiles",
		"Price" : 150,
		"CanDeliver" : False,
		"Condition" : "New",
		"Description" : "Need this gone by Oct 31. Great condition. Can deliver for some extra fee. Original price was $129",
		"ContactInformation" : "858 - 888 - 8888"
	})
	
	Listings.append({
		"Title" : "Comfy Cot",
		"Seller" : "John Doe",
		"Price" : 30,
		"CanDeliver" : True,
		"Condition" : "Used",
		"Description" : "Need this gone by Oct 31. Great condition. Can deliver for some extra fee. Original price was $129",
		"ContactInformation" : "858 - 888 - 8888"
	})
	
	context = {
		"Listings" : Listings,
	} #
	return render(request, "UCSDMarket/my_listings.html", context)