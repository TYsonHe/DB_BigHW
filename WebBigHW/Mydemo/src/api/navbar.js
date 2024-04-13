import request from '@/utils/request'

export function getUserRole() {
  return request({
    url: '/navbar/user/role',
    method: 'get'
  })
}
