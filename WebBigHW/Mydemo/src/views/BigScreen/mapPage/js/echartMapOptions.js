import echarts from 'echarts'
import $ from 'jquery'
import china from './china.js'
import { cityNameData, provinceNameChineseToEng, cityNameChineseToEng } from './geoNameDictionary.js'
import { Loading } from 'element-ui'
import { watch } from 'vue'

var geoCoordMap = {
  'ZheLang': [115.5989, 22.7107],
  'DongShan': [117.4776, 23.8108],
  'XiaMen': [118.0928, 24.5405],
  'BeiShuang': [120.2901, 26.7214],
  'NanJi': [121.0921, 27.5037],
  'DaChen': [121.8941, 28.4545],
  'ZhenHai': [121.6963, 30.0266],
  'ShengShan': [122.7840, 30.7941],
  'LvSi': [121.5974, 32.0596],
  'LianYunGang': [119.3733, 34.8133],
  'XiaoMaiDao': [120.3840, 35.9597],
  'ZhiFuDao': [121.3728, 37.5963],
  'LaoHuTan': [121.6804, 38.8906],
  'XiaoChangShan': [122.6802, 39.1807]

}

var convertData = function(data, provinceEngName, cityNameEng) {
  var res = []
  for (var i = 0; i < data.length; i++) {
    if (provinceEngName) {
      const ret = cityIsInclude(provinceEngName, data[i].name, cityNameEng)
      if (ret) {
        var geoCoord = geoCoordMap[data[i].name]
        if (geoCoord) {
          res.push({
            name: data[i].name,
            value: geoCoord.concat(data[i].value)
          })
        }
      }
    } else {
      const geoCoord = geoCoordMap[data[i].name]
      if (geoCoord) {
        res.push({
          name: data[i].name,
          value: geoCoord.concat(data[i].value)
        })
      }
    }
  }
  return res
}

const cityIsInclude = function(provinceEngName, cityName, cityNameEng) {
  const cities = cityNameData[`cityName_${provinceEngName}`]
  for (const city in cities) {
    if ((!cityNameEng && city.indexOf(cityName) !== -1) || (cityNameEng && city.indexOf(cityName) !== -1 && cities[city] === cityNameEng)) {
      return true
    }
  }
  return false
}

// 这里设置数据中心的数据
const data = [
  { name: 'ZheLang', value: 1 },
  { name: 'DongShan', value: 2 },
  { name: 'XiaMen', value: 3 },
  { name: 'BeiShuang', value: 4 },
  { name: 'NanJi', value: 5 },
  { name: 'DaChen', value: 6 },
  { name: 'ZhenHai', value: 7 },
  { name: 'ShengShan', value: 8 },
  { name: 'LvSi', value: 9 },
  { name: 'LianYunGang', value: 10 },
  { name: 'XiaoMaiDao', value: 11 },
  { name: 'ZhiFuDao', value: 12 },
  { name: 'LaoHuTan', value: 13 },
  { name: 'XiaoChangShan', value: 14 }
]

function MapDrillDown(echartDom, obj) {
  this.chartDom = echarts.init(echartDom)
  this.optionMap = null
  // tag: 0全国 1省 2市
  this.tag = 0
  this.timer = null
  this.provinceOrCityName = ''
  this.lastProvinceOrCityName = ''
  this.loadingObj = obj.$message
  this.$emit = obj.$emit
  this.obj = obj
}

MapDrillDown.prototype = {
  // 设置区域颜色
  setRegions: function(regionsJson) {
    var colors = ['#083967', '#13548d', '#1c74b2']
    var colorsLen = colors.length
    var features = regionsJson.features
    var echatsRegions = []
    // var echatsRegions=[{
    //     name: '南海诸岛',
    //     value: 0,
    //     itemStyle: {
    //         normal: {
    //             opacity: 0,
    //             label: {
    //                 show: false
    //             }
    //         }
    //     }
    // }];

    for (var i = 0, len = features.length; i < len; i++) {
      var regionsItem = {
        name: features[i].properties.name,
        itemStyle: {
          normal: {
            areaColor: colors[Math.floor(Math.random() * colorsLen)]
          }
        }
      }
      echatsRegions.push(regionsItem)
    }
    return echatsRegions
  },
  setMap: function() {
    this.optionMap = {
      tooltip: {
        trigger: 'item',
        // triggerOn:'click', // 鼠标点击时触发
        enterable: true, // 鼠标是否能进入提示框内
        formatter: function(params) {
          var content = ''
          if (params.value !== undefined) {
            content = `<p style='text-align: center;min-width: 100px;'><span class='dpb' style='padding: 5px 8px;font-family: 微软雅黑;font-size: 18px;color: #ffffff;'>${params.name} ${params.value}</span><br></p>`
          }
          return content
        }
      },
      geo: {
        map: 'china',
        label: {
          normal: {
            show: true,
            color: '#639bc3'
          }
        },
        itemStyle: {
          normal: {
            areaColor: '#083967',
            borderColor: '#48c7ff',
            borderWidth: 2
          },
          emphasis: {
            areaColor: '#48c7ff' // 高亮效果
          }
        },
        layoutCenter: ['50%', '50%'],
        layoutSize: '90%'
      },
      series: [
        {
          name: '',
          type: 'scatter',
          coordinateSystem: 'geo',
          opacity: 1,
          data: convertData(data),
          // data: [],
          symbolSize: 7, // 散点图的大小
          label: {
            normal: {
              show: false
            }
          },
          itemStyle: {
            normal: {
              color: '#00d0e4',
              borderColor: '#fff',
              borderWidth: 2
            },
            emphasis: {
              borderColor: '#fff',
              borderWidth: 2
            }
          }
        }
      ]
    }
    // 图表自适应
    window.addEventListener('resize', function() {
      this.chartDom.resize()
    }.bind(this))

    this.optionMap.geo.regions = this.setRegions(china) // 设置区域颜色
    this.chartDom.setOption(this.optionMap)
  },
  setClick: function() {
    const that = this
    // 点击事件
    that.chartDom.on('click', function(params) { // 点击事件
      clearTimeout(that.timer)
      that.timer = setTimeout(function() {
        if (params.componentType === 'geo') { // 点击地图区域
          that.reFreshMap(params.name)
        }
      }, 300)
    })
    // 双击事件
    that.chartDom.on('dblclick', function(params) {
      clearTimeout(that.timer)
      that.tag = 0
      const senddata = {
        'name': 'china',
        'tag': 0
      }
      that.obj.$emit('changeLayer', senddata)
      that.optionMap.series[0].data = convertData(data)
      that.optionMap.geo.map = 'china'
      that.chartDom.setOption(that.optionMap)
    })
  },
  reFreshMap: function(paramsName) {
    const that = this
    // 使用elment-ui的loading组件
    Loading.service({
      lock: true,
      text: '加载中...',
      spinner: 'el-icon-loading',
      background: 'rgba(0, 0, 0, 0.7)'
    })
    if (that.tag === 0) {
      this.provinceOrCityName = paramsName
      const provinceEngName = provinceNameChineseToEng(this.provinceOrCityName)
      console.log(provinceEngName)
      $.get('https://orangleli.github.io/imagesResources/echartMapResources/geoProvince/' + provinceEngName + '.json', function(mapJson) {
        that.tag++
        const senddata = {
          'name': that.provinceOrCityName,
          'tag': that.tag
        }
        that.obj.$emit('changeLayer', senddata)
        Loading.service().close()
        that.optionMap.series[0].data = convertData(data, provinceEngName)
        that.optionMap.geo.map = provinceEngName
        echarts.registerMap(provinceEngName, mapJson)
        that.chartDom.setOption(that.optionMap)
      })
      this.lastProvinceOrCityName = this.provinceOrCityName
    } else if (that.tag === 1) {
      if (this.lastProvinceOrCityName.includes('直辖市') > 0 || this.lastProvinceOrCityName.includes('台湾省') > 0) {
        this.provinceOrCityName = paramsName
        var provinceEngName = provinceNameChineseToEng(this.lastProvinceOrCityName)
        const cityNameEng = cityNameChineseToEng(that.provinceOrCityName, provinceEngName)
        that.tag++
        const senddata = {
          'name': that.provinceOrCityName,
          'tag': that.tag
        }
        // 等待1.5s
        setTimeout(function() {
          Loading.service().close()
          that.obj.$emit('changeLayer', senddata)
        }, 2000)
        return
      }
      this.provinceOrCityName = paramsName
      var provinceEngName = provinceNameChineseToEng(this.lastProvinceOrCityName)
      const cityNameEng = cityNameChineseToEng(that.provinceOrCityName, provinceEngName)
      $.get('https://orangleli.github.io/imagesResources/echartMapResources/city/' + provinceEngName + '/' + cityNameEng + '.json', function(mapJson) {
        that.tag++
        const senddata = {
          'name': that.provinceOrCityName,
          'tag': that.tag
        }
        that.obj.$emit('changeLayer', senddata)
        Loading.service().close()
        that.optionMap.series[0].data = convertData(data, provinceEngName, cityNameEng)
        that.optionMap.geo.map = provinceEngName
        echarts.registerMap(provinceEngName, mapJson)
        that.chartDom.setOption(that.optionMap)
      })
    } else {
      Loading.service().close()
    }
  },
  init() {
    this.setMap()
    this.setClick()
  }
}
export {
  MapDrillDown
}
