import request from '@/utils/request'

export function getAllSpecies() {
  return request({
    url: '/species/all',
    method: 'get'
  })
}

export function addSpecies(data) {
  return request({
    url: '/species/add',
    method: 'post',
    data
  })
}

export function updateSpecies(data) {
  return request({
    url: '/species/update',
    method: 'post',
    data
  })
}

export function deleteSpecies(data) {
  return request({
    url: '/species/delete',
    method: 'post',
    data
  })
}
