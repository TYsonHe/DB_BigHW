import request from '@/utils/request'

export function getAllLogs() {
  return request({
    url: '/logs/all',
    method: 'get'
  })
}
