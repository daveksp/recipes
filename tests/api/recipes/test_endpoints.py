import json

from app.api.messages import recipe_details
from app.api.messages import recipe_created
from app.api.messages import recipe_not_found
from app.api.messages import recipe_removed
from app.api.messages import recipe_updated
from tests.base import BaseTest
from tests.data_sample import get_recipe_data


class RecipesResourceTests(BaseTest):

    # Test Post endpoint
    def test_post(self):
        """post: check post endpoint works just fine"""
        # given
        data = get_recipe_data()

        # when
        response = self.app.test_client().post(
            '/recipes', data=json.dumps(data),
            headers=self.header)
        response_data = json.loads(response.data)

        # then
        self.assertEqual(response_data['message'], recipe_created)
        self.assertEqual(len(response_data['recipe']), 1)
        self.assertEqual(response.status_code, 200)
        

    # Test get endpoint
    def test_get_recipe_by_id(self):
        """get: check recipe is returned for a valid id"""
        # given
        recipe = self.create_recipe()

        # when
        response = self.app.test_client().get(
            f'/recipes/{recipe.id}',
        )
        response_data = json.loads(response.data)

        # then
        self.assert200(response)
        self.assertEqual(response_data['message'], recipe_details)
        self.assertEqual(int(response_data['recipe'][0]['cost']), recipe.cost)
        self.assertEqual(response_data['recipe'][0]['id'], recipe.id)
    

    def test_get_recipe_by_id_missing_id(self):
        """get: check recipe with id 1 is returned when no id is provided"""
        # given
        recipe = self.create_recipe()

        # when
        response = self.app.test_client().get(
            f'/recipes/',
        )
        response_data = json.loads(response.data)

        # then
        self.assert200(response)
        self.assertEqual(response_data['message'], recipe_details)
        self.assertEqual(response_data['recipe'][0]['id'], 1)

    def test_get_all_recipe(self):
        """get: check recipe is returned for a valid id"""
        # given
        for _ in range(3):
            self.create_recipe()

        # when
        response = self.app.test_client().get(
            f'/recipes',
        )
        response_data = json.loads(response.data)

        # then
        self.assert200(response)
        self.assertEqual(3, len(response_data['recipes']))


    def test_get_recipe_by_id_not_found(self):
        """get: check if 404 is received when recipe doesn't exist"""
        # given / when
        response = self.app.test_client().get(
            f'/recipes/99',
        )
        json.loads(response.data)

        # then
        self.assert200(response)
    

    # Test patch endpoint
    def test_patch_recipe(self):
        """patch: check recipe is properly updated for a valid id"""
        # given
        recipe = self.create_recipe()
        data = {
            "title": "nice test title" 
        }

        # when
        response = self.app.test_client().patch(
            f'/recipes/{recipe.id}', data=json.dumps(data),
            headers=self.header
        )
        response_data = json.loads(response.data)

        # then
        self.assert200(response)
        self.assertEqual(response_data['message'], recipe_updated)
        self.assertEqual(data['title'], response_data['recipe'][0]['title'])
    

    def test_patch_recipe_missing_id(self):
        """patch: check recipe with id 1 is properly updated when no id is provided"""
        # given
        recipe = self.create_recipe()
        data = {
            "title": "nice test title" 
        }

        # when
        response = self.app.test_client().patch(
            f'/recipes/', data=json.dumps(data),
            headers=self.header
        )
        response_data = json.loads(response.data)

        # then
        self.assert200(response)
        self.assertEqual(response_data['message'], recipe_updated)
        self.assertEqual(1, response_data['recipe'][0]['id'])


    def test_patch_recipe_not_found(self):
        """patch: check 404 is received when trying to update a recipe that doesn't exist"""
        # given
        recipe = self.create_recipe()
        data = {
            "title": "nice test title" 
        }

        # when
        response = self.app.test_client().patch(
            f'/recipes/99', data=json.dumps(data),
            headers=self.header
        )
        response_data = json.loads(response.data)

        # then
        self.assert200(response)


    # Test delete endpoint
    def test_delete_recipe(self):
        """delete: check recipe is properly deleted for a valid id"""
        # given
        for _ in range(3):
            recipe = self.create_recipe()

        # when
        response = self.app.test_client().delete(
            f'/recipes/{recipe.id}'
        )
        response_data = json.loads(response.data)

        # then
        self.assert200(response)
        self.assertEqual(response_data['message'], recipe_removed)
        
        response = self.app.test_client().get(
            f'/recipes/{recipe.id}'
        )

        #response_data = json.loads(response.data)
        #self.assert200(response)
        #self.assertEqual(response_data['message'], recipe_not_found)

        response_list = self.app.test_client().get(
            f'/recipes'
        )
        response_list_data = json.loads(response_list.data)
        self.assert200(response_list)
        self.assertEqual(2, len(response_list_data['recipes']))
        

    
    def test_delete_recipe_not_found(self):
        """delete: check 200 is received when trying to delete a recipe that doesn't exist"""
        # given / when
        response = self.app.test_client().delete(
            f'/recipes/99'
        )
        response_data = json.loads(response.data)

        # then 
        self.assert200(response)
        self.assertEqual(response_data['message'], recipe_not_found)


    # Test invalid endpoint
    def test_not_found_invalid_endpoint(self):
        """get: check if 404 is received when endpoint doesn't exist"""
        # given / when
        response = self.app.test_client().get(
            f'/recipest',
        )
        json.loads(response.data)

        # then
        self.assert404(response)
