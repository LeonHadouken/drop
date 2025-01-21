from django.shortcuts import render
import xml.etree.ElementTree as ET

def view_types(request):
    files = {
        'types': 'C:/SteamLibrary/steamapps/common/DayZServer/mpmissions/regular.namalsk/db/types.xml',
        'types_dzn': 'C:/SteamLibrary/steamapps/common/DayZServer/mpmissions/regular.namalsk/db/types_dzn.xml',
    }

    data = {'types': [], 'types_dzn': []}

    if request.method == 'POST':
        for key, file_path in files.items():
            tree = ET.parse(file_path)
            root = tree.getroot()

            for i, type_elem in enumerate(root.findall('type'), start=1):
                type_elem.set('name', request.POST.get(f'{key}_name_{i}', type_elem.get('name')))
                for child in type_elem:
                    if child.tag == 'flags':
                        for flag in ['count_in_map', 'count_in_hoarder', 'count_in_cargo', 'count_in_player', 'crafted', 'deloot']:
                            new_value = '1' if request.POST.get(f'{key}_flags_{flag}_{i}', '0') == '1' else '0'
                            child.set(flag, new_value)
                    elif child.tag == 'attachments':
                        for item_index, item in enumerate(child.findall('item'), start=1):
                            item.set('name', request.POST.get(f'{key}_attachments_item_name_{i}_{item_index}', item.get('name')))
                            item.set('chance', request.POST.get(f'{key}_attachments_item_chance_{i}_{item_index}', item.get('chance')))
                    elif child.text is not None:
                        child.text = request.POST.get(f'{key}_{child.tag}_{i}', child.text)

            tree.write(file_path)

    for key, file_path in files.items():
        tree = ET.parse(file_path)
        root = tree.getroot()
        for type_elem in root.findall('type'):
            attributes = {
                'name': type_elem.get('name'),
                'nominal': type_elem.findtext('nominal', ''),
                'lifetime': type_elem.findtext('lifetime', ''),
                'restock': type_elem.findtext('restock', ''),
                'min': type_elem.findtext('min', ''),
                'quantmin': type_elem.findtext('quantmin', ''),
                'quantmax': type_elem.findtext('quantmax', ''),
                'cost': type_elem.findtext('cost', ''),
                'flags': {
                    'count_in_map': type_elem.find('flags').get('count_in_map', '0'),
                    'count_in_hoarder': type_elem.find('flags').get('count_in_hoarder', '0'),
                    'count_in_cargo': type_elem.find('flags').get('count_in_cargo', '0'),
                    'count_in_player': type_elem.find('flags').get('count_in_player', '0'),
                    'crafted': type_elem.find('flags').get('crafted', '0'),
                    'deloot': type_elem.find('flags').get('deloot', '0'),
                } if type_elem.find('flags') else {},
                'category': type_elem.find('category').get('name', '') if type_elem.find('category') else '',
                'tags': [tag.get('name') for tag in type_elem.findall('tag')],
                'usage': [usage.get('name') for usage in type_elem.findall('usage')],
                'value': [value.get('user') for value in type_elem.findall('value')],
                'attachments': [
                    {
                        'name': item.get('name', ''),
                        'chance': item.get('chance', ''),
                    }
                    for attachment_group in type_elem.findall('attachments')
                    for item in attachment_group.findall('item')
                ],
            }
            data[key].append(attributes)

    return render(request, 'utils/types.html', {'data': data})
