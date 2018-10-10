from ts.tsdb.models import Actor
import json
from pprint import pprint

with open('scripts/data.json') as data_file:
    data = json.load(data_file)
    print("Data loaded")
    print(data)

print("Data outside of with")
print(data)

actors = data["Actors"]

for actor in actors:
    print("Actor")
    print(actor)
    Actor.objects.get_or_create(name=actor["name"], organization_id=actor["organization_id"], owner_user_id=actor["owner_user_id"])
else:
    print("Loop done")

for actor in actors:
    if (actor["Actors"]):
        print("Actors")
        print(actor)
        obj_actor = Actor.objects.get(name=actor["name"])
        for actor_actor in actor["Actors"]:
            obj_actor.actors.add(Actor.objects.get(name=actor_actor))
else:
    print("2 Loop Done")

print("TEST PASSED")
