#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from googleads import adwords
import json

PAGE_SIZE = 5

def get_ads_selector(request_type, requested_attribute_types, queries):
    ads_selector = {'ideaType': 'KEYWORD', 'requestType': request_type}
    ads_selector['requestedAttributeTypes'] = requested_attribute_types
    ads_selector['paging'] = {'startIndex': '0', 'numberResults': str(PAGE_SIZE)}
    ads_selector['searchParameters'] = [{
        'xsi_type': 'RelatedToQuerySearchParameter',
        'queries': queries
    }]
    ads_selector['searchParameters'].append({
        'xsi_type': 'LanguageSearchParameter',
        'languages': [{'id': '1005'}]
    })
    ads_selector['searchParameters'].append({
        'xsi_type': 'NetworkSearchParameter',
        'networkSetting': {
            'targetGoogleSearch': True,
            'targetSearchNetwork': False,
            'targetContentNetwork': False,
            'targetPartnerSearchNetwork': False
        }
    })
    return ads_selector

def get_ads_results(ads_selector):
    ads_list = []
    page = {}
    try:
        page = targeting_idea_service.get(ads_selector)
    except Exception as e:
        print(e)

    if 'entries' in page:
        for result in page['entries']:
            attributes = {}
            for attribute in result['data']:
                attributes[attribute['key']] = getattr(attribute['value'], 'value', '0')
            if attributes['SEARCH_VOLUME'] is not None and int(attributes['SEARCH_VOLUME']) > 0:
                record = {
                    'keyword': attributes['KEYWORD_TEXT'],
                    'search_volume': attributes['SEARCH_VOLUME'],
                    'monthly_search_volume': attributes['TARGETED_MONTHLY_SEARCHES']
                }
                ads_list.append(record)
    else:
        print('Adwords API: No related keywords were found.')
    return ads_list

def main(target_keywords):
    ads_selector = get_ads_selector('IDEAS', ['KEYWORD_TEXT', 'SEARCH_VOLUME','TARGETED_MONTHLY_SEARCHES'], target_keywords)
    ads_list = get_ads_results(ads_selector)

    targetidea_list = []
    cnt = 0
    for i in ads_list:
        cnt += 1
        str_search_volume = str(int(i['search_volume']))
        str_monthly_search_volume =str(i['monthly_search_volume'])
        str_monthly_search_volume = str_monthly_search_volume.replace('\n','')
        str_monthly_search_volume = json.dumps(str_monthly_search_volume)
        str_monthly_search_volume = json.loads(str_monthly_search_volume)
        record = {
                'no': cnt,
                'keyword': target_keywords[0],
                'search_volume': str_search_volume,
                'monthly_search_volume': str_monthly_search_volume
        }
        targetidea_list.append(record)
        if cnt == 1:
            break
    cnt = 1
    for row in ads_list:
        cnt += 1
        str_search_volume = str(int(row['search_volume']))
        str_monthly_search_volume = str(row['monthly_search_volume'])
        str_monthly_search_volume = str_monthly_search_volume.replace('\n','')
        str_monthly_search_volume = json.dumps(str_monthly_search_volume)
        str_monthly_search_volume = json.loads(str_monthly_search_volume)
        record = {
            'no': cnt,
            'keyword': row['keyword'],
            'search_volume': str_search_volume,
            'monthly_search_volume': str_monthly_search_volume
        }
        targetidea_list.append(record)

    print(targetidea_list)

if __name__ == '__main__':
    ads_client = adwords.AdWordsClient.LoadFromStorage('~/Desktop/googlegraph/google-ads.yaml')
    targeting_idea_service = ads_client.GetService('TargetingIdeaService', version='v201809')

    target_keywords = ['ダイエット']
    main(target_keywords)
