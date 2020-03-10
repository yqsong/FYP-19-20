from django.http import HttpResponse
from django.shortcuts import render
from .forms import RelationSupportCSVDatasetForm, QueriesCSVDatasetForm, TextDatasetForm, NewsArticleURLForm
import json
from django.views.decorators.cache import never_cache
import os
import sys
sys.path.insert(0, os.environ['FEWREL_PATH'])
from fyp_detection_framework import DetectionFramework
from threading import Thread


@never_cache
def home(request):
    """
        Renders the home page of the app.
    """
    rel_sup_csv_form = RelationSupportCSVDatasetForm()
    queries_csv_form = QueriesCSVDatasetForm()
    text_file_form = TextDatasetForm()
    article_url_form = NewsArticleURLForm()
    data = []
    for i in results:
        data.append({'sentence':i[0], 'head':i[1], 'tail':i[2], 'pred_relation':i[3], 'pred_sentiment':i[5], 'conf':i[6]})
    ckpts = [f for f in os.listdir(os.environ['FEWREL_PATH'] + "/checkpoint") if '.pth.tar' in f]
    return render(request, 'home.html', {'rel_sup_csv_form': rel_sup_csv_form, 'queries_csv_form': queries_csv_form, 'text_file_form': text_file_form, 'article_url_form': article_url_form, 'data': data, 'ckpts': ckpts})


def handle_uploaded_file(f, fname):
    """
        Takes the uploaded files and saves them appropriately to disk.
    """
    with open(fname, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def rel_sup_csv_upload(request):
    """
        Uploads the selected relation support dataset from the user.
    """
    if request.method == "POST":
        relation_support_dataset = request.FILES['relation_support_dataset']
        handle_uploaded_file(relation_support_dataset, 'temp/relation_support_dataset.csv')

        return HttpResponse(
            json.dumps({'success':'success'}),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"error": "error, GET request not supported"}),
            content_type="application/json"
        )

def query_csv_upload(request):
    """
        Uploads the selected queries CSV dataset from the user.
    """
    if request.method == "POST":
        queries_dataset = request.FILES['queries_dataset']
        handle_uploaded_file(queries_dataset, 'temp/queries.csv')

        return HttpResponse(
            json.dumps({'success':'success'}),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"error": "error, GET request not supported"}),
            content_type="application/json"
        )

def text_file_upload(request):
    """
        Uploads the text file dataset from the user.
    """
    if request.method == "POST":
        queries_dataset = request.FILES['text_file']
        handle_uploaded_file(queries_dataset, 'temp/queries.txt')

        return HttpResponse(
            json.dumps({'success':'success'}),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"error": "error, GET request not supported"}),
            content_type="application/json"
        )
    
def select_news_article(request):
    """
        Saves the news article url selected by the user.
    """
    global results
    if request.method == "POST":
        print(list(request.POST.items()))
        article_url = request.POST.get('article_url')
        with open('temp/url.txt', 'w') as f:
            f.write(article_url)

        return HttpResponse(
            json.dumps({'success':'success'}),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"error": "error, GET request not supported"}),
            content_type="application/json"
        )


currently_analyzing = False  #flag indicating whether the analysis is currently running or not
results = []  #list of the results which have been generated so far
cancel_flag=[False]  #flag used to indicate whether the analysis should be cancelled or not
errors = []  #list of the errors whcih have been generated
error_i = 0  #index from which new errors can be sent
d = None #
def do_analysis(ckpt, queries_type):
    """
        Runs the actual analysis in a different thread
    """
    global currently_analyzing, results, d
    try:
        print("starting analysis!")
        currently_analyzing = True
        results = []
        ckpt = os.environ['FEWREL_PATH'] + "/checkpoint/" + ckpt
        if d is None or d.ckpt_path != ckpt:
            d = DetectionFramework(ckpt_path=ckpt)
            
        d.clear_support_queries()
        if not os.path.exists("temp/relation_support_dataset.csv"):
            raise ValueError("Please upload relation support dataset!")
            
        d.load_support("temp/relation_support_dataset.csv", K=5)
        if queries_type == "csv_option":
            if not os.path.exists("temp/queries.csv"):
                raise ValueError("Please upload query CSV dataset!")
            d.load_queries_csv("temp/queries.csv")
        elif queries_type == "url_option":
            if not os.path.exists("temp/url.txt"):
                raise ValueError("Please specify news article url!")
            pass #TODO
        elif queries_type == "txt_option":
            if not os.path.exists("temp/queries.txt"):
                raise ValueError("Please upload queries text file!")
            pass #TODO

        d.detect(rt_results=results, cancel_flag=cancel_flag)
        currently_analyzing = False
    except ValueError as e:
        errors.append(str(e))
    finally:
        currently_analyzing = False
    

def start_analysis(request):
    """
        Starts the analysis process
    """
    if request.method == "GET":

        if not currently_analyzing:
            cancel_flag[0] = False
            t = Thread(target=do_analysis, args=(request.GET.get('ckpt'),request.GET.get('queries_type'),))
            t.start()
            return HttpResponse(
                json.dumps({"success": "analysis started"}),
                content_type="application/json"
            )
        else:
            return HttpResponse(
                json.dumps({"error": "error, analysis already running"}),
                content_type="application/json"
            )
    else:
        return HttpResponse(
            json.dumps({"error": "error, POST request not supported"}),
            content_type="application/json"
        )
        
        

def get_analysis_results(request):
    """
        Returns the periodic analysis results as a specific json list
    """
    global error_i
    if not currently_analyzing and len(results) == 0 and error_i >= len(errors):
        return HttpResponse(
            json.dumps({'status':'analysis_not_running'}),
            content_type="application/json"
        )
    elif error_i < len(errors):
        from_i = error_i
        error_i = len(errors)
        return HttpResponse(
            json.dumps({'status':'error',
                       'errors':errors[from_i:]}),
            content_type="application/json"
        )
    else:
        client_index_till = int(request.GET.get('cur_index_reached', 0))
        new_data = []
        for i in results[client_index_till:]:
            new_data.append({'sentence':i[0], 'head':i[1], 'tail':i[2], 'pred_relation':i[3], 'pred_sentiment':i[5], 'conf':i[6]})
        status = 'analysis_in_progress'
        if not currently_analyzing:
            status = 'finished_analysis'
        return HttpResponse(
            json.dumps({'status':status, 'new_data':new_data}),
            content_type="application/json"
        )
    
def cancel_analysis(request):
    """
        Cancels the analysis if it is currently running.
    """
    cancel_flag[0] = True
    if not currently_analyzing:
        return HttpResponse(
            json.dumps({'error':"error"}),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({'success':"success"}),
            content_type="application/json"
        )