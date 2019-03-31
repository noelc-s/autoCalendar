from html.parser import HTMLParser
import urllib.request
from GoogleCalendarAddEvent import addEvent
from datetime import datetime, timedelta

class LinksParser(HTMLParser):
  def __init__(self,tag,goal_name,goal_val):
    HTMLParser.__init__(self)
    self.recording = 0
    self.data = []
    self.tag = tag
    self.name=goal_name
    self.val=goal_val

  def handle_starttag(self, tag, attributes):
    if tag != self.tag:
      return
    if self.recording:
      self.recording += 1
      return
    for name, value in attributes:
        #print(name,'_',value,"\\'event_location\\'")
        if name == self.name and value == self.val:
            break
    else:
      return
    self.recording = 1
    self.data.append('Date:')

  def handle_endtag(self, tag):
    if tag == self.tag and self.recording:
      self.recording -= 1

  def handle_data(self, data):
    if self.recording:
      if '\\n' != data:
        self.data.append(data)

class event():
    def __init(self):
        self.location = ''
        self.speaker=''
        self.name=''
        self.date=''
    def set_params(self, attributes):
        self.location=location
        self.speaker=speaker
        self.name=name
        self.date=date

with urllib.request.urlopen('http://www.cms.caltech.edu/seminars') as response:
    page = response.read()

parser = LinksParser('div','class',"\\'post\\'")
parser.feed(str(page))
#print(parser.data)

combined_data = ['ya','try']
all_data = []
for i in range(len(parser.data)):
    if 'Date' in parser.data[i]:
        all_data.append(combined_data)
        combined_data=[]
    if ":" == parser.data[i][-1]:
        prev_tag = parser.data[i]
    else:
        combined_data.append(parser.data[i])
#print ('--')
all_data = all_data[1:]
print('Adding the following events:')
for x in all_data:
    print(x)
    date = datetime.strptime(x[1], '%B %d, %Y')
    start_time = datetime.strptime(x[2].strip(), "%I:%M %p")
    end_time = datetime.strptime(x[2].strip(), "%I:%M %p")+ timedelta(hours=1)
    start = date.strftime('%Y-%m-%d')+'T'+start_time.strftime('%H:%M:%S')+'-04:00'
    end = date.strftime('%Y-%m-%d')+'T'+end_time.strftime('%H:%M:%S')+'-04:00'
    event = {}
    event['start'] = {}
    event['start']['dateTime']=start
    event['start']['timeZone']='America/Los_Angeles'
    event['end'] = {}
    event['end']['dateTime']=end
    event['end']['timeZone']='America/Los_Angeles'
    event['summary'] = x[3]
    event['description']="".join(x[4:-1])
    event['location']=x[-1].replace('\\n','')
    addEvent(event)


