from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from accounts.models import CustomUser
from .models import ShopItem, UserBalance, CurrencyTransaction, ItemPurchase
import os
import glob
from django.conf import settings
from django.test import override_settings
import tempfile

# Setup many of the 
@override_settings(MEDIA_ROOT=tempfile.mkdtemp()) # Makes temporary media folder for storage of test images 
class SetUpTest(TestCase):
    def setUp(self):
        self.shop_url=reverse('shop:shop')
        self.redeem_page_url = reverse('shop:redeem_page')

        # Creates a test player account
        self.player = CustomUser.objects.create_user(email ='player@gmail.com', 
                                                    username = 'player1', 
                                                    password = 'testpassword12345',
                                                    first_name = 'Player',
                                                    last_name = 'User',
                                                    role = 'player',
                                                    verified = True)
        # Creates initial balance for test player
        self.player_balance = UserBalance.objects.create(user_id = self.player, currency = 20)

        # Fake image used for shop items
        test_image = SimpleUploadedFile(
            name = 'test_image.jpg',
            content = b'',
            content_type = 'image/jpeg'
        )

        # Creates digital shop item
        self.digital_shop_item = ShopItem.objects.create(name="Digital item", currency_cost=10, 
                                                         description = 'digital item description',
                                                         image = test_image, is_digital=True)
        
        # URL to buy above item
        self.buy_digital_item_url=(reverse('shop:buy_shop_item', args=[self.digital_shop_item.item_id]))
        
        # Creates non-digital shop item
        self.non_digital_shop_item = ShopItem.objects.create(name="Non Digital item", currency_cost=10, 
                                                             description = 'non-digital item description',
                                                             image = test_image, is_digital=False)
        
        # URL to buy above item
        self.buy_non_digital_item_url=(reverse('shop:buy_shop_item', args=[self.non_digital_shop_item.item_id]))

        # URL to redeem non-digital shop item
        self.redeem_non_digital_item_url=(reverse('shop:buy_shop_item', args=[self.non_digital_shop_item.item_id]))

        # Creates a test game keeper account
        self.game_keeper = CustomUser.objects.create_user(email ='gamekeeper@gmail.com', 
                                                         username = 'gamekeeper1', 
                                                         password = 'testpassword54321',
                                                         first_name = 'Game',
                                                         last_name = 'Keeper',
                                                         role = 'gameKeeper',
                                                         is_staff = True,
                                                         verified = True)
        

class ShopTest(SetUpTest):
    # Verifies a user can access the page, and it displays the correct content, if logged in
    def test_user_can_access_page(self):
        # Logins as test player, and tests if they can access the shop page
        self.client.login(username='player1', password='testpassword12345')
        response = self.client.get(self.shop_url)

        # Verifies the correct page is rendered
        self.assertEqual(response.status_code, 200) 
        self.assertTemplateUsed(response, 'shop/shop.html')

        # Verifies the page displays the correct items
        self.assertIn(self.digital_shop_item, response.context['items'])
        self.assertIn(self.non_digital_shop_item, response.context['items'])

    # Verifies the user can buy digital items, and the correct data is stored in the db
    def test_buy_digital_item(self): 
        # Logins as test player, and can buy digital item
        self.client.login(username='player1', password='testpassword12345')
        response = self.client.get(self.buy_digital_item_url)
        self.player_balance.refresh_from_db()


        self.assertEqual(response.status_code, 302) # Verifies the user is redirected
        self.assertEqual(self.player_balance.currency, 10) # Verifies the balance has 10 instead of 20 currency

        # Verifies a transaction is stored in db, and it has the correct attributes
        test_transaction = CurrencyTransaction.objects.get(transaction_id = 1)
        self.assertEqual(test_transaction.currency_difference, -10)
        self.assertEqual(test_transaction.description, f"Bought {self.digital_shop_item.name}")

        # Verifies the purchase is stored correctly in db
        test_purchase = ItemPurchase.objects.get(purchase_id = 1)
        self.assertEqual(test_purchase.user, self.player)
        self.assertEqual(test_purchase.item, self.digital_shop_item)
        self.assertTrue(test_purchase.is_digital)
        self.assertEqual(test_purchase.redeem_code, None)
        self.assertFalse(test_purchase.is_redeemed)

    # Verifies the user can buy non-digital items, and the correct data is stored in the db
    def test_buy_non_digital_item(self): 
        # Logins as test player, and buy non-digital item
        self.client.login(username='player1', password='testpassword12345')
        response = self.client.get(self.buy_non_digital_item_url)
        self.player_balance.refresh_from_db()

        
        self.assertEqual(response.status_code, 302) # Verifies the user is redirected
        self.assertEqual(self.player_balance.currency, 10) # Verifies the balance has 10 instead of 20 currency

        # Verifies a transaction is stored in db, and it has the correct attributes
        test_transaction = CurrencyTransaction.objects.get(transaction_id = 1)
        self.assertEqual(test_transaction.currency_difference, -10)
        self.assertEqual(test_transaction.description, f"Bought {self.non_digital_shop_item.name}")

        # Verifies the purchase is stored correctly in db
        test_purchase = ItemPurchase.objects.get(purchase_id = 1)
        self.assertEqual(test_purchase.user, self.player)
        self.assertEqual(test_purchase.item, self.non_digital_shop_item)
        self.assertFalse(test_purchase.is_digital)
        self.assertEqual(len(test_purchase.redeem_code), 6)
        self.assertFalse(test_purchase.is_redeemed)

class DisplayRedeemCodeTest(SetUpTest): 
    # Verifies a player can access this page, and if it generates and displays the QR code for a purchase
    def test_display_redeem_qr_code(self):
        # Logins as test player, and buy non-digital item
        self.client.login(username='player1', password='testpassword12345')
        self.client.get(self.buy_non_digital_item_url)

        # Makes temp folder for qr_code, as @override_settings(MEDIA_ROOT=tempfile.mkdtemp()) is in use
        qr_code_dir = os.path.join(settings.MEDIA_ROOT, "qr_codes")
        os.makedirs(qr_code_dir, exist_ok=True)

        # Verifies the purchase's randomly generated redeem code can render the page
        test_purchase = ItemPurchase.objects.get(purchase_id = 1)
        response = self.client.get(reverse('shop:display_redeem_code', args=[test_purchase.redeem_code]))
        self.assertEqual(response.status_code, 200) # Would of been redirected (302) if wrong

        # Verifies the render includes a qr_code and the purchase
        self.assertIn('qr_code', response.context)
        self.assertIn('purchase', response.context)

    # Verifies a non-player can't access this page, even if using correct correct url, and is redirected
    def test_unauthorised_user_redirected(self):
        # Logins as test player, and buy non-digital item, then logout
        self.client.login(username='player1', password='testpassword12345')
        self.client.get(self.buy_non_digital_item_url)
        self.client.logout()

        # Logins as test game keeper, and trys to access page as unauthorised
        self.client.login(username='gamekeeper1', password='testpassword54321')
        test_purchase = ItemPurchase.objects.get(purchase_id = 1)
        response = self.client.get(reverse('shop:display_redeem_code', args=[test_purchase.redeem_code]))

        # Verifies the user is redirect to unauthorised.html page if they can't access page
        self.assertEqual(response.status_code, 302) 
        self.assertRedirects(response, '/shop/unauthorised/')

class RedeemPageTest(SetUpTest): 
    # Verifies a game keeper can access this page
    def test_gamekeeper_can_access_redeem_page(self):
        # Logins as test game keeper, and attempt to access redeem_page
        self.client.login(username='gamekeeper1', password='testpassword54321')
        response = self.client.get(self.redeem_page_url)
        self.assertEqual(response.status_code, 200) 

    # Verifies a player can't access this page
    def test_player_cant_access_redeem_page(self):
        # Logins as test player, and attempt to access redeem_page
        self.client.login(username='player1', password='testpassword12345')
        response = self.client.get(self.redeem_page_url)

        # Verifies the user is redirected to unauthorised.html page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/shop/unauthorised/')

    # Verifies the game keeper is sent to the correct page, if using the correct code
    def test_gamekeeper_redirect_correctly_using_redeem_code(self):
        # Logins as test player, and buy non-digital item, then logout
        self.client.login(username='player1', password='testpassword12345')
        self.client.get(self.buy_non_digital_item_url)
        self.client.logout()

        # Logins as test game keeper, and trys to access redeem_item page by inputing correct redeem 
        # code into redeem_page. 
        self.client.login(username='gamekeeper1', password='testpassword54321')
        test_purchase = ItemPurchase.objects.get(purchase_id = 1)
        response = self.client.post(self.redeem_page_url, {'redeem_code':test_purchase.redeem_code})

        # Verifies the game keeper is redirected to the correct page for redeeming items
        self.assertEqual(response.status_code, 302)
        redeem_item_url = reverse('shop:redeem_item', args=[test_purchase.redeem_code])
        self.assertRedirects(response, redeem_item_url)

    # Verifies the gamekeeper is informed with the correct message if they input invalid code
    def test_inform_gamekeeper_invalid_redeem_code(self):
        # Logins as test game keeper, and input wrong code into redeem page
        self.client.login(username='gamekeeper1', password='testpassword54321')
        response = self.client.post(self.redeem_page_url, {'redeem_code': 'invald'}) # Lowercase letters are never used for redeem code

        # Checks if view attempts render and displays correct message
        self.assertEqual(response.status_code, 200) 
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Invalid redeem code, please try again.')

class RedeemItemTest(SetUpTest):
    # Verifies a gamekeeper can access the redeem item page if using the correct code
    def test_gamekeeper_can_access_redeem_item(self):
        # Logins as test player, and buy non-digital item, then logout
        self.client.login(username='player1', password='testpassword12345')
        self.client.get(self.buy_non_digital_item_url)
        self.client.logout()

        # Logins as test game keeper, and verifies they can access redeem_item page using correct redeem code
        self.client.login(username='gamekeeper1', password='testpassword54321')
        test_purchase = ItemPurchase.objects.get(purchase_id = 1)
        redeem_item_url = reverse('shop:redeem_item', args=[test_purchase.redeem_code])
        response = self.client.get(redeem_item_url)
        self.assertEqual(response.status_code, 200)

    # Verifies a player can't access the redeem_item page, and is redirect to the correct page
    def test_player_cant_access_redeem_item(self):
        # Logins as test player, and buy non-digital item, then attempt to access redeem item page
        self.client.login(username='player1', password='testpassword12345')
        self.client.get(self.buy_non_digital_item_url)
        test_purchase = ItemPurchase.objects.get(purchase_id = 1)
        redeem_item_url = reverse('shop:redeem_item', args=[test_purchase.redeem_code])
        response = self.client.get(redeem_item_url)

        # Verifies the user is redirected to unauthorised page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/shop/unauthorised/')

    # Verifies a game keeper can redeem an item through POST, and the item is redeemed, and if they are redirected
    def test_gamekeeper_can_redeem_item(self):
        # Logins as test player, and buy non-digital item, then logout
        self.client.login(username='player1', password='testpassword12345')
        self.client.get(self.buy_non_digital_item_url)
        self.client.logout()

        # Logins as test game keeper, and accesses redeem_item 
        self.client.login(username='gamekeeper1', password='testpassword54321')
        test_purchase = ItemPurchase.objects.get(purchase_id = 1)
        redeem_item_url = reverse('shop:redeem_item', args=[test_purchase.redeem_code])

        response = self.client.post(redeem_item_url) # Cause a post response on view

        # Verifies the purchase has been redeemed
        test_purchase.refresh_from_db()
        self.assertEqual(test_purchase.is_redeemed, True)

        # Verifies theredirected to the correct page
        redeemed_url = reverse('shop:redeemed')
        self.assertRedirects(response, redeemed_url)

