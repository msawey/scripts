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
from  django.core.exceptions import
from pprint import pprint

THREAT_MODEL_FILE_PATH = '/Users/msawey/threatstream/scripts/data.json'
ASSOCIATION_FILE_PATH = '/Users/msawey/threatstream/scripts/associations.json'

def get_threat_models():
    data = get_data(THREAT_MODEL_FILE_PATH)
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
    return actors, ttps, tip_reports

def get_data(file_path):
    try:
        print(os.path.abspath(os.path.dirname(sys.argv[0])))
        with open(file_path) as data_file:
            objects = json.load(data_file)
            data = objects.get("objects")
            return data
    except Exception as e:
        print(e)
        print("File does not exist")
        print(file_path)
        quit()

def get_association_data():
    return get_data(ASSOCIATION_FILE_PATH)

def add_association_data(associations):
    for association in associations:
        try:
            if association.get("type1") == 'actor':
                actor = Actor.objects.get(id=association.get("id1"))
                add_threat_model_association(actor, association)
            if association.get("type1") == 'ttp':
                ttp = Ttp.objects.get(id=association.get("id1"))
                add_threat_model_association(ttp, association)
            if association.get("type1") == 'tipreport':
                tipreport = TipReport.objects.get(id=association.get("id1"))
                add_threat_model_association(tipreport, association)
        except:
            print("Threat Model does not exist")

def add_threat_model_association(threat_model, association):
    try:
        if association.get("type2") == 'actor':
            threat_model.actors.add(association.get("id2"))
        elif association.get("type2") == 'ttp':
            threat_model.ttps.add(association.get("id2"))
        elif association.get("type2") == 'tipreport':
            threat_model.tipreports.add(association.get("id2"))
    except:
        print("Association does not exist")

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
        actor_soph_type = actor.get("soph_type")
        if actor_soph_type:
            actor_soph_type_id = actor_soph_type.get("id")
        else:
            actor_soph_type_id = None
        actor_owner_user = actor.get("owner_user")
        if actor_owner_user:
            actor_owner_user_id = actor_owner_user.get("id")
        else:
            actor_owner_user_id = None
        obj_actor, created = Actor.objects.get_or_create(\
            name=actor["name"][:255],\
            tlp=actor.get("tlp"),\
            start_date=actor.get("start_date"),\
            soph_type_id=actor_soph_type_id,\
            description=actor.get("description"),\
            organization_id=actor.get("organization_id"),\
            owner_user_id=actor_owner_user_id\
            )
        add_actor_aliases(obj_actor, actor.get("aliases"))
        add_actor_motivations(obj_actor, actor.get("motivations"))
        add_actor_victims(obj_actor, actor.get("victims"))
        obj_actor.add_tags(actor.get("tags_v2"), get_user_org(actor.get("organization_id")))
        obj_actor.save()

def add_actor_aliases(actor, aliases):
    for alias in aliases:
        ActorAlias.objects.get_or_create(actor_id=actor.id, name=alias.get("name"))

def add_actor_motivations(actor, motivations):
    for motivation in motivations:
        #TODO m_type_id to use .get()
        ActorMotivation.objects.get_or_create(actor_id=actor.id, description=motivation.get("description"), m_type_id=motivation["m_type"]["id"])

def add_actor_victims(actor, victims):
    for victim in victims:
        victim_type = VictimType.objects.get(id=victim.get("id"))
        actor.victims.add(victim_type)

def add_actor_(actors):
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
            name=ttp.get("name"),\
            tlp=ttp.get("tlp"),\
            description=ttp.get("description"),\
            organization_id=ttp.get("organization_id")\
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

User_Organizations = UserOrganization.objects.get_query_set()

threat_models = get_threat_models()
actors, ttps, tip_reports = threat_models
if actors:
    add_actors(actors)

#add_actor_relations(actors)

if ttps:
    add_ttps(ttps)

if tip_reports:
    add_tip_reports(tip_reports)

associations = get_association_data()
pprint(associations)
add_association_data(associations)
