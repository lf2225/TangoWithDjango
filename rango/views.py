from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.http import HttpResponse
#Import the Category model
from rango.models import Category, Page


def main(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)
    #Query the database for a list of ALL catrogires currently stored.
    #Order the categories by number of likes in descending order.
    #Retrieve the top 5 only - or all if less than 5.
    #Place the list in the context_dict dictionary which will be passed to the templates engine.
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories' : category_list}
    #context_dict = {'boldmessage': "I am bold font from the context"}


    # The following two lines are new.
    # We loop through each category returned, and create a URL attribute.
    # This attribute stores an encoded URL (e.g. spaces replaced with underscores).
    for category in category_list:
        category.url = category.name.replace(' ', '_')

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    #return render_to_response('rango/index.html', context_dict, context)

    #Render the response and send it back!
    return render_to_response('rango/index.html', context_dict, context)


def about(request):
	 # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    context_dict = {'boldmessage': "I am bold font from the context"}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render_to_response('rango/index.html', context_dict, context)
def thirdpage(request):
	return HttpResponse("Rango doesnt say anything. Back to the main page<a href='/rango'>Main</a>")



def category(request, category_name_url):
	#Request our context form the resquest passed to us
	context = RequestContext(request)

	#Cahnge underscores in the category name to spaces
	#URLs dont handle spaces well, so we use _
	category_name = category_name_url.replace('_', ' ')

	#Create a context dict which we can pass to the templates rendering engine
	#we start by containign the name of hte catgory passed by user
	context_dict = {'category_name' : category_name}

	try:
		#Can we find a category with a given name?
		#If we can, the .get() method raisesa DoesNotExist exception
		#So the .get() emethod returns oe model instance or raises an except.
		category = Category.objects.get(name=category_name)

		#Retrieve all of the assicated pages
		#Noe that filter returns >= 1 model instance
		pages = Page.objects.filter(category=category)

		#Add our results list to the template context under name pages
		context_dict['pages'] = pages
		#We also add th category object from the database to the context dict
		#We'll use this in the template to varify that the category exists
		context_dict['category'] = category
	except Category.DoesNotExist:
		#we get hre if no find specific category
		#teplate display 'no category'
		pass

	#go render response and return to client
	return render_to_response('rango/category.html', context_dict, context)