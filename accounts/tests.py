from django.core import mail
from django.test import TestCase
from django.urls import reverse
from .models import CustomUser

# Create your tests here.
class SetUpTest(TestCase):
    def setUp(self):
        self.signup_url=reverse('accounts:signup')
        self.login_url=reverse('accounts:login')

        self.valid_user={
            'email':'test@gmail.com',
            'username':'testUser123',
            'first_name':'Test',
            'last_name':'User',
            'password1':'TestPassword12345',
            'password2':'TestPassword12345',
        }

        self.valid_user_login={
            'username':'testUser123', 
            'password':'TestPassword12345',
        }

        self.invalid_email_user={
            'email':'invalid.email',
            'username':'invalidEmail123',
            'first_name':'Invalid',
            'last_name':'Email',
            'password1':'TestEmail12345',
            'password2':'TestEmail12345',
        }

        self.short_password_user={
            'email':'short@gmail.com',
            'username':'shortPassword123',
            'first_name':'Short',
            'last_name':'Password',
            'password1':'passTwo',
            'password2':'passTwo',
        }

        self.not_matching_passwords_user={
            'email':'matching@gmail.com',
            'username':'notMatching123',
            'first_name':'Unmatched',
            'last_name':'Passwords',
            'password1':'TestEmail12345',
            'password2':'unMatched54321',
        }

        return super().setUp()
    
class SignupTest(SetUpTest):
    # Verifies the page is accessable using correct url, and if it renders the correct html
    def test_can_access_page(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')
    
    # Verifies the user is redirect using valid account details, indicating success
    def test_can_signup_user(self):
        response = self.client.post(self.signup_url, self.valid_user)
        self.assertEqual(response.status_code, 302) 

    # Verifies the user is informed correctly that email is taken when inputing taken email. 
    def test_cant_signup_taken_email(self):
        self.client.post(self.signup_url, self.valid_user)
        response=self.client.post(self.signup_url, self.valid_user)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This email address is already in use, please use another email address.")

    # Verifies the user is informed correctly that username is taken when inputing taken username. 
    def test_cant_signup_taken_username(self): 
        self.client.post(self.signup_url, self.valid_user)
        response=self.client.post(self.signup_url, self.valid_user)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This username is already in use, please use another username.")

    # Verifies the user is informed correctly that there two passwords dont match. 
    def test_cant_signup_unmatching_passwords(self):
        response=self.client.post(self.signup_url, self.not_matching_passwords_user)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The two password fields didn’t match.")


class LoginTest(SetUpTest):
    # Verifies the user renders the correct page, when using the correct url
    def test_can_access_page(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    # Verifies the user can login using valid account details if account is verified 
    def test_user_can_login(self):
        self.client.post(self.signup_url, self.valid_user)
        user = CustomUser.objects.get(username='testUser123')
        user.verified = True # Ensure account is verified
        user.save()

        response = self.client.post(self.login_url, self.valid_user_login)
        self.assertEqual(response.status_code, 302)

    # Verifies the user cant login using valid account details if account isn't verified 
    def test_user_cant_login_unverified(self):
        self.client.post(self.signup_url, self.valid_user)
        response = self.client.post(self.login_url, self.valid_user_login)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Email has not been verified")


class VerificationTest(SetUpTest):
    # Verifies an email is sent when user signs up using valid details
    def test_send_verification_email(self):
        # Signs up a new user using valid details
        self.client.post(self.signup_url, self.valid_user)
        user = CustomUser.objects.get(username='testUser123')

        self.assertEqual(len(mail.outbox), 1) # Checks if mail outbox contains one new email
        verification_email = mail.outbox[0] # Stores new email in variable

        # Checks if the email holds the correct contents
        self.assertEqual(verification_email.subject, "Email Verification for Sustainable Campus")
        verification_link = f"http://127.0.0.1:8000/accounts/email_verification/{user.verification_token}"
        email_body = f"Hello {user.first_name}, \n\nPlease verify your email through the following link below:\n{verification_link}\n\nThank You!"
        self.assertEqual(verification_email.body, email_body)

    # Verifies a user account can, on valid signup, use their verification token to verifiy.
    def test_user_verify_successfully(self):
        # Signs up a new user using valid details, and stores its verification_token in a variable
        self.client.post(self.signup_url, self.valid_user)
        user = CustomUser.objects.get(username='testUser123')
        token = user.verification_token

        # Creates the expected url for verification
        verification_url = (reverse('accounts:email_verification', kwargs={'token': token}))

        # Verifies a new page is rendered on using the url, and if the correct message is given
        response = self.client.get(verification_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/')

        # Verifies if the user is now verified
        user = CustomUser.objects.get(username='testUser123')
        self.assertTrue(user.verified)