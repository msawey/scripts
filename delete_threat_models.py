from ts.tsdb.models import (
    Actor,
    Ttp,
    TipReport
)

def delete_threat_models():
    actors = Actor.objects.get_query_set()
    for actor in actors:
        actor.delete()
    ttps = Ttp.objects.get_query_set()
    for ttp in ttps:
        ttp.delete()
    tipreports = TipReport.objects.get_query_set()
    for tipreport in tipreports:
        tipreport.delete()

delete_threat_models()

