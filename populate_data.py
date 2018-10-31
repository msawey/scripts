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
from ts.tsdb.models import UserOrganization
import json
import os
import sys
from psycopg2.extras import Json
from pprint import pprint

def get_threat_models(data):
    actors = []
    ttps = []
    tip_reports = []
    for threat_model in data:
        if threat_model["model_type"] == "actor":
            actors.append(threat_model)
        if threat_model["model_type"] == "ttp":
            ttps.append(threat_model)
        if threat_model["model_type"] == "tipreport":
            tip_reports.append(threat_model)
    return (actors, ttps, tip_reports)

def get_data():
    try:
        print(os.path.abspath(os.path.dirname(sys.argv[0])))
        with open('/Users/msawey/threatstream/scripts/data.json') as data_file:
            objects = json.load(data_file)
            data = objects.get("objects")
            return data
    except Exception as e:
        print(e)
        print("File does not exist")
        quit()

def get_actors(data):
    actors = []
    for threat_model in data:
        if threat_model["model_type"] == "actor":
            actors.append(threat_model)
    return data.get("Actors")

def get_ttps(data):
    return data.get("TTPs")

def get_tip_reports(data):
    return data.get("Tip_Reports")

def get_user_org(id):
    for user_org in User_Organizations:
        if user_org.id == id:
            return user_org

def add_actors(actors):
    for actor in actors:
        obj_actor, created = Actor.objects.get_or_create(name=actor["name"],\
            tlp=actor["tlp"],\
            start_date=actor["start_date"],\
            soph_type_id=actor["soph_type"]["id"],\
            description=actor["description"],\
            organization_id=actor["organization_id"],\
            owner_user_id=actor["owner_user"]["id"]\
            )
        add_actor_aliases(obj_actor, actor["aliases"])
        add_actor_motivations(obj_actor, actor["motivations"])
        add_actor_victims(obj_actor, actor["victims"])
        obj_actor.add_tags(actor["tags_v2"], get_user_org(actor["organization_id"]))
        obj_actor.save()

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
        obj_ttp, created = Ttp.objects.get_or_create(\
            name=ttp["name"],\
            tlp=ttp["tlp"],\
            description=ttp["description"],\
            organization_id=ttp["organization_id"]\
            )
        add_ttp_aliases(obj_ttp, ttp["aliases"])
        add_ttp_behavior_malware(obj_ttp, ttp["behavior_malware"])
        add_ttp_behavior_attackpatterns(obj_ttp, ttp["behavior_attackpatterns"])
        add_ttp_behavior_exploits(obj_ttp, ttp["behavior_exploits"])
        obj_ttp.add_tags(ttp["tags_v2"], get_user_org(ttp["organization_id"]))
        obj_ttp.save()

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
        obj_tip_report, created = TipReport.objects.get_or_create(\
            name=tip_report["name"],\
            tlp=tip_report["tlp"],\
            source=tip_report["source"]\
        )
        obj_tip_report.add_tags(tip_report["tags_v2"], get_user_org(tip_report["owner_org_id"]))
        obj_tip_report.save()

data = get_data()
User_Organizations = UserOrganization.objects.get_query_set()

threat_models = get_threat_models(data)
actors, ttps, tip_reports = threat_models

if actors:
    add_actors(actors)

#add_actor_relations(actors)

#ttps = get_ttps(data)
if ttps:
    add_ttps(ttps)

#tip_reports = get_tip_reports(data)
if tip_reports:
    add_tip_reports(tip_reports)
