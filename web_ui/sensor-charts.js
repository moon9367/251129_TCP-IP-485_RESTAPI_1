/**
 * 센서 모니터 페이지 차트 관리
 */

const sensorChartsManager = {
  charts: {},
  lastChartData: {},
  
  init: function() {
    // 온도 차트
    this.initChart('chartTemp', ['indoor_temp_1', 'outdoor_temp'], 
                   ['내부 온도', '외부 온도'], 
                   'rgb(75, 192, 192)', 'rgb(255, 99, 132)');
    
    // 습도 차트
    this.initChart('chartHumidity', ['indoor_humidity', 'outdoor_humidity'], 
                   ['내부 습도', '외부 습도'], 
                   'rgb(54, 162, 235)', 'rgb(153, 102, 255)');
    
    // 일사량 차트
    this.initChart('chartSolar', ['indoor_solar', 'outdoor_solar'], 
                   ['내부 일사량', '외부 일사량'], 
                   'rgb(255, 206, 86)', 'rgb(255, 159, 64)');
    
    // 토양 수분 함수율 차트
    this.initChart('chartSoilMoisture', ['indoor_humidity'], 
                   ['토양 수분 함수율'], 
                   'rgb(75, 192, 192)');
    
    // 토양 수분 장력 차트
    this.initChart('chartSoilTension', ['indoor_soil_tension'], 
                   ['토양 수분 장력'], 
                   'rgb(255, 99, 132)');
    
    // 데이터 로드
    this.loadChartData();
    
    console.log('Sensor charts manager initialized');
  },
  
  initChart: function(canvasId, sensorKeys, labels, ...colors) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) {
      console.error(`Chart canvas not found: ${canvasId}`);
      return;
    }
    
    const datasets = sensorKeys.map((key, idx) => ({
      label: labels[idx] || key,
      data: [],
      borderColor: colors[idx] || 'rgb(75, 192, 192)',
      backgroundColor: colors[idx] ? colors[idx].replace('rgb', 'rgba').replace(')', ', 0.2)') : 'rgba(75, 192, 192, 0.2)',
      tension: 0.1
    }));
    
    const chart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: [],
        datasets: datasets
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: true,
            position: 'top'
          }
        },
        scales: {
          x: {
            ticks: {
              maxTicksLimit: 24
            },
            grid: {
              display: false
            }
          },
          y: {
            beginAtZero: false,
            grid: {
              color: 'rgba(255, 255, 255, 0.1)'
            }
          }
        }
      }
    });
    
    this.charts[canvasId] = chart;
  },
  
  loadChartData: async function() {
    try {
      const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.HISTORY}/24h`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const result = await response.json();
      this.processChartData(result.data || []);
      this.updateAllCharts();
      
      console.log('Sensor chart data loaded:', result.count, 'records');
    } catch (error) {
      console.error('Failed to load sensor chart data:', error);
    }
  },
  
  processChartData: function(rawData) {
    if (!rawData || rawData.length === 0) {
      this.lastChartData = {};
      return;
    }
    
    // 1시간 단위로 데이터 집계
    const hourlyData = {};
    const sensorKeys = ['indoor_temp_1', 'indoor_temp_2', 'indoor_humidity', 'indoor_solar', 'indoor_soil_tension',
                       'outdoor_temp', 'outdoor_humidity', 'outdoor_solar', 
                       'outdoor_wind_dir', 'outdoor_wind_speed'];
    
    sensorKeys.forEach(key => {
      hourlyData[key] = [];
    });
    
    // 시간별로 그룹화
    const hourGroups = {};
    rawData.forEach(row => {
      const date = new Date(row.timestamp);
      const hourKey = date.getHours();
      
      if (!hourGroups[hourKey]) {
        hourGroups[hourKey] = { count: 0, sums: {} };
        sensorKeys.forEach(key => {
          hourGroups[hourKey].sums[key] = 0;
        });
      }
      
      hourGroups[hourKey].count++;
      sensorKeys.forEach(key => {
        const val = parseFloat(row[key]);
        if (!isNaN(val)) {
          hourGroups[hourKey].sums[key] += val;
        }
      });
    });
    
    // 시간 순서대로 정렬
    const sortedHours = Object.keys(hourGroups).sort((a, b) => parseInt(a) - parseInt(b));
    
    sortedHours.forEach(hour => {
      const group = hourGroups[hour];
      sensorKeys.forEach(key => {
        const avg = group.count > 0 ? (group.sums[key] / group.count) : null;
        hourlyData[key].push(avg);
      });
    });
    
    this.lastChartData = hourlyData;
  },
  
  updateAllCharts: function() {
    const labels = this.lastChartData.indoor_temp_1 ? 
      Array.from({ length: this.lastChartData.indoor_temp_1.length }, (_, i) => `${i}시`) : [];
    
    // 온도 차트
    if (this.charts.chartTemp) {
      this.charts.chartTemp.data.labels = labels;
      if (this.lastChartData.indoor_temp_1) {
        this.charts.chartTemp.data.datasets[0].data = this.lastChartData.indoor_temp_1;
      }
      if (this.lastChartData.outdoor_temp) {
        this.charts.chartTemp.data.datasets[1].data = this.lastChartData.outdoor_temp;
      }
      this.charts.chartTemp.update('none');
    }
    
    // 습도 차트
    if (this.charts.chartHumidity) {
      this.charts.chartHumidity.data.labels = labels;
      if (this.lastChartData.indoor_humidity) {
        this.charts.chartHumidity.data.datasets[0].data = this.lastChartData.indoor_humidity;
      }
      if (this.lastChartData.outdoor_humidity) {
        this.charts.chartHumidity.data.datasets[1].data = this.lastChartData.outdoor_humidity;
      }
      this.charts.chartHumidity.update('none');
    }
    
    // 일사량 차트
    if (this.charts.chartSolar) {
      this.charts.chartSolar.data.labels = labels;
      if (this.lastChartData.indoor_solar) {
        this.charts.chartSolar.data.datasets[0].data = this.lastChartData.indoor_solar;
      }
      if (this.lastChartData.outdoor_solar) {
        this.charts.chartSolar.data.datasets[1].data = this.lastChartData.outdoor_solar;
      }
      this.charts.chartSolar.update('none');
    }
    
    // 토양 수분 함수율 차트
    if (this.charts.chartSoilMoisture) {
      this.charts.chartSoilMoisture.data.labels = labels;
      if (this.lastChartData.indoor_humidity) {
        this.charts.chartSoilMoisture.data.datasets[0].data = this.lastChartData.indoor_humidity;
      }
      this.charts.chartSoilMoisture.update('none');
    }
    
    // 토양 수분 장력 차트
    if (this.charts.chartSoilTension) {
      this.charts.chartSoilTension.data.labels = labels;
      if (this.lastChartData.indoor_soil_tension) {
        this.charts.chartSoilTension.data.datasets[0].data = this.lastChartData.indoor_soil_tension;
      }
      this.charts.chartSoilTension.update('none');
    }
  }
};

// 페이지 로드 시 초기화
document.addEventListener('DOMContentLoaded', () => {
  if (typeof sensorChartsManager !== 'undefined') {
    sensorChartsManager.init();
  }
});



