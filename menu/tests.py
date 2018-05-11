import datetime
import pytz

from django.urls import reverse
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User

from .models import Menu, Item, Ingredient 
from menu.forms import MenuForm, ItemForm 



exp_date = datetime.datetime(2018,10,10,tzinfo=pytz.timezone('Australia/Adelaide'))
menu_data_1 = {
    'season': 'Summer',
    'expiration_date': exp_date
}

menu_data_2 = {
    'season': 'Winter',
    'expiration_date': exp_date
}

user_data = {'username': 'stmcintos',
             'first_name': 'stuart',
             'last_name': 'mcintosh',
             'email': 's.mcintosh@test.com',
             'password': 'XGEyPfoMRNYTo7A#yWLnKEht',
             }

ingredient_1 = Ingredient(name='chocolate')
ingredient_1.save()
ingredient_2 = Ingredient(name='strawberry')
ingredient_2.save()
       

     
# test the model
class MenuViewsTests(TestCase):
    ''' testing of the menu model '''
    def setUp(self):
        ''' setup up dummy data in our model '''
        self.user_1 = User.objects.create_user(**user_data)

        self.item_1 = Item(
        name='Menu item',
        description='topping',
        chef=self.user_1
        )
        self.item_1.save()

        self.item_1.ingredients.add(ingredient_1, ingredient_2)
        self.menu_1 = Menu.objects.create(**menu_data_1)
        self.menu_1.items.add(self.item_1)
        self.menu_2 = Menu.objects.create(**menu_data_2)
        self.menu_2.items.add(self.item_1)

    def test_menu_creation(self):
        ''' test out the creation of our model '''
        menu = Menu.objects.get(season="Summer")
        self.assertEqual(menu, self.menu_1)
        menu = Menu.objects.get(season="Winter")
        self.assertEqual(menu, self.menu_2)

    def test_menu_list_view(self):
        test =  '<title>Soda FountainSoda Fountain - Menus All</title>'
        resp = self.client.get(reverse('menu:menu_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.menu_1, resp.context['menus'])
        self.assertIn(self.menu_2, resp.context['menus'])
        self.assertTemplateUsed(resp, 'menu/list_all_current_menus.html')
        print(resp.context)
        self.assertContains(resp, test)
       
        
    # def test_menu_detail_view(self):
    #     test =  '<title>Soda Fountain - Menu Details </title>\n'
    #     resp = self.client.get(reverse('menu:menu_detail',
    #         kwargs={'pk': self.menu_1.pk}))
    #     self.assertEqual(resp.status_code, 200)
    #     self.assertEqual(self.menu_1, resp.context['menus'])
    #     self.assertTemplateUsed(resp, 'menu/menu_detail.html')

    #     self.assertContains(resp, test)
       
    # def test_create_new_menu_view_GET(self):
    #     test = '<title>Soda Fountain - Edit Menu</title>'
    #     resp = self.client.get(reverse('menu:menu_new'))
    #     self.assertEqual(resp.status_code, 200)
    #     print(resp.content)
    #     self.assertContains(resp, test)
    
    # def test_create_new_menu_view_POST(self):
    #     test = '<title>Soda Fountain - Edit Menu</title>'
    #     resp = self.client.post(reverse('menu:menu_new'))
    #     self.assertEqual(resp.status_code, 200)
    #     self.assertContains(resp, test)

    # def test_edit_menu_view_GET(self):
    #     test = '<title>Soda Fountain - Edit Menu</title>'
    #     resp = self.client.get(reverse('menu:menu_edit',
    #         kwargs={'pk': self.menu_1.pk}))
    #     self.assertEqual(resp.status_code, 200)
    #     self.assertContains(resp, test)

    # def test_edit_menu_view_POST(self):
    #     resp = self.client.post(reverse('menu:menu_edit',
    #         kwargs={'pk': self.menu_1.pk}))
    #     self.assertEqual(resp.status_code, 200)

# class ItemViewsTest(TestCase):
#     def test_item_detail_view(self):
#         resp = self.client.get(reverse('imenu:tem_detail',
#             kwargs={'pk': self.item1.pk}))
#         self.assertEqual(resp.status_code, 200)
#         self.assertTemplateUsed('menu/detail_item.html')

#     def test_item_detail_view_404(self):
#         resp = self.client.get(reverse('menu:item_detail', kwargs={'pk': 1}))
#         self.assertEqual(resp.status_code, 404)
#         self.assertTemplateUsed('menu/detail_item.html')


class IngredientViewsTest(TestCase):
    pass


# #################################
# ########## Form Tests ##########
# #################################
# class MenuFormsTest(TestCase):
#     def test_menu_create_form_good_data(self):
#         form_data = {'season': 'Winter',
#             'items': self.item1,
#             'expiration_date': '10/10/2019'
#         }
#         form = MenuForm(data=form_data)
#         self.assertTrue(form.is_valid())
#         menu = form.save()
#         self.assertEqual(menu.season, 'Winter')
#         self.assertEqual(menu.expiration_date, '10/10/2019')
#         self.assertEqual(menu.items, self.item1)

#     def test_menu_create_form_blank_data(self):
#         form = MenuForm(data={})
#         self.assertFalse(form.is_valid())


# #################################
# ########## Model Tests ##########
# #################################
# class MenuModelTest(TestCase):
#     def test_menu_creation(self):
#         menu = Menu.objects.create(**menu_data1)
#         self.assertEqual(menu.season, 'Summer')