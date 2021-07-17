from lxml import html
import requests
import csv

page = requests.get('https://screensiz.es/')
tree = html.fromstring(page.content)

dlist = tree.xpath('//*[@id="device_info"]/tbody/tr')

device_dict = []
print(tree.xpath(f'//*[@id="device_info"]/tbody/tr[1]/td[1]/text()')[1])

for i in range(len(dlist)-1):
    ratio = "1:1.41"
    if len(tree.xpath(f'//*[@id="device_info"]/tbody/tr[{i+1}]/td[10]/text()')) != 0:
        ratio = tree.xpath(f'//*[@id="device_info"]/tbody/tr[{i+1}]/td[10]/text()')[0].strip()


    dict = {
        'name' : tree.xpath(f'//*[@id="device_info"]/tbody/tr[{i+1}]/td[1]/text()')[1].strip().replace("\n", " "),
        'width' : int(tree.xpath(f'//*[@id="device_info"]/tbody/tr[{i+1}]/td[5]/text()')[0].strip()),
        'height' : int(tree.xpath(f'//*[@id="device_info"]/tbody/tr[{i+1}]/td[6]/text()')[0].strip()),
        'aspect_ratio' : ratio,
        'type' : tree.xpath(f'//*[@id="device_info"]/tbody/tr[{i+1}]/td[14]/text()')[0].strip(),
    }
    print(i,dict)
    device_dict.append(dict)

headers = ['name', 'width', 'height', 'aspect_ratio', 'type']
filename = 'devicelist.csv'

try:
    with open(filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        for data in device_dict:
            writer.writerow(data)
except IOError:
    print("I/O error")

for device in device_dict:
    print(device)
