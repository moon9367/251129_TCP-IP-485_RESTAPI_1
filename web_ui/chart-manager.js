/**
 * 차트 관리자
 * Chart.js를 사용하여 센서 데이터 그래프 표시
 */

const chartManager = {
  chart: null,
  currentTab: '온도',
  
  init: function() {
    // Chart.js 설정
    const ctx = document.getElementById('envChart');
    if (!ctx) {
      console.error('Chart canvas not found');
      return;
    }
    
    const config = {
      type: 'line',
      data: {
        labels: [],
        datasets: [
          {
            label: '내부 온도',
            data: [],
            borderColor: 'rgb(75, 192, 192)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            tension: 0.1,
            yAxisID: 'y'
          },
          {
            label: '외부 온도',
            data: [],
            borderColor: 'rgb(255, 99, 132)',
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            tension: 0.1,
            yAxisID: 'y'
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false  // 범례는 CSS로 별도 표시
          }
        },
        scales: {
          x: {
            ticks: {
              maxTicksLimit: 24  // 24시간 표시
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
    };
    
    this.chart = new Chart(ctx, config);
    
    // 탭 변경 이벤트
    this.initTabs();
    
    // 초기 데이터 로드
    this.loadChartData();
    
    console.log('Chart manager initialized');
  },
  
  initTabs: function() {
    const tabs = document.querySelectorAll('.chart-header .tabs span');
    if (!tabs || tabs.length === 0) {
      console.error('Chart tabs not found');
      return;
    }
    
    tabs.forEach(tab => {
      tab.addEventListener('click', () => {
        // 활성 탭 변경
        tabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        
        // 차트 데이터 변경
        this.currentTab = tab.textContent.trim();
        this.updateChartForTab(this.currentTab);
      });
    });
  },
  
  updateChartForTab: function(tabName) {
    if (!this.chart) return;
    
    const config = this.getChartConfigForTab(tabName);
    
    // 데이터셋 업데이트
    this.chart.data.labels = config.labels;
    this.chart.data.datasets = config.datasets;
    this.chart.options.scales.y = config.scales.y;
    this.chart.update('none');  // 애니메이션 없이 업데이트
  },
  
  getChartConfigForTab: function(tabName) {
    const labels = this.chart.data.labels || [];
    const data = this.lastChartData || {};
    
    switch(tabName) {
      case '온도':
        return {
          labels: labels,
          datasets: [
            {
              label: '내부 온도',
              data: data.indoor_temp_1 || [],
              borderColor: 'rgb(75, 192, 192)',
              backgroundColor: 'rgba(75, 192, 192, 0.2)',
              tension: 0.1
            },
            {
              label: '외부 온도',
              data: data.outdoor_temp || [],
              borderColor: 'rgb(255, 99, 132)',
              backgroundColor: 'rgba(255, 99, 132, 0.2)',
              tension: 0.1
            }
          ],
          scales: {
            y: {
              beginAtZero: false,
              grid: { color: 'rgba(255, 255, 255, 0.1)' }
            }
          }
        };
        
      case '습도':
        return {
          labels: labels,
          datasets: [
            {
              label: '내부 습도',
              data: data.indoor_humidity || [],
              borderColor: 'rgb(54, 162, 235)',
              backgroundColor: 'rgba(54, 162, 235, 0.2)',
              tension: 0.1
            },
            {
              label: '외부 습도',
              data: data.outdoor_humidity || [],
              borderColor: 'rgb(153, 102, 255)',
              backgroundColor: 'rgba(153, 102, 255, 0.2)',
              tension: 0.1
            }
          ],
          scales: {
            y: {
              beginAtZero: true,
              max: 100,
              grid: { color: 'rgba(255, 255, 255, 0.1)' }
            }
          }
        };
        
      case '일사량':
        return {
          labels: labels,
          datasets: [
            {
              label: '내부 일사량',
              data: data.indoor_solar || [],
              borderColor: 'rgb(255, 206, 86)',
              backgroundColor: 'rgba(255, 206, 86, 0.2)',
              tension: 0.1
            },
            {
              label: '외부 일사량',
              data: data.outdoor_solar || [],
              borderColor: 'rgb(255, 159, 64)',
              backgroundColor: 'rgba(255, 159, 64, 0.2)',
              tension: 0.1
            }
          ],
          scales: {
            y: {
              beginAtZero: true,
              grid: { color: 'rgba(255, 255, 255, 0.1)' }
            }
          }
        };
        
      case '토양':
        return {
          labels: labels,
          datasets: [
            {
              label: '토양 함수율',
              data: data.indoor_humidity || [],  // indoor_humidity와 매핑
              borderColor: 'rgb(255, 206, 86)',
              backgroundColor: 'rgba(255, 206, 86, 0.2)',
              tension: 0.1
            },
            {
              label: '토양 수분 장력',
              data: data.indoor_soil_tension || [],
              borderColor: 'rgb(255, 159, 64)',
              backgroundColor: 'rgba(255, 159, 64, 0.2)',
              tension: 0.1
            }
          ],
          scales: {
            y: {
              beginAtZero: true,
              grid: { color: 'rgba(255, 255, 255, 0.1)' }
            }
          }
        };
        
      default:
        return {
          labels: labels,
          datasets: [],
          scales: {
            y: {
              beginAtZero: false,
              grid: { color: 'rgba(255, 255, 255, 0.1)' }
            }
          }
        };
    }
  },
  
  loadChartData: async function() {
    try {
      const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.HISTORY}/24h`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const result = await response.json();
      this.processChartData(result.data || []);
      this.updateChartForTab(this.currentTab);
      
      console.log('Chart data loaded:', result.count, 'records');
    } catch (error) {
      console.error('Failed to load chart data:', error);
      // 에러 시 빈 차트 표시
      if (this.chart) {
        this.chart.data.labels = [];
        this.chart.data.datasets.forEach(dataset => dataset.data = []);
        this.chart.update('none');
      }
    }
  },
  
  processChartData: function(rawData) {
    if (!rawData || rawData.length === 0) {
      this.lastChartData = {};
      this.chart.data.labels = [];
      return;
    }
    
    // 1시간 단위로 데이터 집계 (24시간 = 24개 포인트)
    const hourlyData = {};
    const sensorKeys = ['indoor_temp_1', 'indoor_temp_2', 'indoor_humidity', 'indoor_solar', 'indoor_soil_tension',
                       'outdoor_temp', 'outdoor_humidity', 'outdoor_solar', 
                       'outdoor_wind_dir', 'outdoor_wind_speed'];
    
    // 센서별로 초기화
    sensorKeys.forEach(key => {
      hourlyData[key] = [];
    });
    const labels = [];
    
    // 시간별로 그룹화
    const hourGroups = {};
    rawData.forEach(row => {
      const date = new Date(row.timestamp);
      const hourKey = date.getHours(); // 0-23
      
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
    
    // 시간 순서대로 정렬 (0시~23시)
    const sortedHours = Object.keys(hourGroups).sort((a, b) => parseInt(a) - parseInt(b));
    
    sortedHours.forEach(hour => {
      const group = hourGroups[hour];
      labels.push(`${hour}시`);
      
      sensorKeys.forEach(key => {
        const avg = group.count > 0 ? (group.sums[key] / group.count) : null;
        hourlyData[key].push(avg);
      });
    });
    
    this.chart.data.labels = labels;
    this.lastChartData = hourlyData;
  },
  
  refresh: function() {
    this.loadChartData();
  }
};

