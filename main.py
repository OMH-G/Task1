import json, unittest, datetime

with open("./data-1.json","r") as f:
    jsonData1 = json.load(f)
with open("./data-2.json","r") as f:
    jsonData2 = json.load(f)
with open("./data-result.json","r") as f:
    jsonExpectedResult = json.load(f)




def convertFromFormat1 (jsonObject):
    # IMPLEMENT: Conversion From Type 1
    locat=jsonObject['location'].split('/')
    status=jsonObject["operationStatus"]
    temp=jsonObject['temp']
    data=dict()
    data.update({'country':locat[0],'city':locat[1],'area':locat[2],'factory':locat[3],'section':locat[4]})
    jsonObject['location']=data
    del jsonObject['operationStatus']
    del jsonObject['temp']
    data={'status':status,'temperature':temp}
    jsonObject['data']=data
    return jsonObject

def convertFromFormat2 (jsonObject):
    # IMPLEMENT: Conversion From Type 1
    time = jsonObject['timestamp']
    date = datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.%fZ')
    timestamp = str((date - datetime.datetime(1970, 1, 1)).total_seconds()*1000)
    timestamp=int(timestamp[:-2])
    jsonObject.update({'deviceID':jsonObject['device']['id'],'deviceType':jsonObject['device']['type'],'timestamp':timestamp,"location": {
        "country": jsonObject["country"],
        "city": jsonObject["city"],
        "area": jsonObject["area"],
        "factory": jsonObject["factory"],
        "section": jsonObject["section"]
    }, "data": {
        "status": jsonObject['data']['status'],
        "temperature": jsonObject['data']['temperature']
    }})
    for i in ['device','city','area','factory','section','country']:
        del jsonObject[i]
    return jsonObject


def main (jsonObject):

    result = {}

    if (jsonObject.get('device') == None):
        result = convertFromFormat1(jsonObject)
    else:
        result = convertFromFormat2(jsonObject)

    return result


class TestSolution(unittest.TestCase):

    def test_sanity(self):

        result = json.loads(json.dumps(jsonExpectedResult))
        self.assertEqual(
            result,
            jsonExpectedResult
        )

    def test_dataType1(self):

        result = main (jsonData1)
        self.assertEqual(
            result,
            jsonExpectedResult,
            'Converting from Type 1 failed'
        )

    def test_dataType2(self):

        result = main (jsonData2)
        self.assertEqual(
            result,
            jsonExpectedResult,
            'Converting from Type 2 failed'
        )

if __name__ == '__main__':
    unittest.main()
