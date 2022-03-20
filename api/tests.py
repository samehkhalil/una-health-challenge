from venv import create
from django.urls import reverse
from rest_framework.test import APITestCase
from .models import Level

class LevelDetailTests(APITestCase):
    def create_multiple_level_records(self, user_id):
        Level.objects.bulk_create(
            [
                Level(
                    id='0f40a5b0-5318-4e62-91a2-e2755ba6318f',
                    user_id=user_id,
                    timestamp="2022-03-10 16:20",
                    glucose_value=90
                ),
                Level(
                    id='3f40a5b0-5318-4e62-91a2-e2755ba6318f',
                    user_id=user_id,
                    timestamp="2022-03-08 19:20",
                    glucose_value=80
                ),
            ],
        )

    def test_level_detail_not_found(self):
        response = self.client.get(reverse('level-detail', args=['222']))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'], 'Not found.')
    
    def test_level_detail_found_correct(self):
        record_id = '3f40a5b0-5318-4e62-91a2-e2755ba6318f'
        user_id = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
        self.create_multiple_level_records(user_id)
        record = Level.objects.get(id=record_id)

        response = self.client.get(reverse('level-detail', args=[record_id]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], str(record.id))
        self.assertEqual(response.data['user_id'], str(record.user_id))
        self.assertEqual(response.data['glucose_value'], record.glucose_value)

class LevelListTests(APITestCase):
    """ Tests for Level List GET endpoint """

    def create_multiple_level_records(self, user_id):
        """ helper function to create records """
        Level.objects.bulk_create(
            [
                Level(
                    user_id=user_id,
                    timestamp="2022-03-10 16:20",
                    glucose_value=90
                ),
                Level(
                    user_id=user_id,
                    timestamp="2022-03-08 19:20",
                    glucose_value=80
                ),
                Level(
                    user_id=user_id,
                    timestamp="2022-03-11 15:20",
                    glucose_value=100
                ),
            ],
        )

    def test_level_list_user_id_required(self):
        response = self.client.get(reverse('level-list'))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data[0], 'User ID required')

    def test_level_list_get_empty(self):
        response = self.client.get(reverse('level-list'), {'user_id': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_level_list_get_records_of_user(self):
        user_id = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
        Level.objects.create(
            user_id=user_id,
            timestamp="2022-03-08 19:20",
            glucose_value=90
        )
        response = self.client.get(reverse('level-list'), {'user_id': user_id })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_level_list_filter_by_start(self):
        user_id = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
        self.create_multiple_level_records(user_id)

        response = self.client.get(reverse('level-list'), {'user_id': user_id, 'start': '2022-03-09' })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_level_list_filter_by_stop(self):
        user_id = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
        self.create_multiple_level_records(user_id)
        
        response = self.client.get(reverse('level-list'), {'user_id': user_id, 'stop': '2022-03-11 10:20' })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
    
    def test_level_list_filter_by_start_and_stop(self):
        user_id = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
        self.create_multiple_level_records(user_id)
        
        response = self.client.get(reverse('level-list'), {
            'user_id': user_id, 
            'start': '2022-03-09',
            'stop': '2022-03-11 10:20' },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
    
    def test_level_list_order_by_glucose_value(self):
        user_id = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
        self.create_multiple_level_records(user_id)
        
        response = self.client.get(reverse('level-list'), {
            'user_id': user_id,
            'ordering': 'glucose_value',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['glucose_value'], 80)
    
    def test_level_list_reverse_order_by_timestamp(self):
        user_id = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
        self.create_multiple_level_records(user_id)
        
        response = self.client.get(reverse('level-list'), {
            'user_id': user_id,
            'ordering': '-timestamp',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['glucose_value'], 100)
    
    def test_level_list_supports_limit(self):
        user_id = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
        self.create_multiple_level_records(user_id)
        
        response = self.client.get(reverse('level-list'), {
            'user_id': user_id,
            'limit': 2,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 3)
        self.assertEqual(len(response.data['results']), 2)
        self.assertIsNone(response.data['previous'])
        self.assertIn('offset=2', response.data['next'])


class LevelDetailTests(APITestCase):
    
    def test_prepopulate(self):
        """ Tests the prepopulate POST endpoint"""

        response = self.client.post(reverse('prepopulate'))
        records = Level.objects.all()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(records.count(), 3579)
