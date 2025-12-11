// 🌐 REST API 클라이언트 (영어 전용 API 연동)
class APIClient {
  constructor() {
    this.config = API_CONFIG || {};
    //this.baseURL = this.config.BASE_URL || 'http://192.168.0.14:8000';
    this.baseURL = this.config.BASE_URL || 'https://normally-roman-jaguar-reflects.trycloudflare.com';  // Cloudflare Tunnel (주석처리)
  }

  // 🏥 헬스 체크 (Modbus 연결 상태 확인)
  async checkHealth() {
    try {
      const response = await fetch(`${this.baseURL}${this.config.ENDPOINTS.HEALTH}`, {
        method: 'GET',
        timeout: this.config.TIMEOUT || 5000,
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('✅ Health check:', data);
      return data;
    } catch (error) {
      console.error('❌ Health check failed:', error);
      throw error;
    }
  }
  
  // 📋 전체 제어 항목 목록 가져오기
  async getControlsList(category = null, writableOnly = false) {
    try {
      let url = `${this.baseURL}${this.config.ENDPOINTS.CONTROLS_LIST}`;
      const params = new URLSearchParams();
      
      if (category) params.append('category', category);
      if (writableOnly) params.append('writable_only', 'true');
      
      if (params.toString()) url += `?${params.toString()}`;
      
      const response = await fetch(url, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('❌ Failed to get controls list:', error);
      return null;
    }
  }

  // 🌡️ 모든 센서 데이터 가져오기 (GET /api/sensors/all)
  async getAllSensors() {
    try {
      const response = await fetch(`${this.baseURL}${this.config.ENDPOINTS.SENSORS_ALL}`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      
      if (!data.success) {
        console.warn('⚠️ Sensors data not successful:', data);
        return null;
      }
      
      // 응답 형식: { success: true, count: 10, sensors: { name: {value, unit, ...}, ... } }
      const formatted = this._formatSensorData(data.sensors);
      return formatted;
    } catch (error) {
      console.error('❌ Failed to fetch all sensors:', error);
      return null;
    }
  }

  // 🌡️ 개별 센서 데이터 가져오기 (GET /api/sensors/{name})
  async getSensor(sensorKey) {
    try {
      // UI 키를 API 영어 이름으로 변환
      const apiKey = this.config.SENSOR_KEYS[sensorKey] || sensorKey;
      
      const response = await fetch(`${this.baseURL}${this.config.ENDPOINTS.SENSOR}/${apiKey}`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      
      if (!data.success) {
        console.warn(`⚠️ Sensor ${apiKey} not successful:`, data);
        return null;
      }
      
      return data;
    } catch (error) {
      console.error(`❌ Failed to fetch sensor ${sensorKey}:`, error);
      return null;
    }
  }

  // 🗺️ 센서 데이터 포맷팅 (REST API 응답 → UI 형식)
  _formatSensorData(sensorsObj) {
    const formatted = {};
    
    // 영어 API 이름 → UI 키로 역매핑
    const reverseMap = {};
    for (const [uiKey, apiKey] of Object.entries(this.config.SENSOR_KEYS)) {
      reverseMap[apiKey] = uiKey;
    }
    
    // sensors 객체를 순회하며 포맷팅
    for (const [apiName, sensorData] of Object.entries(sensorsObj)) {
      const uiKey = reverseMap[apiName];
      if (uiKey && sensorData.success !== false) {
        formatted[uiKey] = sensorData.value !== null ? sensorData.value : 0;
      }
    }
    
    return formatted;
  }

  // 🎛️ 설정값 읽기 (GET /api/settings/{name})
  async getSetting(settingKey) {
    try {
      // UI 키를 API 영어 이름으로 변환
      const apiKey = this.config.SETTING_KEYS?.[settingKey] || settingKey;
      
      const response = await fetch(`${this.baseURL}${this.config.ENDPOINTS.SETTINGS}/${apiKey}`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      
      if (!data.success) {
        console.warn(`⚠️ Setting ${apiKey} not successful:`, data);
        return null;
      }
      
      return data;
    } catch (error) {
      console.error(`❌ Failed to get setting ${settingKey}:`, error);
      return null;
    }
  }

  // 🎛️ 설정값 쓰기 (PUT /api/settings/{name})
  async setSetting(settingKey, value) {
    try {
      // UI 키를 API 영어 이름으로 변환
      const apiKey = this.config.SETTING_KEYS?.[settingKey] || settingKey;
      
      const response = await fetch(`${this.baseURL}${this.config.ENDPOINTS.SETTINGS}/${apiKey}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ value: value }),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      
      if (!data.success) {
        console.warn(`⚠️ Setting ${apiKey} write not successful:`, data);
        return data;
      }
      
      console.log(`✅ Setting ${apiKey} = ${value}:`, data);
      return data;
    } catch (error) {
      console.error(`❌ Failed to set ${settingKey}:`, error);
      throw error;
    }
  }

  // 📊 상태값 읽기 (GET /api/status/{name})
  async getStatus(statusKey) {
    try {
      const response = await fetch(`${this.baseURL}${this.config.ENDPOINTS.STATUS}/${statusKey}`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      
      if (!data.success) {
        console.warn(`⚠️ Status ${statusKey} not successful:`, data);
        return null;
      }
      
      return data;
    } catch (error) {
      console.error(`❌ Failed to get status ${statusKey}:`, error);
      return null;
    }
  }

  // 🔧 Raw 레지스터 읽기 (GET /api/raw/read/{address})
  async readRawRegister(address) {
    try {
      const response = await fetch(`${this.baseURL}${this.config.ENDPOINTS.RAW_READ}/${address}`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error(`❌ Failed to read raw register ${address}:`, error);
      throw error;
    }
  }

  // 🔧 Raw 레지스터 쓰기 (POST /api/raw/write/{address})
  async writeRawRegister(address, value) {
    try {
      const response = await fetch(`${this.baseURL}${this.config.ENDPOINTS.RAW_WRITE}/${address}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ value: value }),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error(`❌ Failed to write raw register ${address}:`, error);
      throw error;
    }
  }

  // ⚠️ 레거시 메서드 (하위 호환성)
  // 새 코드에서는 setSetting()을 사용하세요
  async setBit(wordAddr, bitNum, value) {
    console.warn('⚠️ setBit() is deprecated. Use setSetting() instead.');
    return this.writeRawRegister(wordAddr, value);
  }

  async setWord(wordAddr, value) {
    console.warn('⚠️ setWord() is deprecated. Use setSetting() instead.');
    return this.writeRawRegister(wordAddr, value);
  }
}

// 전역 인스턴스 생성
const apiClient = new APIClient();

// 전역에서 사용 가능하도록 내보내기
if (typeof window !== 'undefined') {
  window.APIClient = APIClient;
  window.apiClient = apiClient;
}

