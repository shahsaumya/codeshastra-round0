
import http.client, urllib.request, urllib.parse, urllib.error, base64, requests, json

subscription_key = '5979034bfb134316b72d9625b0c320c5'


uri_base = 'https://westcentralus.api.cognitive.microsoft.com'


headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': subscription_key,
}


def detect():
  
    params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
    }

    body1 = {'url': 'https://vignette.wikia.nocookie.net/harrypotter/images/c/c1/Harry%2Bpotter-Harry_Potter_HP4_01.jpg'}
    body2 = {'url': 'https://images.pottermore.com/bxd3o8b291gf/3SQ3X2km8wkQIsQWa02yOY/25f258f21bdbe5f552a4419bb775f4f0/HarryPotter_WB_F4_HarryPotterMidshot_Promo_080615_Port.jpg'}

    try:
    
        response1 = requests.request('POST', uri_base + '/face/v1.0/detect', json=body1, data=None, headers=headers, params=params)
        response2 = requests.request('POST', uri_base + '/face/v1.0/detect', json=body2, data=None, headers=headers, params=params)

        #print ('Response:')
        parsed1 = json.loads(response1.text)
        parsed2 = json.loads(response2.text)
        faceId1=parsed1[0]['faceId']
        faceId2=parsed2[0]['faceId']
        verify(faceId1,faceId2)
        #print (json.dumps(parsed, sort_keys=True, indent=2))

    except Exception as e:
        print('Error:')
        print(e)


def verify(faceId1,faceId2):
    params = urllib.parse.urlencode({
    })

    body = { 
        "faceId1": faceId1,
        "faceId2": faceId2,
    }

    try:
    
        response = requests.request('POST', uri_base + '/face/v1.0/verify', json=body, data=None, headers=headers, params=params)
        print ('Response:')
        parsed = json.loads(response.text)
        print(parsed)
        print (json.dumps(parsed, sort_keys=True, indent=2))
    except Exception as e:
        print('Error:')
        print(e)




