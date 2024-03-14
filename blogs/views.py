from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.utils.http import urlencode
from django.urls import reverse
from .models import BlogPost, BlogCategory, BlogUser
from .forms import BlogForm, CategoryForm
# Create your views here.

# minutes and seconds variable
minutes = 60
seconds = minutes * 60

""" Utility functions"""
# define a function to set my cookies in login url.
def create_response_with_cookies(login_url="accounts/login"):
    response = redirect(login_url)
    response.set_cookie("till_browser_closes", "wait_for_browser")
    response.set_cookie("time_cookie", f"{minutes}_minutes", max_age=seconds)
    return response

def check_current_user_to_get_user(request, dj_user_pk):
    current_django_user_username = request.user.get_username()
    current_django_user_id = User.objects.filter(
        username=current_django_user_username,
    ).first().id
    if current_django_user_id != dj_user_pk:
        login_url = reverse("login") + "?" + urlencode({"next": reverse("blog:home")})
        response = create_response_with_cookies(login_url)
        return ("no", response)
    return ("yes", )

def check_creator_of_blog_post(dj_user_pk, blog_post):
    blog_post_creator = blog_post.blog_user.user_id
    if dj_user_pk == blog_post_creator:
        return True
    return False


class BlogCreate(View):
    def get(self, request, dj_user_pk):
        if request.user.is_authenticated:
            # to prevent a  blog post creation
            # without the actual django_user logged in, but the post is created
            # because another user is logged in and their session has not expired
            # and doing it this must be done
            # put this as a utility function so I DRM(don't repeat myself) 
            outcome = check_current_user_to_get_user(request, dj_user_pk)
            if outcome[0] == "no":
                return outcome[1]
            else:
                pass

            # now after we know that is the actual django_user
            # we have to check the cookies if they have expired
            # then finally redirect the login to the blogcreate form for that user
            if (not request.COOKIES.get("till_browser_closes", None) == "wait_for_browser")  or \
                    (not request.COOKIES.get("time_cookie", None) == f"{minutes}_minutes"):
                login_url = reverse("login") + "?" + urlencode({"next": request.path})
                response = create_response_with_cookies(login_url)
                return response
            # initalize an empty context variable
            context = {}

            # check if the blog post creatin was a success
            if request.session.get("outcome", None) == 0:
                    message = "blog post successfully created"
                    context["message"] = message
                    del request.session["outcome"]

            #create a blog user using the django user id
            blog_user, created = BlogUser.objects.get_or_create(
                                    user_id=dj_user_pk,
            )

            # get initial data in the BlogForm
            default_category = BlogCategory.objects.filter(
                category="Tech",
            ).first()
            default_data = {
                "blog_user": blog_user.id,
                "blog_category": default_category.id, 
            }
            blog_form = BlogForm(initial=default_data)
            category_form = CategoryForm()
            dj_user_id = dj_user_pk

            # save blog form, category form and django_user_id
            # in a context variable to be used in the template
            context["blog_form"] = blog_form
            context["category_form"] = category_form
            context["dj_user_id"] = dj_user_id
            
            # return a template either on sucess or trying to create
            # post
            return render(request, "blogs/CreateBlog.html", context)

        # if user is not authenticated or a direct get request was sent.
        login_url = reverse("login") + "?" + urlencode({"next": reverse("blog:home")})
        response = create_response_with_cookies(login_url)
        return response

    def post(self, request, dj_user_pk):
        # check category form data
        category_data = {
            "category": request.POST.get("category"),
        }
        blog_data = {
            "blog_title": request.POST.get("blog_title"),
            "blog": request.POST.get("blog"),
            "blog_user": request.POST.get("blog_user"),
            "blog_category": request.POST.get("blog_category"),
        }
        check_category_form = CategoryForm(category_data)
        check_blog_form = BlogForm(blog_data)
        if (not check_category_form.is_valid()) or \
                (not check_blog_form.is_valid()):
            dj_user_id = dj_user_pk
            context = {
                "blog_form": check_blog_form,
                "category_form": check_category_form,
                "dj_user_id": dj_user_id,
            }
            return render(request, "blogs/CreateBlog.html", context)
        # get category id and save blog data
        save_category_id = BlogCategory.objects.filter(
            category=request.POST.get("category"),
        ).first().id
        save_blog_data = {
            "blog_title": request.POST.get("blog_title"),
            "blog": request.POST.get("blog"),
            "blog_user": request.POST.get("blog_user"),
            "blog_category": save_category_id,
        }
        save_blog_form = BlogForm(save_blog_data)
        save_blog_form.save()
        request.session["outcome"] = 0
        return redirect(request.path)


class BlogRead(View):
    def get(self, request, dj_user_pk, start, end, counter):
        if request.user.is_authenticated:
            # check if blog user exists first
            blog_user = BlogUser.objects.filter(
                user_id=dj_user_pk,
            ).first()
            if not blog_user:
                response = create_response_with_cookies()
                return response

            # put this as a utility function so I DRM(don't repeat myself) 
            outcome = check_current_user_to_get_user(request, dj_user_pk)
            if outcome[0] == "no":
                return outcome[1]
            else:
                pass

            if (not request.COOKIES.get("till_browser_closes", None) == "wait_for_browser")  or \
                    (not request.COOKIES.get("time_cookie", None) == f"{minutes}_minutes"):
                login_url = reverse("login") + "?" + urlencode({"next": request.path})
                response = create_response_with_cookies(login_url)
                return response
            # initialize the context
            context = {}
            splited_user_blogs = blog_user.user_blogs.all()[start: end]
            if not splited_user_blogs:
                message = "No more posts available :("
                context["message"] = message
            length_of_user_blogs = len(splited_user_blogs)
            context["splited_user_blogs"] = splited_user_blogs
            context["start"] = start
            context["end"] = end
            context["dj_user_pk"] = dj_user_pk
            context["length_of_user_blogs"] = length_of_user_blogs
            context["counter"] = counter

            # return template ReadBlog.html
            return render(request, "blogs/ReadBlog.html", context)

        # if the user is not authenticated
        login_url = reverse("login") + "?" + urlencode({"next": request.path})
        response = create_response_with_cookies(login_url)
        return response


class BlogUpdate(View):
    def get(self, request, dj_user_pk, blog_post_id, back_path):
        if request.user.is_authenticated:
            # check if blog user exist first
            blog_user = BlogUser.objects.filter(
                user_id=dj_user_pk,
            ).first()
            if not blog_user:
                response = create_response_with_cookies()
                return response

            # check if blog_post exist using blog_post_id
            blog_post = BlogPost.objects.filter(
                id=blog_post_id,
            ).first()
            if not blog_post:
                response = create_response_with_cookies()
                return response

            # check if the user throught get is same as user authenticated
            outcome = check_current_user_to_get_user(request, dj_user_pk)
            if outcome[0] == "no":
                return outcome[1]
            else:
                pass
            
            # now use the blog post to know the user that created it
            # by comaparing the dj_user_pk == blogpost.user.user_id
            creator_outcome = check_creator_of_blog_post(dj_user_pk, blog_post)
            if not creator_outcome:
                response = create_response_with_cookies
                return response
            
            # now check for cookies
            if (not request.COOKIES.get("till_browser_closes", None) == "wait_for_browser")  or \
                    (not request.COOKIES.get("time_cookie", None) == f"{minutes}_minutes"):
                login_url = reverse("login") + "?" + urlencode({"next": request.path})
                response = create_response_with_cookies(login_url)
                return response
            
            # now if all case is justifed create an updateform object using the blogform
            # and intsance of that blog post to create a new form
            context = {}
            update_form = BlogForm(instance=blog_post)
            context["update_form"] = update_form
            context["dj_user_pk"] = dj_user_pk
            context["blog_post_id"] = blog_post_id
            context["back_path"] = back_path
            
            # check if this is a successful outcome or the post request
            if request.session.get("outcome", None) == "success":
                message = request.session.get("message")
                context["message"] = message
                del request.session["outcome"]
                del request.session["message"]
            return render(request, "blogs/UpdateBlog.html", context)
        
        # if user is not authenticated
        login_url = reverse("login") + "?" + urlencode({"next": request.path})
        response = create_response_with_cookies(login_url)
        return response

    def post(self, request, dj_user_pk, blog_post_id, back_path):
        # check if cookies has expired then sen to login if expired
        # and now a get request to the request.path
        if (not request.COOKIES.get("till_browser_closes", None) == "wait_for_browser")  or \
                (not request.COOKIES.get("time_cookie", None) == f"{minutes}_minutes"):
            login_url = reverse("login") + "?" + urlencode({"next": request.path})
            response = create_response_with_cookies(login_url)
            return response
        
        context = {}
        # now first validation to se if form is without errors
        check_update_form = BlogForm(request.POST)
        if not check_update_form.is_valid():
            context["update_form"] = check_update_form
            context["dj_user_pk"] = dj_user_pk
            context["blog_post_id"] = blog_post_id
            context["back_path"] = back_path
            return render(request, "blogs/UpdateBlog.html", context)

        """
        This is not working i dont know why though.
        # for validation 2 if my dj_user starts from 1 don't subtract 1 from dj_user
        # if not subtract 1 from dj_user
        user = request.POST.get("blog_user")
        if dj_user_pk - 1 != user:
            error_message = f"Warning, you have selected an invalid user by messing with blog_user field, you are {dj_user_pk}"
            blog_post = BlogPost.objects.filter(
                id=blog_post_id,
            ).first()
            check_update_form = BlogForm(instance=blog_post)
            context["update_form"] = check_update_form
            context["dj_user_pk"] = dj_user_pk
            context["blog_post_id"] = blog_post_id
            context["back_path"] = back_path
            context["error_message"] = error_message
            return render(request, "blogs/UpdateBlog.html", context)
        """

        # if both validation are good do this
        # get the post instance take the updated instance and save it
        blog_post = BlogPost.objects.filter(
            id=blog_post_id,
        ).first()
        save_update_form = BlogForm(request.POST, instance=blog_post)
        save_update_form.save()

        # now do the post redirect get request, success outcome, and put a success message in session
        message = "Form updated successfully :)"
        request.session["outcome"] = "success"
        request.session["message"] = message
        return redirect(request.path)


class BlogReadUpdate(View):
    def get(self, request, dj_user_pk, start, end, counter):
        if request.user.is_authenticated:
            # check if blog user exists first
            blog_user = BlogUser.objects.filter(
                user_id=dj_user_pk,
            ).first()
            if not blog_user:
                response = create_response_with_cookies()
                return response

            # put this as a utility function so I DRM(don't repeat myself)
            outcome = check_current_user_to_get_user(request, dj_user_pk)
            if outcome[0] == "no":
                return outcome[1]
            else:
                pass

            if (not request.COOKIES.get("till_browser_closes", None) == "wait_for_browser")  or \
                    (not request.COOKIES.get("time_cookie", None) == f"{minutes}_minutes"):
                login_url = reverse("login") + "?" + urlencode({"next": request.path})
                response = create_response_with_cookies(login_url)
                return response
            # initialize the context
            context = {}
            splited_user_blogs = blog_user.user_blogs.all()[start: end]
            if not splited_user_blogs:
                message = "No more posts available :("
                context["message"] = message
            length_of_user_blogs = len(splited_user_blogs)
            context["splited_user_blogs"] = splited_user_blogs
            context["start"] = start
            context["end"] = end
            context["dj_user_pk"] = dj_user_pk
            context["length_of_user_blogs"] = length_of_user_blogs
            context["counter"] = counter
            context["back_path"] = str(request.path)[1:]

            # return template UpdateReadBlog.html
            return render(request, "blogs/UpdateReadBlog.html", context)

        # if user not authenticated
        login_url = reverse("login") + "?" + urlencode({"next": request.path})
        response = create_response_with_cookies(login_url)
        return response



class BlogDelete(View):
    def get(self, request, dj_user_pk, blog_post_id, back_path):
        if request.user.is_authenticated:
            # check if blog user exist first
            blog_user = BlogUser.objects.filter(
                user_id=dj_user_pk,
            ).first()
            if not blog_user:
                response = create_response_with_cookies()
                return response

            # check if blog_post exist using blog_post_id
            blog_post = BlogPost.objects.filter(
                id=blog_post_id,
            ).first()
            if not blog_post:
                response = create_response_with_cookies()
                return response

            # check if the user throught get is same as user authenticated
            outcome = check_current_user_to_get_user(request, dj_user_pk)
            if outcome[0] == "no":
                return outcome[1]
            else:
                pass

            # now use the blog post to know the user that created it
            # by comaparing the dj_user_pk == blogpost.user.user_id
            creator_outcome = check_creator_of_blog_post(dj_user_pk, blog_post)
            if not creator_outcome:
                response = create_response_with_cookies
                return response

            # now check for cookies
            if (not request.COOKIES.get("till_browser_closes", None) == "wait_for_browser")  or \
                    (not request.COOKIES.get("time_cookie", None) == f"{minutes}_minutes"):
                login_url = reverse("login") + "?" + urlencode({"next": request.path})
                response = create_response_with_cookies(login_url)
                return response

            # now if all case is justifed get a context to take in some data
            context = {}
            context["dj_user_pk"] = dj_user_pk
            context["blog_post_id"] = blog_post_id
            context["back_path"] = back_path
            return render(request, "blogs/ConfirmDeleteBlog.html", context)


class ConfirmDelete(View):
    def get(self, request, blog_post_id, back_path):
        if request.session.get("outcome", None) == "success":
            message = request.session.get("message")
            context = {}
            context["back_path"] = back_path
            context["message"] = message
            del request.session["outcome"]
            del request.session["message"]
            return render(request, "blogs/DeleteSuccessPage.html", context)

        response = create_response_with_cookies()
        return response

    def post(self, request, blog_post_id, back_path):
        # check if cookies has expired then sen to login if expired
        # and now a get request to the request.path
        if (not request.COOKIES.get("till_browser_closes", None) == "wait_for_browser")  or \
                (not request.COOKIES.get("time_cookie", None) == f"{minutes}_minutes"):
            login_url = reverse("login") + "?" + urlencode({"next": request.path})
            response = create_response_with_cookies(login_url)
            return response

        
        # it is either a yes to confrm delete post or a cancel that automatically
        # takes one back to read delete page and not even submit the post
        # now get the post and delete it
        blog_post = BlogPost.objects.filter(
            id=blog_post_id,
        ).first()
        blog_post.delete()

        # now do the post redirect get request, success outcome, and put a success message in session
        message = "blogpost successfully deleted :)"
        request.session["outcome"] = "success"
        request.session["message"] = message
        return redirect(request.path)


class BlogReadDelete(View):
    def get(self, request, dj_user_pk, start, end, counter):
        if request.user.is_authenticated:
            # check if blog user exists first
            blog_user = BlogUser.objects.filter(
                user_id=dj_user_pk,
            ).first()
            if not blog_user:
                response = create_response_with_cookies()
                return response

            # put this as a utility function so I DRM(don't repeat myself)
            outcome = check_current_user_to_get_user(request, dj_user_pk)
            if outcome[0] == "no":
                return outcome[1]
            else:
                pass

            if (not request.COOKIES.get("till_browser_closes", None) == "wait_for_browser")  or \
                    (not request.COOKIES.get("time_cookie", None) == f"{minutes}_minutes"):
                login_url = reverse("login") + "?" + urlencode({"next": request.path})
                response = create_response_with_cookies(login_url)
                return response
            # initialize the context
            context = {}
            splited_user_blogs = blog_user.user_blogs.all()[start: end]
            if not splited_user_blogs:
                message = "No more posts available :("
                context["message"] = message
            length_of_user_blogs = len(splited_user_blogs)
            context["splited_user_blogs"] = splited_user_blogs
            context["start"] = start
            context["end"] = end
            context["dj_user_pk"] = dj_user_pk
            context["length_of_user_blogs"] = length_of_user_blogs
            context["counter"] = counter
            context["back_path"] = str(request.path)[1:]

            # return template UpdateReadBlog.html
            return render(request, "blogs/DeleteReadBlog.html", context)

        # if user not authenticated
        login_url = reverse("login") + "?" + urlencode({"next": request.path})
        response = create_response_with_cookies(login_url)
        return response


def homepage(request):
    if request.user.is_authenticated:
        if (not request.COOKIES.get("till_browser_closes", None) == "wait_for_browser")  or \
                (not request.COOKIES.get("time_cookie", None) == f"{minutes}_minutes"):
            login_url = reverse("login") + "?" + urlencode({"next": request.path})
            response = create_response_with_cookies(login_url)
            return response
        
        # get primary key of user, firstname and lastname
        user_obj = User.objects.filter(username=request.user.get_username()).first()
        user_pk = user_obj.id
        user_firstname = user_obj.first_name
        user_lastname = user_obj.last_name
        # once you are sent to the homepage you must create a bloguser
        # create a blog user using the django user id
        # and do nothing with it
        blog_user, created = BlogUser.objects.get_or_create(
                                    user_id=user_pk,
        )
        # now get the username to know the number of logins
        user_userhandle = user_obj.username
        request.session[user_userhandle] = request.session.get(user_userhandle, 0) + 1
        if request.session.get(user_userhandle) <= 1:
            user_message = "Welcome"
        else:
            user_message = "Welcome back"
        context = {
            "user_pk": user_pk,
            "user_firstname": user_firstname,
            "user_lastname": user_lastname,
            "user_message": user_message,
        }
        return render(request, "blogs/user_homepage.html", context)
    login_url = reverse("login") + "?" + urlencode({"next": request.path})
    response = create_response_with_cookies(login_url)
    return response


class SignUp(View):
    def get(self, request):
        if request.session.get("status", None) == 1:
            message = request.session.get("message")
            cntx = {"message": message}
            del request.session["message"]
            del request.session["status"]
            return render(request, "blogs/signup.html", cntx)
        elif request.session.get("status", None) == 0:
            del request.session["status"]
            login_url = reverse('login') + '?' + urlencode({'next': reverse('blog:home')})
            response = create_response_with_cookies(login_url)
            return response
        return render(request, "blogs/signup.html")

    def post(self, request):
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password_auth = request.POST.get("verify-password")

        # credentials check
        fullname = User.objects.filter(
                    first_name=firstname.capitalize(),
                    last_name=lastname.capitalize(),
                ).first()
        user_handle = User.objects.filter(username=username)
        email_check = User.objects.filter(email=email.lower())
        password_check = User.objects.filter(password=password)

        # verifying status
        if fullname:
            message = "This user already exists i.e first and last name"
            request.session["message"] = message
            request.session["status"] = 1
            return redirect(request.path)
        elif user_handle:
            message = "username {} is already taken.".format(username)
            request.session["message"] = message
            request.session["status"] = 1
            return redirect(request.path)
        elif email_check:
            message = "This email is already in use."
            request.session["message"] = message
            request.session["status"] = 1
            return redirect(request.path)
        elif password_check:
            message = "This password already belongs to a user."
            request.session["message"] = message
            request.session["status"] = 1
        elif password != password_auth:
            message = "Verified password is not the same with password."
            request.session["message"] = message
            request.session["status"] = 1
            return redirect(request.path)
        else:
            new_user = User.objects.create_user(
                        first_name=firstname.capitalize(),
                        last_name=lastname.capitalize(),
                        username=username,
                        email=email.lower(),
                        password=password,
                    )
            request.session["status"] = 0
            return redirect(request.path)
