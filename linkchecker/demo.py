# Program to find the URL from an input string 
import re
import urllib.request, urllib.error

def url(str):
   # findall() has been used 
   # with valid conditions for urls in string
   ur = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str)
   return ur
# Driver Code
str ='[  {    "Button": "aorta",    "Topic heading": "Abdominal Aortic Aneurysm Screen",    "Subject": "Screen men age 65-80 with ultrasound once.","General Patient Text": "n/a","Health Provider Text": "[[Weak recommendation by canadian task force; https://canadiantaskforce.ca/guidelines/published-guidelines/abdominal-aortic-aneurysm/]]","Gender": "m","Minimum age": 65,"Maximum age": 80,"": """Button": "aorta", "Topic heading": "Aorta:the bodys main blood vessel","Subject": "Talk to your \nprovider to see \nif you need a test.","General Patient Text": "Your provider may ask for\n an ultrasound of your belly\n to detect a bulge in the main blood vessel \n(the bulge is nicknamed AAA \nfor short or\nabdominal aortic aneurysm)\nIf the bulge grows it can burst and cause death.","Health Provider Text": "n/a","Gender": "m","Minimum age": 65,"Maximum age": 80,"": """Button": "Figure outside body walking","Topic heading": "Be active","Subject": "","General Patient Text": "Physical activity\nprevents heart disease, cancer, depression and [[more; https://www.reframehealthlab.com/23-and-12-hours/]]\n\nThe recommended minimum amount of physical activity\n is 150 minutes a week of moderate intensity exercise. \nDefinition of moderate intensity:\nwhile you are active you have enough breath to say a short sentence but  not enough to sing\n• [[more info for age 18-64; http://www.csep.ca/CMFiles/Guidelines/CSEP_PAGuidelines_adults_en.pdf]]\n• [[ more info for age 65+; http://csepguidelines.ca/wp-content/uploads/2018/03/CSEP_PAGuidelines_older-adults_en.pdf]]","Button": "Bone","Topic heading": "Bone health","Subject": "•Do exercises for healthy bones.\n[[Recommendations; https://osteoporosis.ca/bone-health-osteoporosis/exercises-for-healthy-bones/]]\n•Bone density test:below age 65:only recommended if:","General Patient Text": "you have [[risk factors; https://www.canada.ca/en/public-health/services/chronic-diseases/osteoporosis.html]]","Health Provider Text": "patient has  [[risk factors; http://www.osteoporosis.ca/multimedia/pdf/Quick_Reference_Guide_October_2010.pdf]] or use [[OST; http://www.cfp.ca/content/61/7/612]]","Button": "Bone","Topic heading": "Bone health","Subject": "•Do exercises for healthy bones.\n[[Recommendations; https://osteoporosis.ca/bone-health-osteoporosis/exercises-for-healthy-bones/]]\n•Bone density test:\nRecommended age 65 and over :","General Patient Text": "Your provider will determine when to repeat it\n[[more info; https://choosingwiselycanada.org/bone-density-tests/]]\n[[calculator for 10 year fracture risk; https://www.sheffield.ac.uk/FRAX/tool.jsp?country=19 ]]","Health Provider Text": "•[[osteoporosis.ca; http://www.cmaj.ca/content/cmaj/early/2010/10/12/cmaj.100771.full.pdf]]\n•or use [[OST; http://www.cfp.ca/content/61/7/612]]\n•frequency of retesting [[not more than every 2 years; https://choosingwiselycanada.org/rheumatology/]]\n[[decision aid; https://osteoporosisdecisionaid.mayoclinic.org/]]","Button": "Breast","Topic heading": "Breast Cancer","Subject": "Prevent breast cancer","General Patient Text": "•Limit alcohol (see our substance use info)\n•Dont smoke\n•Control your weight\n•Be physically active (see our physical activity info for this)\n•Breastfeed if you are able\n•Limit time on hormone therapy\n[[more; https://www.mycanceriq.ca/Cancers/Risk]]\n\nMammograms for healthy women below age 50 \nwith no symptoms, no breast problems\n and no additional risks \nis not recommended.\n[[risks; http://www.cancer.ca/en/cancer-information/cancer-type/breast/risks/?region=on]]\n[[harms of mammograms; https://www.youtube.com/watch?v=UZlY6Q4m-MM]]\nDISCUSS WITH YOUR HEALTH CARE PROVIDER.","Button": "Breast","Topic heading": "Breast Cancer","Subject": "Get tested for breast cancer \nat age 50-74","General Patient Text": "Get a mammogram every 2 years:\nYou may need one earlier or more often\n if you have risks or symptoms.\n[[more; http://www.cancer.ca/en/cancer-information/cancer-type/breast/risks/?region=on]]'
url = url(str)
for x in url:
   print(x)
   try:
      conn = urllib.request.urlopen(x)
   except urllib.error.HTTPError as e:
        # Return code error (e.g. 404, 501, ...)
        # ...
      print('HTTPError: {}'.format(e.code))
   except urllib.error.URLError as e:
        # Not an HTTP-specific error (e.g. connection refused)
        # ...
      print('URLError: {}'.format(e.reason))
   else:
        # 200
        # ...
      print('good')

      if __name__ == '__main__':
  app.run(debug = True)