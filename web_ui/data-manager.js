// 데이터 관리 및 실시간 업데이트 클래스
class DataManager {
  constructor() {
    this.sensorData = {};
    this.updateCallbacks = [];
    this.refreshInterval = null;
    this.isRunning = false;
    this.config = API_CONFIG || {};
  }

  // 센서 데이터 업데이트 콜백 등록
  onUpdate(callback) {
    if (typeof callback === 'function') {
      this.updateCallbacks.push(callback);
    }
  }

  // 업데이트 콜백 해제
  offUpdate(callback) {
    this.updateCallbacks = this.updateCallbacks.filter(cb => cb !== callback);
  }

  // 모든 콜백에게 데이터 전파
  _notifyUpdate(data) {
    this.updateCallbacks.forEach(callback => {
      try {
        callback(data);
      } catch (error) {
        console.error('Callback error:', error);
      }
    });
  }

  // 센서 데이터 새로고침
  async refresh() {
    try {
      const data = await apiClient.getAllSensors();
      if (data) {
        this.sensorData = data;
        this._notifyUpdate(data);
        return data;
      }
    } catch (error) {
      console.error('Sensor data refresh failed:', error);
      return null;
    }
  }

  // 자동 새로고침 시작
  start() {
    if (this.isRunning) {
      console.warn('DataManager is already running');
      return;
    }

    this.isRunning = true;
    
    // 즉시 한 번 실행
    this.refresh();
    
    // 주기적으로 실행
    const interval = this.config.REFRESH_INTERVAL || 10000;
    this.refreshInterval = setInterval(() => {
      this.refresh();
    }, interval);
    
    console.log(`DataManager started with ${interval}ms interval`);
  }

  // 자동 새로고침 중지
  stop() {
    if (!this.isRunning) return;
    
    this.isRunning = false;
    
    if (this.refreshInterval) {
      clearInterval(this.refreshInterval);
      this.refreshInterval = null;
    }
    
    console.log('DataManager stopped');
  }

  // 현재 센서 데이터 가져오기
  getSensorData() {
    return { ...this.sensorData };
  }

  // 특정 센서 데이터 가져오기
  getSensor(key) {
    return this.sensorData[key] || null;
  }

  // UI 업데이트 유틸리티 함수
  updateSensorCard(cardId, value, unit = '') {
    const card = document.querySelector(`[data-sensor="${cardId}"]`);
    if (!card) return;

    const valueEl = card.querySelector('.value');
    if (valueEl) {
      // 값이 유효하지 않으면 현재 값을 유지
      if (value === null || value === undefined || isNaN(value)) {
        return;
      }
      valueEl.textContent = `${value}${unit}`;
    }
  }

  // 내부 센서 카드들 업데이트
  updateInternalSensors(data) {
    // 내부 온도 (indoor_current_temperature → indoor_temp 매핑)
    this.updateSensorCard('indoor_temp', data.indoor_temp, '℃');
    
    // 내부 습도
    this.updateSensorCard('indoor_humidity', data.indoor_humidity, '%');
    
    // 내부 일사량
    this.updateSensorCard('indoor_solar', data.indoor_solar, ' W/㎡');
    
    // 토양 수분 함수율
    this.updateSensorCard('indoor_moisture', data.indoor_moisture, '%');
    
    // 토양 수분 장력
    this.updateSensorCard('indoor_soil_tension', data.indoor_soil_tension, ' kPa');
  }

  // 외부 센서 데이터 업데이트
  updateExternalSensors(data) {
    // 외부 온도
    this.updateSensorCard('outdoor_temp', data.outdoor_temp, '℃');
    
    // 외부 습도
    this.updateSensorCard('outdoor_humidity', data.outdoor_humidity, '%');
    
    // 외부 일사량
    this.updateSensorCard('outdoor_solar', data.outdoor_solar, ' W/㎡');
    
    // 풍향
    const outdoorWindDirEl = document.querySelector('[data-sensor="outdoor_wind_dir"]');
    if (outdoorWindDirEl && data.outdoor_wind_dir !== null && data.outdoor_wind_dir !== undefined) {
      outdoorWindDirEl.textContent = data.outdoor_wind_dir;
    }
    
    // 풍속
    const outdoorWindSpeedEl = document.querySelector('[data-sensor="outdoor_wind_speed"]');
    if (outdoorWindSpeedEl && data.outdoor_wind_speed !== null && data.outdoor_wind_speed !== undefined && !isNaN(data.outdoor_wind_speed)) {
      outdoorWindSpeedEl.textContent = `${data.outdoor_wind_speed} m/s`;
    }
  }

  // 전체 센서 데이터 업데이트
  updateAllSensors(data) {
    this.updateInternalSensors(data);
    this.updateExternalSensors(data);
    
    // 마지막 업데이트 시간 갱신
    this.updateLastRefreshTime();
  }

  // 마지막 새로고침 시간 업데이트
  updateLastRefreshTime() {
    const now = new Date();
    const hours = now.getHours();
    const minutes = now.getMinutes();
    const period = hours >= 12 ? '오후' : '오전';
    const displayHours = hours > 12 ? hours - 12 : hours;
    
    const sidebarFooter = document.querySelector('.sidebar-footer');
    if (sidebarFooter) {
      sidebarFooter.innerHTML = `
        실시간 데이터 수집 <strong>ON</strong><br />
        최근 업데이트: 오늘 ${period} ${displayHours}:${minutes.toString().padStart(2, '0')}
      `;
    }
  }
}

// 전역 인스턴스 생성
const dataManager = new DataManager();

// 전역에서 사용 가능하도록 내보내기
if (typeof window !== 'undefined') {
  window.DataManager = DataManager;
  window.dataManager = dataManager;
}

