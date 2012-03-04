from models import PDAccount, PDRecord
from django.http import HttpResponse
import json
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from provdjango.provmodel import ProvContainer
import logging

logging.basicConfig(level=logging.DEBUG)

def get_prov_json(request):
    from provdjango.provserver.test.testModel import Test
    g1 = Test.w3c_publication_1()
    from models import save_records
    account = save_records(g1)
    
    if 'id' in request.GET:
        entity_id = request.GET.get('id')
        records = PDRecord.objects.filter(rec_id=entity_id)
        accounts = set()
        for record in records:
            accounts.add(record.account)
        # TODO Deal with records from multiple account
        if accounts:
            return HttpResponse(content='{id : %s}' % entity_id, mimetype='application/json')
        return HttpResponse(content='{Not found}', mimetype='application/json')
    else:
#        account = PDAccount.objects.get()
        g2 = account.get_PROVContainer()
        return render_to_response('provserver/test.html', {'json_1' : json.dumps(g1, cls=ProvContainer.JSONEncoder, indent=4),
                                                           'json_2' : json.dumps(g2, cls=ProvContainer.JSONEncoder, indent=4),
                                                           'asn_1': g1.get_asn(),
                                                           'asn_2': g2.get_asn()},
                                  context_instance=RequestContext(request))
#        return HttpResponse(content=simplejson.dumps(graph.to_provJSON(), indent=4), mimetype='application/json')

