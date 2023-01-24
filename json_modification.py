import json
import codecs
import os
import ast

# assign directory
info_to_write =''
file_to_write =''
data=''
directory = 'c:/Users/apetrov/Desktop/Changes/FOR_TCRM-15689/'
# iterate over files in
# that directory

with open('c:\Mapping\Views.txt','r',encoding="utf8") as input_view_file:
    input_json = input_view_file.read()
views_json=json.loads(input_json)

with open('c:\Mapping\Hierarchy.txt','r',encoding="utf8") as input_hierarchy_file:
    input_json = input_hierarchy_file.read()
hierarchy_json=json.loads(input_json)    

def get_hierarchical_data(index_name):
        # "_meta": {
        # "name": "opportunities",
        # "label": "Сделки",
        # "order": "1",
        # "main_link":"/deals/$id$"
        # }
    _meta=''
    _meta_name=''
    _meta_order=''
    _meta_label=''
    _meta_l1_order=''
    _meta_l2_order=''
    _meta_main_link=''
    for i in hierarchy_json["payload"]["entities"]:
                if i["name"]==index_name:
                    _meta_name=i["name"]
                    _meta_order=f'"{i["order"]}"'
                    _meta_label=f'"{i["label"]}"'
                    # print (_meta_name, _meta_order)
                if _meta_name=='':
                    _meta_l1_order=f'{i["order"]}'
                    for nested_l1 in i['nestedEntities']:
                        if nested_l1["name"]==index_name:
                            _meta_name=nested_l1["name"]
                            _meta_order=f'"{_meta_l1_order}.{nested_l1["order"]}"'
                            _meta_label=f'"{nested_l1["label"]}"'
                            # print (_meta_name, _meta_order)
                        if _meta_name=='':
                            _meta_l2_order=nested_l1["order"]
                            for nested_l2 in nested_l1['nestedEntities']:
                                if nested_l2["name"]==index_name:
                                    _meta_name=nested_l2["name"]
                                    _meta_order=f'"{_meta_l1_order}.{_meta_l2_order}.{nested_l2["order"]}"'
                                    _meta_label=f'"{nested_l2["label"]}"'
                                    # print (_meta_name, _meta_order,_meta_label)
    #Opportunities
    if index_name in ('opportunities'):
        _meta_main_link='"deals/$id$"'
    elif index_name in ('opportunities_positions','opportunities_payments_sub','opportunities_payments',
    'opportunities_other_costs','opportunities_contact_persons','opportunities_acts_sub','opportunities_acts',
    'opportunity_notes'):
        _meta_main_link='"deals/$opportunity_id$"'
    elif index_name in ('opportunities_products'):
        _meta_main_link='"deals/$opportunity_id$/product/$id$"'
    #Contracts
    elif index_name in ('contracts'):
        _meta_main_link='"contracts/$id$"'
    elif index_name in ('contracts_positions','contracts_payments_sub','contracts_payments',
    'contracts_other_costs','contracts_contact_persons','contracts_acts_sub','contracts_acts','contract_notes'):
        _meta_main_link='"contracts/$contract_id$"'
    elif index_name in ('contracts_products'):
        _meta_main_link='"contracts/$contract_id$/product/$id$"'
    ##Company ID
    elif index_name in ('addresses','company_notes','company_positions'):
        _meta_main_link='"organizations/$company_id$"'
    elif index_name in ('companies'):
        _meta_main_link='"organizations/$id$"'
    #Marketing Event
    elif index_name in ('marketing_events'):
        _meta_main_link='"marketing-events/$id$"'
    elif index_name in ('marketing_events_budget','marketing_events_positions','marketing_events_program_items'):
        _meta_main_link='"marketing-events/$marketing_event_id$"'
    #Person
    elif index_name in ('persons_addresses','persons_contact_informations','persons_employment_informations','persons_positions'):
        _meta_main_link='"physical-person/$contact_person_id$"'
    ##Tasks
    elif index_name in ('tasks'):
        _meta_main_link='"tasks/$id$"'
    elif index_name in ('task_notes','persons_contact_informations','persons_employment_informations','persons_positions'):
        _meta_main_link='"tasks/$task_id$"'
    #Leads

    _meta=f'"_meta":{{"name":"{_meta_name}","label":{_meta_label},"order":{_meta_order},"main_link":{_meta_main_link} }}'      
    return _meta

# print(get_hierarchical_data('opportunities'))

def get_view_data(index_name,key_name):
        # "meta": {
        #   "label": "Краткое наименование",
        #   "base_params": """{"order":1,"visible":1}""",
        #   "filter_type_code": "listFilters",
        #   "sort_params": """{"sortable":1,"type":"none","order":0}"""
        # }
    meta=''
    meta_label=''
    meta_base_params=''
    meta_filter_type_code=''
    meta_sort_params=''
    meta_link=''
    for index in views_json['payload']['tables']:
        if index["name"]==index_name:
           for attribute in index['attributes']:
                if attribute["name"]==key_name:
                    meta_label=f'"label":"{attribute["label"]}"'
                    meta_base_params=f'"base_params":"{{\\"order\\":{attribute["order"]},\\"visible\\":{attribute["visible"]}}}"'
                    ##Странное поведение, наоборот пропускает null
                    if '/' in str({attribute["link"]}):
                        meta_link=f',"link":"{attribute["link"]}"'
                    meta_filter_type_code=f'"filter_type_code":"{attribute["filterType"]}"'
                    meta_sort_params=f'"sort_params":"{{\\"sortable\\":{attribute["sortable"]},\\"type\\":\\"{attribute["sortType"]}\\",\\"order\\":{attribute["sortOrder"]}}}"'
                    meta=f'"meta":{{ {meta_label} {meta_link}, {meta_base_params}, {meta_filter_type_code}, {meta_sort_params} }}'
    return meta

# print(get_hierarchical_data('persons_positions', 'main'))

for filename in os.listdir(directory):
    full_path = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(full_path):
        # print(file_to_write) 
        #Read json from mapping file
        with open(full_path,'r',encoding="utf8") as mapping_file:
            info_to_write=''
            file_to_write ='ru_'+filename
            m_f = mapping_file.read()
            mapping_json=json.loads(m_f.lstrip('\ufeff'))
            info_to_write=info_to_write +' {"settings": '
            info_to_write=info_to_write + ' ' + str(mapping_json['settings']).replace("'", '"')
            info_to_write=info_to_write + ' ' + ', "mappings":{ '
            info_to_write=info_to_write  + get_hierarchical_data(filename.replace('.txt',''))
            info_to_write=info_to_write + ', "properties":{ '
            counter = 0
            for key in mapping_json['mappings']['properties']:
                key_data=''
                data =''
                key_data=json.dumps(mapping_json['mappings']['properties'][key])
                data=f'"{key}":{key_data}'
                if counter == 0:
                    info_to_write = info_to_write + ' ' + data
                else:
                    info_to_write = info_to_write + ' ,' + data
                counter += 1
                view_data = get_view_data(filename.replace('.txt',''),key)
                if view_data !='':
                    info_to_write=info_to_write[:-1] + ', ' + get_view_data(filename.replace('.txt',''),key) + '}'
    if filename.replace('.txt','') !='marketing_events':
        info_to_write=info_to_write+'}'*3        
    completeName = os.path.join('c:/Users/apetrov/Desktop/Changes/FOR_TCRM-15689/New', file_to_write)
    print(filename)
    # print (info_to_write)
    # ast.literal_eval(info_to_write)
    out_file = codecs.open(completeName, "w", encoding='utf-8')
    out_file.write(info_to_write)
    out_file.close()


### order
### прописать link
