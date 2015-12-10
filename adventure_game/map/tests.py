from django.test import TestCase, Client
from django.contrib.auth.models import User

# Create your tests here.
class TaskTests(TestCase):

    #Daniel and his daughter login to the account they created last time they
    #went on an adventure.
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.client.login(username='testuser', password='pass')

    #They have selected the adventure to help the wizard and start adventure
    #They now see a page showing them information about the adventure. The
    #estimated time to complete, estimated cost, and any items needed to
    #complete
    def test_preadventure_information(self):
        response = self.client.get('/information/')
        advetnureid = response.context('adventureid')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'map/information.html')
        self.assertEqual(adventureid , '0000')
        
    #They have hit accept and have gone on to the actual adventure
    #They see the wizard asking for help and telling them what's happening to
    #his land.
    def test_story_so_far(self):
        response = self.client.get('/story/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'coreapp/story.html')

    def test_task1(self):


class MapTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.client.login(username='testuser', password='pass')

    def test_(self):
