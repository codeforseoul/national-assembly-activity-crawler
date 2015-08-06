# -*- coding: utf-8 -*-
import json
import re

district_data = json.load(open('election-data.json', 'r', encoding='utf-8'))
assembly_data = json.load(open('assembly.json', 'r', encoding='utf-8'))
p_find_idx = re.compile(r'dept_cd=(\d+)')

def find_cities():
  return list(x.get('name') for x in district_data)

def find_locals(city_name):
  city_info = list(filter(lambda x: x['name'] == city_name, district_data))[0]
  return city_info["district_info"]

def find_towns(city_name, local_name):
  city_info = list(filter(lambda x: x['name'] == city_name, district_data))[0]
  district_info = list(filter(lambda x: x['local'] in local_name, city_info["district_info"]))
  towns = list()
  for district in district_info:
    towns = towns + district['associated_towns']
  return towns


def find_district_name(city_name, local_name, town_name):
  city_info = list(filter(lambda x: x['name'] in city_name, district_data))[0]
  district_info = city_info['district_info']
  district_candidates = list(filter(lambda x: x['local'] == local_name, district_info))
  district_name = list()
  for district_info in district_candidates:
    print(district_info['associated_towns'])
    if town_name in district_info['associated_towns']:
      district_name = district_info['name']
  return district_name


def find_member_idx_with_district(city_name, district_name):
  gen_district = city_name[0:2] + ' ' + district_name
  selected_member = list(filter(lambda x: x['district'] == gen_district, assembly_data))[0]
  return int(p_find_idx.search(selected_member['url']).group(1))


def find_member_idx(city_name, local_name, town_name):
  return find_member_idx_with_district(city_name, find_district_name(city_name, local_name, town_name))


if __name__ == '__main__':
    member_name = find_member_idx('울산광역시', '울주군', '청량면')
    print(member_name)
