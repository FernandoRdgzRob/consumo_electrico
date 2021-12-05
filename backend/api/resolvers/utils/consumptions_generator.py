from datetime import datetime, timedelta
from random import randint

consumptions_dictionary = {
  'Calefactor': [1190.78, 454.9037438, 426.1538286, 8.310189229, 407.161326, 154.9152524, 34.55550816, 1116.943674],
  'Aire': [1530.215, 521.4123497, 434.6590496, 1515.308565],
  'Ventilador': [13.0331682, 41.98858762, 14.17160171, 38.95179302, 41.91133225, 34.58294195, 5.945336012, 44.25926454, 39.68962332, 43.36338792, 29.9912244],
  'Secadora': [125.7751449, 751.137992, 170.0201655, 583.6958211, 105.4323564, 662.4510662, 872.7258136, 86.13733545, 202.1010782, 895.5, 867.5214606],
  'Lavatrastes': [882.098677187157, 934.32597665418, 813.169887794767, 846.560168721789, 1017.23705857013, 1037.57765604263, 1033.21920796759, 950.269810551671, 1009.78654270814, 990.996118114301, 957.425087515416],
  'Estufa': [1425],
  'Microondas': [1087.40923366697, 1179.31509685432, 1207.10893868555, 1124.59784164756, 1232.84300134353, 1225.70383560558, 1145.99143136672, 1096.70109676812, 1178.52875084551, 1130.03763363276],
  'Lavadora': [895.5],
  'Refrigerador': [2861.7],
  'Foco': [10.5]
}

def get_consumption_from_dictionary(device_name):
  if randint(0, 1):
    index = randint(0, len(consumptions_dictionary[device_name]) - 1)
    return consumptions_dictionary[device_name][index]
  else:
    return 0

def generate_consumptions(device_name, days=3):
  maxDatetime = datetime.today().replace(minute=0, second=0, microsecond=0)
  minDatetime = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=days)
  
  consumptions = []
  currentDate = minDatetime
  while currentDate <=  maxDatetime:
    consumptions.append({
      'consumption_datetime': currentDate,
      'consumption_amount': get_consumption_from_dictionary(device_name=device_name)
    })
    currentDate += timedelta(hours=1)
  
  return consumptions