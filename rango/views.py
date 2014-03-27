from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from rango.bing_search import run_query

#Import the Category model
from rango.models import Category, Page, UserProfile
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm

@login_required
def restricted(request):
	context_dict = {'boldmessage':"RESTRICTED.  EXIT NOW!"}
    	context =  RequestContext(request)
    	return render_to_response('rango/restricted.html', context_dict, context)

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/rango/')

def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user is not None:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/rango/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Do Not Try This.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('rango/sign_in.html', {}, context)


def register(request):
	if request.session.test_cookie_worked():
		print ">>>> TEST COOKIE WORKED!"
		request.session.delete_test_cookie()

        #like before, get the request's context
	context = RequestContext(request)

	#a boolean value for telling the template whether the registration was successful
	#set to false initially. code changes value to true when registration succeeds
	registered = False

	#if its a HTTP POST, were interested in processing form data
	if request.method == 'POST':
		#attempt to grab informatino from teh raw form info
		#note that we make use of both UserForm and UserProfileForm
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()

			profile = profile_form.save(commit=False)
			profile.user = user

			if 'picture' in request.FILES:
				profile.pictur = request.FILES['picture']

			profile.save()
			registred = True

		else:
			print user_form.errors, profile_form.errors

	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

	return render_to_response(
			'rango/register.html',
			{'user_form' : user_form, 'profile_form' : profile_form, 'registered' : registered},
			context)



#make sure this class encodes and decodes the url
#everywhere with tha cat url, its /rango/category/{category stuff }add page
def add_page(request, category_name_url):
	context = RequestContext(request)

	category_name = decode(category_name_url)
	if request.method == 'POST':
		form = PageForm(request.POST)

		if form.is_valid():
			page = form.save(commit=False)

			try:
				cat = Category.objects.get(name=category_name)
				page.category = cat
			except Category.DoesNotExist:
				return render_to_response('rango/add_category.html', {}, context)

			
			page.views=0
			

			pagave.save()
			return category(request, category_name_url)
		else:
			print form.errors
	else:
		form = PageForm()

	return render_to_response( 'rango/add_page.html',
			{'category_name_url' : category_name_url,
			 'category_name' : category_name, 'form':form},
			 context) 
@login_required
def add_category(request):
	#get the context form the request
	context = RequestContext(request)


	#A HTTP POST?
	if request.method == 'POST':
		form = CategoryForm(request.POST)

		#have them provided with a valid form
		if form.is_valid():
			form.save(commit=True)

			#now call the main() view
			#the user will be shown the homepage
			return main(request)
		else:
			print form.errors

	else:
		form = CategoryForm()

	#bad form of form details, no from suppied
	#render the form with error msgs if any
	return render_to_response('rango/add_category.html', {'form':form}, context)


def main(request):
    context = RequestContext(request)

    category_list = Category.objects.all()
    context_dict = {'categories': category_list}

    for category in category_list:
    	category.url = encode(category.name)

    page_list = Page.objects.order_by('-views')[:5]
    context_dict['pages'] = page_list

    if request.session.get('last_visit'):
    	last_visit_time = request.session.get('last_visit')
    	visits = request.session.get('visits', 0)

    	if (datetime.now() - datetime.strptime(last_visit_time[:-7], "%Y-%m-%d %H:%M:%S")).seconds > 5:
		request.session['visits'] = visits + 1
		request.session['last_visit'] = str(datetime.now())
	else:
		pass
    else:
	    request.session['last_visit'] = str(datetime.now())
	    request.session['visits'] = 1
    return render_to_response('rango/index.html', context_dict, context)

def about(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    context_dict = {}
    # If the visits session varible exists, take it and use it.
    # If it doesn't, we haven't visited the site so set the count to zero.
    if request.session.get('visits'):
	    count = request.session.get('visits')
    else:
	    count = 0
    # remember to include the visit data
    return render_to_response('rango/about.html', {'visits': count}, context)

def thirdpage(request):
	return HttpResponse("Rango doesnt say anything. Back to the main page<a href='/rango'>Main</a>")



def category(request, category_name_url):
	#Request our context form the resquest passed to us
	context = RequestContext(request)

	#Cahnge underscores in the category name to spaces
	#URLs dont handle spaces well, so we use _
	category_name = decode(category_name_url)

	#Create a context dict which we can pass to the templates rendering engine
	#we start by containign the name of hte catgory passed by user
	context_dict = {'category_name' : category_name,
					'category_name_url' : category_name_url}

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

def page(request, page_name_url):
	#Request our context form the resquest passed to us
	context = RequestContext(request)

	#Cahnge underscores in the category name to spaces
	#URLs dont handle spaces well, so we use _
	page_name = encode(page_name_url)

	#Create a context dict which we can pass to the templates rendering engine
	#we start by containign the name of hte catgory passed by user
	context_dict = {'page_name' : page_name}

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

def encode(raw_url):
	return raw_url.replace(' ', '_')

def decode(cooked_url):
	return cooked_url.replace('_', ' ')

def search(request):
	context = RequestContext(request)
	result_list = []

	if request.method == 'POST':
		query = request.POST['query'].strip()

		if query:
			result_list = run_query(query)

	return render_to_response('rango/search.html', {'result_list': result_list}, context)
