from django.shortcuts import render
import json
import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests

with open('fmv_app/states.json') as f:
    states = json.load(f)

with open('fmv_app/district.json') as k:
    dist = json.load(k)

heads = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.51"
}


# Create your views here.
def home(request):
    return render(request, 'home.html', {"data": states['states']})


@api_view(['POST'])
def getDistrict(request):
    data = request.data
    state = data['state']
    distlist = dist[state]
    html = ""
    for i in distlist:
        html = html + "<a class='dropdown-item district-dropdown' id='" + str(i['district_id']) + "'>" + i[
            'district_name'] + "</a>"
    return Response(data={"data": html})


def getid(state, district):
    for i in dist[state]:
        if i['district_name'] == district:
            return i['district_id']


def maketabstrue(data):
    text = ""
    for i in data['centers']:
        text1 = '''
        <div class="card mb-4 shadow-sm">
            <div class="card-header">
                <h4 class="my-0 font-weight-normal">{}</h4>
                <p>{}</p>
            </div>
        <div class="card-body">
        <h1 class="card-title pricing-card-title">{}</h1>
        '''.format(i['name'], i['address'], i['fee_type'])
        text2 = ""
        for y in i['sessions']:
            text2 = text2 + '''
        <ul class="list-unstyled mt-3 mb-4">
            <li><strong>Date</strong>: {}</li>
            <li><strong>Vaccine</strong>: {}</li>
            <li><strong>Available Capacity</strong>: {}</li>
            <li><strong>Age Limit</strong>: {}+</li>
        </ul>
        '''.format(y['date'], y['vaccine'], y['available_capacity'], y['min_age_limit'])
        text3 = '''
        <ul class="list-unstyled mt-3 mb-4">
            <li><strong>Available Slots</strong></li>
            <li>09:00AM-11:00AM</li>
            <li>11:00AM-01:00PM</li>
            <li>01:00PM-03:00PM</li>
            <li>03:00PM-05:00PM</li>
        </ul>
        </div>
        </div>
        '''
        text = text + text1 + text2 + text3
    return text


def maketabsfalse(data):
    text = ""
    for i in data['sessions']:
        text = text + '''
                <div class="card mb-4 shadow-sm">
            <div class="card-header">
                <h4 class="my-0 font-weight-normal">{}</h4>
                <p>{}</p>
            </div>
            <div class="card-body">
                <h1 class="card-title pricing-card-title">{}</h1>
                <ul class="list-unstyled mt-3 mb-4">
                    <li><strong>Date</strong>: {}</li>
                    <li><strong>Vaccine</strong>: {}</li>
                    <li><strong>Available Capacity</strong>: {}</li>
                    <li><strong>Age Limit</strong>: {}+</li>
                </ul>
                <ul class="list-unstyled mt-3 mb-4">
            <li><strong>Available Slots</strong></li>
            <li>09:00AM-11:00AM</li>
            <li>11:00AM-01:00PM</li>
            <li>01:00PM-03:00PM</li>
            <li>03:00PM-05:00PM</li>
        </ul>
            </div>
        </div>
        '''.format(i['name'], i['address'], i['fee_type'], i['date'], i['vaccine'], i['available_capacity'],
                   i['min_age_limit'])
    return text


@api_view(['POST'])
def findByPin(request):
    global text
    data = request.data
    pin = data['pin']
    att = data['att']
    date = data['date']
    date = datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%d-%m-%Y")
    params = {"pincode": pin, "date": date}
    if att == "false":
        try:
            x = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin", params=params,
                             headers=heads)
            xj = x.json()
            if not xj['sessions']:
                text = "<h3>Vaccines Not Available in Your Area</h3>"
            else:
                text = maketabsfalse(x.json())
        except:
            text = "Cowin Servers Seems to Be Busy Check After Some Time"
    else:
        try:
            x = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin",
                             params=params, headers=heads)
            xj = x.json()
            if not xj['centers']:
                text = "<h3>Vaccines Not Available in Your Area</h3>"
            else:
                text = maketabstrue(xj)
        except:
            text = "Cowin Servers Seems to Be Busy Check After Some Time"
        # print(x.json())

    return Response(data={"data": text})


@api_view(['POST'])
def findByDistrict(request):
    global text2
    data = request.data
    state = data['selstate']
    district = data['seldist']
    att = data['att']
    date = data['date']
    date = datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%d-%m-%Y")
    id = getid(state, district)
    params = {"district_id": id, "date": date}
    if att == "false":
        try:
            x = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict",
                             params=params, headers=heads)
            xj = x.json()
            if not xj['sessions']:
                text2 = "<h3>Vaccines Not Available in Your Area</h3>"
            else:
                text2 = maketabsfalse(x.json())
        except:
            text2 = "Cowin Servers Seems to Be Busy Check After Some Time"
    else:
        try:
            x = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict",
                             params=params, headers=heads)
            xj = x.json()
            if not xj['centers']:
                text2 = "<h3>Vaccines Not Available in Your Area</h3>"
            else:
                text2 = maketabstrue(xj)
        except:
            text2 = "Cowin Servers Seems to Be Busy Check After Some Time"
    return Response(data={"data": text2})
