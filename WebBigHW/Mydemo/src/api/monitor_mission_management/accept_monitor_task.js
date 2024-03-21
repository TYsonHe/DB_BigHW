import request from '@/utils/request'

export function getMonitorTaskListByRole(params) {
  return request({
    url: '/monitor_task/getMonitorTaskListByRole',
    method: 'get',
    params
  })
}

export function acceptMonitorTask(data) {
  return request({
    url: '/monitor_task/acceptMonitorTask',
    method: 'post',
    data
  })
}
