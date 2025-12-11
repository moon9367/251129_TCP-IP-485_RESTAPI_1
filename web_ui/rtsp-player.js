// RTSP 스트림 플레이어 관리
class RTSPPlayerManager {
  constructor() {
    this.config = API_CONFIG || {};
    this.players = {};
  }

  // RTSP 스트림 URL 가져오기
  getRTSPUrl(channel) {
    const streams = this.config.RTSP_STREAMS || {};
    return streams[channel] || '';
  }

  // 비디오 플레이어 초기화
  initPlayer(channelId) {
    const screenEl = document.querySelector(`[data-channel="${channelId}"]`);
    if (!screenEl) {
      console.error(`Channel ${channelId} not found`);
      return;
    }

    const rtspUrl = this.getRTSPUrl(channelId);
    
    if (!rtspUrl) {
      // RTSP URL이 없으면 NO SIGNAL 표시
      screenEl.innerHTML = `
        <div class="no-signal">
          <div class="no-signal-icon">📹</div>
          <div class="no-signal-text">NO SIGNAL</div>
          <div style="font-size: 11px; margin-top: 8px; opacity: 0.6;">RTSP 주소 미설정</div>
        </div>
      `;
      return;
    }

    // RTSP 스트림 표시
    // 참고: 브라우저에서 RTSP를 직접 재생하려면 변환 서버가 필요함
    // 여기서는 RTSP를 HLS/MPEG-DASH로 변환하는 예시를 제공
    
    this.players[channelId] = this._createVideoPlayer(rtspUrl, screenEl);
  }

  // 비디오 플레이어 생성 (예시)
  _createVideoPlayer(url, container) {
    // 실제 구현 시에는 RTSP를 HLS로 변환하는 서버가 필요
    // 예: ffmpeg + nginx-rtmp-module 또는 MediaMTX
    
    // 임시 구현: img 태그로 표시
    const player = {
      container: container,
      url: url,
      element: null,
    };

    // 예시: HLS 플레이어 사용
    // 실제로는 HLS.js 또는 비슷한 라이브러리 필요
    container.innerHTML = `
      <div class="no-signal">
        <div class="no-signal-icon">📹</div>
        <div class="no-signal-text">STREAMING</div>
        <div style="font-size: 11px; margin-top: 8px; opacity: 0.6;">${url}</div>
        <div style="font-size: 10px; margin-top: 4px; opacity: 0.4;">
          (RTSP 스트림은 변환 서버 필요)
        </div>
      </div>
    `;

    return player;
  }

  // HLS 플레이어 초기화 (실제 구현 예시)
  initHLSPlayer(url, container) {
    // HLS.js 라이브러리 필요
    // import Hls from 'hls.js';
    
    /*
    const video = document.createElement('video');
    video.controls = true;
    video.style.width = '100%';
    video.style.height = '100%';
    
    if (Hls.isSupported()) {
      const hls = new Hls();
      hls.loadSource(url);
      hls.attachMedia(video);
    } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
      video.src = url;
    }
    
    container.appendChild(video);
    return { container, url, element: video, hls };
    */
  }

  // 모든 채널 초기화
  initAll() {
    const channels = ['entrance', 'center', 'side_a', 'side_b'];
    channels.forEach(channel => {
      this.initPlayer(channel);
    });
  }

  // 특정 채널 시작
  start(channelId) {
    const player = this.players[channelId];
    if (player && player.element) {
      player.element.play().catch(e => console.error(`Failed to play ${channelId}:`, e));
    }
  }

  // 특정 채널 중지
  stop(channelId) {
    const player = this.players[channelId];
    if (player && player.element) {
      player.element.pause();
    }
  }

  // 모든 채널 중지
  stopAll() {
    Object.keys(this.players).forEach(channelId => {
      this.stop(channelId);
    });
  }

  // 채널 정리
  destroy(channelId) {
    const player = this.players[channelId];
    if (player && player.element) {
      player.element.pause();
      player.element.src = '';
      player.element.remove();
    }
    delete this.players[channelId];
  }

  // 모든 채널 정리
  destroyAll() {
    Object.keys(this.players).forEach(channelId => {
      this.destroy(channelId);
    });
  }
}

// 전역 인스턴스 생성
const rtspPlayer = new RTSPPlayerManager();

// 전역에서 사용 가능하도록 내보내기
if (typeof window !== 'undefined') {
  window.RTSPPlayerManager = RTSPPlayerManager;
  window.rtspPlayer = rtspPlayer;
}



