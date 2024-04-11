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

export function getAllMonitorTaskCount() {
  return request({
    url: '/monitor_task/getAllMonitorTaskCount',
    method: 'get'
  })
}

export function getMiddleChartData(data) {
  return request({
    url: '/monitor_task/getMiddleChartData',
    method: 'post',
    data
  })
}

export function getRightChartData(data) {
  return request({
    url: '/monitor_task/getRightChartData',
    method: 'post',
    data
  })
}
