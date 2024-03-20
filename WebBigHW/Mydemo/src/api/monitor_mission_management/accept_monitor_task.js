import request from '@/utils/request'

export function getMonitorTaskListByRole(data) {
  return request({
    url: '/monitor_task/getMonitorTaskListByRole',
    method: 'post',
    data
  })
}

export function acceptMonitorTask(data) {
  return request({
    url: '/monitor_task/acceptMonitorTask',
    method: 'post',
    data
  })
}
