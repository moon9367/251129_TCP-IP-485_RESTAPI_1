// 대시보드 초기화
document.addEventListener('DOMContentLoaded', () => {
  console.log('스마트팜 데시보드 초기화 중...');

  // 사이드바 토글 이벤트
  initSidebarToggle();

  // 네비게이션 클릭 이벤트
  initNavigation();

  // 토글 스위치 이벤트
  initToggleSwitches();

  // 탭 클릭 이벤트
  initChartTabs();

  // AI 제안 액션 이벤트
  initAIActions();

  // 데이터 새로고침 버튼
  initRefreshButton();

  // REST API 연동 시작
  initAPIConnection();
  
  // 차트 초기화
  if (typeof chartManager !== 'undefined') {
    chartManager.init();
  }

  console.log('데시보드 준비 완료');
});

// 사이드바 토글 처리
function initSidebarToggle() {
  const sidebarToggle = document.getElementById('sidebarToggle');
  const appShell = document.querySelector('.app-shell');

  if (sidebarToggle && appShell) {
    sidebarToggle.addEventListener('click', () => {
      appShell.classList.toggle('sidebar-collapsed');
      console.log('사이드바 토글');
    });
  }
}

// 네비게이션 처리
function initNavigation() {
  // 이제 링크로 동작하므로 네비게이션 클릭 처리는 필요 없음
  // active 클래스는 각 페이지 HTML에서 직접 지정됨
}

// 토글 스위치 처리
function initToggleSwitches() {
  const toggles = document.querySelectorAll('.toggle');
  toggles.forEach(toggle => {
    toggle.addEventListener('click', (e) => {
      e.stopPropagation();
      
      const card = toggle.closest('.control-card');
      const deviceName = card?.querySelector('header strong')?.textContent || '알 수 없음';
      
      // off 클래스가 있으면 제거하고 on 추가, 없으면 반대
      toggle.classList.toggle('on');
      toggle.classList.toggle('off');
      
      // 토글 후 상태로 판단
      const isOn = toggle.classList.contains('on');
      
      // 모드 변경: ON = 수동, OFF = 자동 (수정됨)
      const chipEl = card?.querySelector('.chip');
      const modeValue = toggle.getAttribute('data-mode');
      if (chipEl) {
        if (isOn) {
          toggle.setAttribute('data-mode', '수동');
          chipEl.textContent = '수동';
          chipEl.classList.remove('auto');
          chipEl.classList.add('manual');
        } else {
          toggle.setAttribute('data-mode', '자동');
          chipEl.textContent = '자동';
          chipEl.classList.remove('manual');
          chipEl.classList.add('auto');
        }
      }
      
      // 설명 텍스트 업데이트
      const descSpan = card?.querySelector('header .title span');
      if (descSpan && isOn) {
        descSpan.textContent = descSpan.textContent.replace('자동', '수동').replace('Auto', '수동').replace('Manual', '수동');
      } else if (descSpan && !isOn) {
        descSpan.textContent = descSpan.textContent.replace('수동', '자동').replace('Manual', '자동').replace('Auto', '자동');
      }
      
      const statusSpan = card?.querySelector('footer span:last-child');
      if (statusSpan) {
        statusSpan.textContent = isOn ? 'ON' : 'OFF';
        statusSpan.style.color = isOn 
          ? getComputedStyle(document.documentElement).getPropertyValue('--accent').trim()
          : getComputedStyle(document.documentElement).getPropertyValue('--text-soft').trim();
      }
      
      console.log(`${deviceName}: ${isOn ? '수동 ON' : '자동 OFF'}로 변경`);
    });
  });
}

// 차트 탭 처리
function initChartTabs() {
  const tabs = document.querySelectorAll('.chart-header .tabs span');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      
      console.log(`차트 탭 변경: ${tab.textContent.trim()}`);
    });
  });
}

// AI 제안 액션 처리
function initAIActions() {
  const actionButtons = document.querySelectorAll('.ai-item .actions span');
  actionButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      
      const action = btn.textContent.trim();
      const aiItem = btn.closest('.ai-item');
      const title = aiItem?.querySelector('strong')?.textContent || '';
      
      console.log(`AI 액션 실행: ${title} - ${action}`);
      
      // 예시: 실제로는 API 호출 등을 수행
      if (action.includes('즉시') || action.includes('자동')) {
        btn.style.opacity = '0.5';
        setTimeout(() => {
          btn.textContent = '처리됨';
        }, 500);
      } else if (action.includes('나중에') || action.includes('숨기기') || action === '무시') {
        aiItem.style.opacity = '0.3';
        setTimeout(() => {
          aiItem.style.display = 'none';
        }, 300);
      }
    });
  });
}

// 데이터 새로고침 버튼
function initRefreshButton() {
  const refreshBtn = document.querySelector('.top-actions button');
  if (!refreshBtn) return;
  
  refreshBtn.addEventListener('click', () => {
    console.log('데이터 새로고침 요청');
    
    // 로딩 상태 표시
    refreshBtn.textContent = '새로고침 중...';
    refreshBtn.disabled = true;
    
    // 예시: 실제로는 API 호출
    setTimeout(() => {
      refreshBtn.textContent = '데이터 새로고침';
      refreshBtn.disabled = false;
      console.log('새로고침 완료');
      
      // UI 업데이트 예시
      updateLastRefreshTime();
    }, 1500);
  });
}

// 마지막 새로고침 시간 업데이트
function updateLastRefreshTime() {
  const sidebarFooter = document.querySelector('.sidebar-footer');
  if (sidebarFooter) {
    const now = new Date();
    const timeStr = now.toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' });
    const period = now.getHours() >= 12 ? '오후' : '오전';
    sidebarFooter.innerHTML = `
      실시간 데이터 수집 <strong>ON</strong><br />
      최근 업데이트: 오늘 ${period} ${timeStr}
    `;
  }
}

// 센서 데이터 시뮬레이션 (향후 실제 API와 교체)
function simulateSensorData() {
  // 내부 센서 카드의 값을 약간 변경
  const sensorCards = document.querySelectorAll('.sensor-card');
  sensorCards.forEach(card => {
    const valueEl = card.querySelector('.value');
    if (valueEl && Math.random() > 0.7) {
      const currentValue = valueEl.textContent;
      console.log(`센서 값 업데이트: ${currentValue}`);
    }
  });
}

// REST API 연동 초기화
function initAPIConnection() {
  if (typeof dataManager === 'undefined') {
    console.warn('DataManager is not available');
    return;
  }
  
  // 데이터 업데이트 콜백 등록
  dataManager.onUpdate((sensorData) => {
    console.log('Sensor data updated:', sensorData);
    dataManager.updateAllSensors(sensorData);
  });
  
  // 자동 새로고침 시작
  dataManager.start();
  
  console.log('REST API connection initialized');
}

