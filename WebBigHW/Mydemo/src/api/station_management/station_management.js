import request from '@/utils/request'

export function getAllStations() {
  return request({
    url: '/station/all',
    method: 'get'
  })
}

export function addStation(data) {
  return request({
    url: '/station/add',
    method: 'post',
    data
  })
}

export function updateStation(data) {
  return request({
    url: '/station/update',
    method: 'post',
    data
  })
}

export function deleteStation(data) {
  return request({
    url: '/station/delete',
    method: 'post',
    data
  })
}
