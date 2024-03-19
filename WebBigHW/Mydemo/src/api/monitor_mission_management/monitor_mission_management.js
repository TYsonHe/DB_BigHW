import request from '@/utils/request'

export function getAllMonitoringTasks() {
  return request({
    url: '/monitor_mission_management/getAllMonitoringTasks',
    method: 'get'
  })
}

export function addMonitoringTask(data) {
  return request({
    url: '/monitor_mission_management/addMonitoringTask',
    method: 'post',
    data
  })
}

export function updateMonitoringTask(data) {
  return request({
    url: '/monitor_mission_management/updateMonitoringTask',
    method: 'post',
    data
  })
}

export function deleteMonitoringTask(data) {
  return request({
    url: '/monitor_mission_management/deleteMonitoringTask',
    method: 'post',
    data
  })
}
