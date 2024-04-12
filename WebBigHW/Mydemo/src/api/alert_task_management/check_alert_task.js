import request from '@/utils/request'

export function getAlertTaskListByRole(params) {
  return request({
    url: '/alert_task/getAlertTaskListByRole',
    method: 'get',
    params
  })
}

export function getAllAlertTaskCount(params) {
  return request({
    url: '/alert_task/getAllAlertTaskCount',
    method: 'get',
    params
  })
}

export function acceptAlertTask(data) {
  return request({
    url: '/alert_task/acceptAlertTask',
    method: 'post',
    data
  })
}

export function generateAlertTask(params) {
  return request({
    url: '/alert_task/generateAlertTask',
    method: 'get',
    params
  })
}

export function getMiddleChartData(data) {
  return request({
    url: '/alert_task/getMiddleChartData',
    method: 'post',
    data
  })
}

export function getRightChartData(data) {
  return request({
    url: '/alert_task/getRightChartData',
    method: 'post',
    data
  })
}
