from ts.tsdb.models import Actor
from ts.tsdb.models import ActorAlias
from ts.tsdb.models import ActorMotivation
from ts.tsdb.models import VictimType
from ts.tsdb.models import Ttp
from ts.tsdb.models import TtpAlias
from ts.tsdb.models import BehaviorMalware
from ts.tsdb.models import BehaviorAttackPattern
from ts.tsdb.models import BehaviorExploit
from ts.tsdb.models import TipReport
import json
from psycopg2.extras import Json
from pprint import pprint

class Org:
    def __init__(self, id):
        self.id = id

def get_data():
    try:
        with open('scripts/actor.json') as data_file:
            data = json.load(data_file)
            print("DATA TYPE")
            print(type(data))
            return data
    except:
        print("File does not exist")
        quit()

def get_actors(data):
    return data["Actors"]

def get_ttps(data):
    return data["TTPs"]

def get_tip_reports(data):
    return data["Tip_Reports"]

def add_actors(actors):
    for actor in actors:
        # TODO
        # tags_v2 ask Andy
        print("TAGS")
        pprint(actor["tags_v2"])
        print(type(Json(actor["tags_v2"])))
        Actor.objects.get_or_create(name=actor["name"],\
#            tags_v2=Json(actor["tags_v2"]),\
            tlp=actor["tlp"],\
            start_date=actor["start_date"],\
            soph_type_id=actor["soph_type"]["id"],\
            description=actor["description"],\
            organization_id=actor["organization_id"],\
            owner_user_id=actor["owner_user"]["id"]\
            )
        # Come back to
        org = Org(1)
        obj_actor = Actor.objects.get(name=actor["name"], organization_id=actor["organization_id"])
#        add_actor_tags(obj_actor, actor["tags_v2"], org)
        add_actor_aliases(obj_actor, actor["aliases"])
        add_actor_motivations(obj_actor, actor["motivations"])
        add_actor_victims(obj_actor, actor["victims"])

# TODO: Tags
# Possibly re-usable for TTPs etc.
#def add_actor_tags(actor, tags, org):
#    print("Org ID")
#    print(org.id)
#    actor.add_tags(tags, org)

def add_actor_aliases(actor, aliases):
    for alias in aliases:
        ActorAlias.objects.get_or_create(actor_id=actor.id, name=alias["name"])

def add_actor_motivations(actor, motivations):
    for motivation in motivations:
        ActorMotivation.objects.get_or_create(actor_id=actor.id, description=motivation["description"], m_type_id=motivation["m_type"]["id"])

def add_actor_victims(actor, victims):
    for victim in victims:
        victim_type = VictimType.objects.get(id=victim["id"])
        actor.victims.add(victim_type)

def add_actor_relations(actors):
    for actor in actors:
        if (actor["Actors"]):
            # TODO
            # Test with non existent actors
            # Handle error
            obj_actor = Actor.objects.get(name=actor["name"])
            for actor_actor in actor["Actors"]:
                obj_actor.actors.add(Actor.objects.get(name=actor_actor))

def add_ttps(ttps):
    for ttp in ttps:
        obj_ttp = Ttp.objects.get_or_create(\
            name=ttp["name"],\
#            TAGS
            tlp=ttp["tlp"],\
            # behavior_malware
            description=ttp["description"],\
            organization_id=ttp["organization_id"]\
            )
        obj_ttp = Ttp.objects.get(name=ttp["name"], organization_id=ttp["organization_id"])
        add_ttp_aliases(obj_ttp, ttp["aliases"])
        add_ttp_behavior_malware(obj_ttp, ttp["behavior_malware"])
        add_ttp_behavior_attackpatterns(obj_ttp, ttp["behavior_attackpatterns"])
        add_ttp_behavior_exploits(obj_ttp, ttp["behavior_exploits"])

def add_ttp_aliases(ttp, aliases):
    for alias in aliases:
        TtpAlias.objects.get_or_create(ttp_id=ttp.id, name=alias["name"])

def add_ttp_behavior_malware(ttp, malwares):
    for malware in malwares:
       BehaviorMalware.objects.get_or_create(name=malware["name"], m_type_id=malware["m_type"]["id"], notes=malware["notes"], ttp_id=ttp.id)

def add_ttp_behavior_attackpatterns(ttp, patterns):
    for pattern in patterns:
        BehaviorAttackPattern.objects.get_or_create(name=pattern["name"], notes=pattern["notes"], ttp_id=ttp.id)

def add_ttp_behavior_exploits(ttp, exploits):
    for exploit in exploits:
       BehaviorExploit.objects.get_or_create(name=exploit["name"], notes=exploit["notes"], ttp_id=ttp.id)

def add_tip_reports(tip_reports):
    for tip_report in tip_reports:
        TipReport.objects.get_or_create(\
            name=tip_report["name"],\
            tlp=tip_report["tlp"],\
            source=tip_report["source"])


data = get_data()
# print("RETURNED DATA TPYE")
# print(type(data))
# actors = get_actors(data)
# add_actors(actors)
# #add_actor_relations(actors)
# 
# ttps = get_ttps(data)
# add_ttps(ttps)

tip_reports = get_tip_reports(data)
add_tip_reports(tip_reports)
