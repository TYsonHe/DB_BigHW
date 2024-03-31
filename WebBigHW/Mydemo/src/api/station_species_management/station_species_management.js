import request from '@/utils/request'

export function getStationSpeciesList(params) {
  return request({
    url: '/station_species_management/get_station_species_list',
    method: 'get',
    params
  })
}

export function getStationSpeciesQuantitySeries(data) {
  return request({
    url: '/station_species_management/get_station_species_quantity_series',
    method: 'post',
    data
  })
}

export function getStationSpeciesQuantityRank(data) {
  return request({
    url: '/station_species_management/get_station_species_quantity_rank',
    method: 'post',
    data
  })
}

export function getStationSpeciesQuantityTotal(data) {
  return request({
    url: '/station_species_management/get_station_species_quantity_total',
    method: 'post',
    data
  })
}
