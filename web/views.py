from django.shortcuts import render_to_response
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from models import *
from django.db.models import Q
from django.http import HttpResponse, HttpResponseNotFound
import sys, StringIO
from django.db import connection

def getBasePage():
	return "http://localhost:8000"

def default(request):
	return render_to_response('index.html',{'base_page':getBasePage()})

def show_contig(request,contig_name):
	contig = Contig.objects.get(name=contig_name)
	reads = contig.reads.all()
	translation = contig.get_translation()
	
	return render_to_response('contig.html',{'base_page':getBasePage(),'contig': contig, 'contig_reads': reads, 'translation': translation})

def contig_page(request):
    if request.method=='POST':
        return download_contigs(request)
    else:
        return  show_all_contigs(request)

def sort_query(order_value, order_dict, order_query, desc ):
	if order_value==0 and desc:
		return order_query.reverse()		
	for i in order_dict:
		if order_dict[i]==order_value:
			order_query=order_query.order_by(i).reverse();
			if desc:
				order_query=order_query.reverse()
			break
	return order_query

def sort_query_blastHits(t, desc ):	
	t_aux = t.filter(has_blast_hits=0)
	t = t.filter(has_blast_hits=1)

	t_list_aux = list()
	for i in range(0, len(t)): t_list_aux.append([t[i],len(t[i].blastHits.all())])
	t_list_aux.sort(key = lambda j: j[1])

	t_list=list()
	for i in t_list_aux: t_list.append(i[0])
	
	result=list(t_aux)+t_list
	result.reverse()
	
	if desc: result.reverse()
	
	return result
	
def sort_query_go(t, desc ):
	t_list = list()
	for i in range(1, len(t)): t_list.append([t[i],len(t[i].goAnnotations.all())])
	t_list.sort(key = lambda j: j[1])
	t_list_aux=list()
	for i in t_list: t_list_aux.append(i[0])
	t_list_aux.reverse()
	if desc: t_list_aux.reverse()
	return t_list_aux
	
def download_contigs(request):
    try:
        chk_list=request.POST.getlist('chk')
        contig_list=''
        for i in chk_list:
            c=Contig.objects.get(name=i)
            contig_list+='>'+c.name+'\n'+re.sub("(.{60})", "\\1\n", c.sequence)+'\n'
        fileHandler=StringIO.StringIO(contig_list)
        response= HttpResponse(fileHandler, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=contigs.fasta'
    except:
        response = HttpResponseNotFound()
    return response

def show_translation(request,contig_name):
	translation = Translation.objects.get(name=contig_name)
	return render_to_response('translation.html',{'base_page':getBasePage() ,'translation': translation})

def download_translations(request):
    try:
        chk_list=request.POST.getlist('chk')
        translation_list=''
        for i in chk_list:
            t=Translation.objects.get(name=i)
            translation_list+='>'+t.name+'\n'+re.sub("(.{60})", "\\1\n", t.sequence_translation)+'\n'
        fileHandler=StringIO.StringIO(translation_list)
        response= HttpResponse(fileHandler, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=translations.fasta'
    except:
        response = HttpResponseNotFound()
    return response

def search_translation_page(request):
    if request.method=='POST':
         return download_translations(request)
    else:
         if request.GET.get('auto')=='key':
             return keyword_lookup(request)
	 elif request.GET.get('auto')=='ec':
             return ec_lookup(request)
	 elif request.GET.get('auto')=='go':
             return go_lookup(request)
         else:
             return search_translation(request)

def show_all_pathway(request):

	pathways_to_show = []
	template_results = 'show_pathways.html'
	
	for pathway in Pathway.objects.all():
		reactions_list=[]
		flag = True
		for ec in pathway.reactions.all():
			if len(ec.translation_set.all()) > 0:
				reactions_list.append(str("ec:"+ec.acc))
				break
		if len(reactions_list) > 0: pathways_to_show.append(pathway)
	
	page = request.GET.get('page', 1)
	
	try: page = int(page)
	except ValueError: page = 1
		
	paginator = Paginator(pathways_to_show, 30)
	
	try: objs = paginator.page(page)
	except (EmptyPage, InvalidPage): objs = paginator.page(paginator.num_pages)
	
	return render_to_response(template_results,{'base_page':getBasePage(),'objs': objs} )

#Lookups for autocomplete/suggest 
def keyword_lookup(request):
	results = []
	ec_list=[]
	if request.method == "GET":
		if request.GET.has_key(u'term'):
			value = request.GET[u'term']
                        # Ignore queries shorter than length 3
			if len(value) > 2:
				bh=BlastHit.objects.filter(hit_desc__icontains=value)[0:3000]
				results = [ i.hit_desc for i in bh ]
				x=[]
				xLow=[]
				for i in results:
					for j in re.sub(r';|,|\.|\)|\(|\[|\]|=',' ',i).split(' '):
						if j.lower() not in xLow and '|' not in j:
							x.append(j)
							xLow.append(j.lower())
				keywords=[]
				for i in xLow:
					if value in i:
						keywords.append(x[xLow.index(i)])
	
	json = json_parser(keywords,value)
	return HttpResponse(json, mimetype='text/html')

#Lookup parser
def json_parser(results,value):
	auxlist=[]
	altlist=[]
	results.sort()
	for i in results:
		if value in i[:len(value)]:
			auxlist.append(i)
		else:
			altlist.append(i)

	orderlist=auxlist+altlist

	s="["
	for i in orderlist:
		s+='"'+i+'",'
	s=s[:-1]+"]"
	return s
