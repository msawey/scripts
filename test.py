import unittest
from unittest import TestCase
import os
import json
from pprint import pprint
import logging

OUTPUR_DIR = '/Data'
EXPECTED_DATA_DIR = '/ExpectedData'
ACTOR_FILE_NAME = '/actor.json'
TTP_FILE_NAME = '/ttp.json'
TIPREPORT_FILE_NAME = '/tipreport.json'
ACTORS_OUTPUT = []
ACTORS_EXPECTED = []
TTPS_OUTPUT = []
TTPS_EXPECTED = []
TIPREPORTS_OUTPUT = []
TIPREPORTS_EXPECTED = []
EXPECTED_FILE = []

def testSetup():
    pass

def get_objects(file):
    return json.load(file).get('objects',[])

class TestOutputFile(TestCase):
    @classmethod
    def setUpClass(cls):
        global ACTORS_OUTPUT, ACTORS_EXPECTED, TTPS_OUTPUT, TTPS_EXPECTED, TIPREPORTS_OUTPUT, TIPREPORTS_EXPECTED

        actor_file_path = os.getcwd() + OUTPUR_DIR + ACTOR_FILE_NAME
        print(actor_file_path)
        with open(actor_file_path) as actor_file:
            ACTORS_OUTPUT = get_objects(actor_file)

        ttp_file_path = os.getcwd() + OUTPUR_DIR + TTP_FILE_NAME
        with open(ttp_file_path) as ttp_file:
            TTPS_OUTPUT = get_objects(ttp_file)

        tipreport_file_path = os.getcwd() + OUTPUR_DIR + TIPREPORT_FILE_NAME
        with open(tipreport_file_path) as tipreport_file:
            TIPREPORTS_OUTPUT = get_objects(tipreport_file)

        actor_expected_file_path = os.getcwd() + EXPECTED_DATA_DIR + ACTOR_FILE_NAME
        with open(actor_expected_file_path) as actor_expected_file:
            ACTORS_EXPECTED = get_objects(actor_expected_file)

        ttp_expected_file_path = os.getcwd() + EXPECTED_DATA_DIR + TTP_FILE_NAME
        with open(ttp_expected_file_path) as ttp_expected_file:
            TTPS_EXPECTED = get_objects(ttp_expected_file)

        tipreport_expected_file_path = os.getcwd() + EXPECTED_DATA_DIR + TIPREPORT_FILE_NAME
        with open(tipreport_expected_file_path) as tipreport_expected_file:
            TIPREPORTS_EXPECTED = get_objects(tipreport_expected_file)

    def test_actors(self):
        self.assertEqual(len(ACTORS_EXPECTED), len(ACTORS_OUTPUT))
        for expected_actor in ACTORS_EXPECTED:
            if (expected_actor['model_type'] != 'actor'):
                continue
            for output_actor in ACTORS_OUTPUT:
                if expected_actor.get('name') != output_actor.get('name') or\
                        expected_actor.get('organization_id') != output_actor.get('organization_id'):
                    continue
                print('Testing ' + expected_actor['name'] + ' and ' + output_actor['name'])
                self.assertEqual(expected_actor['name'], output_actor['name'])
                self.assertEqual(expected_actor['tlp'], output_actor['tlp'])
                self.assertEqual(expected_actor['start_date'], output_actor['start_date'])
                self.assertEqual(expected_actor.get('description'), output_actor.get('description'))
                self.assertEqual(expected_actor.get('organization_id'), output_actor.get('organization_id'))
                expected_aliases = [a['name'] for a in expected_actor.get('aliases')]
                output_aliases = [a['name'] for a in output_actor.get('aliases')]
                self.assertEqual(set(expected_aliases), set(output_aliases))
                expected_operation_types = [a['a_type'] for a in expected_actor.get('types')]
                expected_operation_type_ids = [a['id'] for a in expected_operation_types]
                output_operation_types = [a['a_type'] for a in output_actor.get('types')]
                output_operation_types_ids = [a['id'] for a in output_operation_types]
                self.assertEqual(set(expected_operation_type_ids), set(output_operation_types_ids))
                expected_victim_ids = [a['id'] for a in expected_actor.get('victims')]
                output_victim_ids = [a['id'] for a in output_actor.get('victims')]
                self.assertEqual(set(expected_victim_ids), set(output_victim_ids))
                expected_tag_ids = [a['id'] for a in expected_actor.get('tags_v2')]
                output_tag_ids = [a['id'] for a in output_actor.get('tags_v2')]
                self.assertEqual(set(expected_tag_ids), set(output_tag_ids))
                self.assertEqual(expected_actor.get('soph_type').get('id'), output_actor.get('soph_type').get('id'))
                expected_motivation_type_ids = [a['m_type']['id'] for a in expected_actor.get('motivations')]
                output_motivation_type_ids = [a['m_type']['id'] for a in output_actor.get('motivations')]
                self.assertEqual(set(expected_motivation_type_ids), set(output_motivation_type_ids))
                break

    def test_ttps(self):
        self.assertEqual(len(TTPS_EXPECTED), len(TTPS_OUTPUT))
        for expected_ttp in TTPS_EXPECTED:
            if expected_ttp['model_type'] != 'ttp':
                continue
            for output_ttp in TTPS_OUTPUT:
                if expected_ttp.get('name') != output_ttp.get('name') or \
                        expected_ttp.get('organization_id') != output_ttp.get('organization_id'):
                    print("HIT")
                    continue
                self.assertEqual(expected_ttp.get('name'), output_ttp.get('name'))
                self.assertEqual(expected_ttp.get('tlp'), output_ttp.get('tlp'))
                expected_aliases = [a['name'] for a in expected_ttp.get('aliases')]
                output_aliases = [a['name'] for a in output_ttp.get('aliases')]
                self.assertEqual(set(expected_aliases), set(output_aliases))
                expected_tag_ids = [a['id'] for a in expected_ttp.get('tags_v2')]
                output_tag_ids = [a['id'] for a in output_ttp.get('tags_v2')]
                self.assertEqual(set(expected_tag_ids), set(output_tag_ids))

    def test_tipreports(self):
        self.assertEqual(len(TIPREPORTS_EXPECTED), len(TIPREPORTS_OUTPUT))
        for expected_tipreport in TIPREPORTS_EXPECTED:
            if expected_tipreport.get('model_type') != 'tipreport':
                continue
            for output_tipreport in TIPREPORTS_OUTPUT:
                if expected_tipreport.get('name') != output_tipreport.get('name') or \
                        expected_tipreport.get('organization_id') != output_tipreport.get('organization_id'):
                    print("HIT")
                    continue
                self.assertEqual(expected_tipreport.get('name'), output_tipreport.get('name'))
                self.assertEqual(expected_tipreport.get('tlp'), output_tipreport.get('tlp'))
                self.assertEqual(expected_tipreport.get('source'), output_tipreport.get('source'))
                expected_tag_ids = [a['id'] for a in expected_tipreport.get('tags_v2')]
                output_tag_ids = [a['id'] for a in output_tipreport.get('tags_v2')]
                self.assertEqual(set(expected_tag_ids), set(output_tag_ids))


if __name__ == '__main__':
    unittest.main()
