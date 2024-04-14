import request from '@/utils/request'

export function getBigScreenDownScrollData() {
  return request({
    url: '/bigscreen/downscroll',
    method: 'get'
  })
}
