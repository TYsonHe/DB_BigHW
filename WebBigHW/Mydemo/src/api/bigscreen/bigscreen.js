import request from '@/utils/request'

export function getBigScreenDownScrollData() {
  return request({
    url: '/bigscreen/downscroll',
    method: 'get'
  })
}

export function getSpeciesNumber() {
  return request({
    url: '/bigscreen/speciesnumber',
    method: 'get'
  })
}

export function getAllSpeciesCount() {
  return request({
    url: '/bigscreen/allspeciescount',
    method: 'get'
  })
}

export function getAllmonitoringTaskCount() {
  return request({
    url: '/bigscreen/allmonitoringtaskcount',
    method: 'get'
  })
}

export function getAllalertTaskCount() {
  return request({
    url: '/bigscreen/allalerttaskcount',
    method: 'get'
  })
}
