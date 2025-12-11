// API 및 서비스 설정 관리 파일
const API_CONFIG = {
  // ⚙️ REST API 기본 주소 (환경에 따라 변경)
  // 로컬 개발: 'http://localhost:8000'
  // Cloudflare Tunnel: 'https://prefer-nodes-corps-roman.trycloudflare.com'
  // 운영: 'http://실제서버IP:8000' (예: 'http://192.168.1.100:8000')
  //BASE_URL: 'http://192.168.0.14:8000',
  BASE_URL: 'https://normally-roman-jaguar-reflects.trycloudflare.com',  // Cloudflare Tunnel (주석처리)
  
  // 📡 엔드포인트 (영어 전용 REST API)
  ENDPOINTS: {
    // 기본 정보
    ROOT: '/',                          // API 정보
    HEALTH: '/health',                  // 헬스 체크 (Modbus 연결 상태)
    CONTROLS_LIST: '/api/controls/list', // 전체 제어 항목 목록
    
    // 센서 (읽기 전용, 워드주소 70~79)
    SENSORS_ALL: '/api/sensors/all',    // 모든 센서 한 번에
    SENSOR: '/api/sensors',             // /api/sensors/{name}
    
    // 설정값 (읽기/쓰기, 워드주소 0~59)
    SETTINGS: '/api/settings',          // /api/settings/{name}
    
    // 상태값 (읽기 전용, 워드주소 60~69, 80~84)
    STATUS: '/api/status',              // /api/status/{name}
    
    // Raw 레지스터 (고급)
    RAW_READ: '/api/raw/read',          // /api/raw/read/{address}
    RAW_WRITE: '/api/raw/write',        // /api/raw/write/{address}
  },
  
  // 🗺️ 센서 키 매핑 (UI 표시명 → REST API 영어 이름)
  // control_specs.py의 영어 이름과 일치
  SENSOR_KEYS: {
    // 내부 센서 (워드주소 70~74)
    indoor_temp: 'indoor_current_temperature',        // 내부현재온도 (70)
    indoor_humidity: 'indoor_current_humidity',       // 내부현재습도 (71)
    indoor_solar: 'indoor_current_solar_radiation',   // 내부현재일사량 (72)
    indoor_moisture: 'indoor_current_moisture',       // 내부현재함수율 (73)
    indoor_soil_tension: 'indoor_current_soil_tension', // 내부현재수분장력 (74)
    
    // 외부 센서 (워드주소 75~79)
    outdoor_temp: 'outdoor_current_temperature',      // 외부현재온도 (75)
    outdoor_humidity: 'outdoor_current_humidity',     // 외부현재습도 (76)
    outdoor_solar: 'outdoor_solar_radiation',         // 외부일사량 (77)
    outdoor_wind_dir: 'indoor_wind_direction',        // 내부풍향 (78)
    outdoor_wind_speed: 'outdoor_wind_speed',         // 외부풍속 (79)
  },
  
  // 🎛️ 주요 설정 항목 매핑 (UI → REST API 영어 이름)
  SETTING_KEYS: {
    // 모드 제어 (BIT_WRITE)
    dehumidifier_auto: 'dehumidifier_auto_mode',           // 제습오토모드
    circulation_fan_auto: 'circulation_fan_auto_mode',     // 유동팬오토모드
    heating_auto: 'heating_auto_mode',                     // 난방오토모드
    irrigation_auto: 'irrigation_auto_mode',               // 관수오토모드
    lighting_auto: 'lighting_auto_mode',                   // 조명오토모드
    
    // 온도 설정 (REGISTER_WRITE)
    heating_on_temp: 'heating_on_temperature_setting',     // 난방ON온도설정
    heating_off_temp: 'heating_off_temperature_setting',   // 난방OFF온도설정
    circulation_fan_on_temp: 'circulation_fan_on_temperature', // 유동팬ON온도
    circulation_fan_off_temp: 'circulation_fan_off_temperature', // 유동팬OFF온도
  },
  
  // ⏱️ 센서 데이터 새로고침 주기 (밀리초)
  REFRESH_INTERVAL: 10000, // 10초
  
  // 📹 CCTV/모니터링 RTSP 주소 (실제 RTSP 주소로 변경)
  RTSP_STREAMS: {
    entrance: '',  // 온실 입구
    center: '',    // 온실 중앙
    side_a: '',    // 온실 측면 A
    side_b: '',    // 온실 측면 B
  },
  
  // ⏳ 요청 타임아웃 (밀리초)
  TIMEOUT: 5000,
  
  // 🔄 재시도 설정
  RETRY: {
    maxAttempts: 3,
    delay: 1000,
  }
};

// 🛠️ 설정 수정 유틸리티
const ConfigManager = {
  // API 기본 주소 변경 (서버 IP 변경 시 사용)
  // 예: ConfigManager.setBaseURL('http://192.168.1.100:8000')
  setBaseURL: (url) => {
    API_CONFIG.BASE_URL = url;
    console.log(`✅ REST API 서버 주소 변경: ${url}`);
  },
  
  // 현재 서버 주소 가져오기
  getBaseURL: () => {
    return API_CONFIG.BASE_URL;
  },
  
  // RTSP 스트림 주소 설정
  setRTSPStream: (key, url) => {
    if (API_CONFIG.RTSP_STREAMS.hasOwnProperty(key)) {
      API_CONFIG.RTSP_STREAMS[key] = url;
      console.log(`✅ RTSP 스트림 설정: ${key} = ${url}`);
    }
  },
  
  // 전체 센서 키 매핑 가져오기
  getSensorKeys: () => {
    return API_CONFIG.SENSOR_KEYS;
  },
  
  // 전체 설정 키 매핑 가져오기
  getSettingKeys: () => {
    return API_CONFIG.SETTING_KEYS;
  },
  
  // 설정 전체 가져오기
  getConfig: () => {
    return API_CONFIG;
  },
  
  // 서버 연결 테스트
  testConnection: async () => {
    try {
      const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.HEALTH}`);
      const data = await response.json();
      console.log('✅ 서버 연결 성공:', data);
      return { success: true, data };
    } catch (error) {
      console.error('❌ 서버 연결 실패:', error);
      return { success: false, error: error.message };
    }
  }
};

// 전역에서 사용 가능하도록 내보내기
if (typeof window !== 'undefined') {
  window.API_CONFIG = API_CONFIG;
  window.ConfigManager = ConfigManager;
}

