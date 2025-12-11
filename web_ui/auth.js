// 인증 관리 스크립트

// 로그인 처리
document.addEventListener('DOMContentLoaded', () => {
  // 이미 로그인되어 있으면 대시보드로 리다이렉트
  if (window.location.pathname.includes('login.html')) {
    if (checkAuth()) {
      window.location.href = 'index.html';
      return;
    }

    // 로그인 폼 처리
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
      loginForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        const remember = document.getElementById('remember').checked;

        if (username === 'admin' && password === 'admin') {
          // 로그인 성공
          setAuth(username, remember);
          window.location.href = 'index.html';
        } else {
          // 로그인 실패
          alert('아이디 또는 비밀번호가 잘못되었습니다.\n\n임시 로그인 정보: admin / admin');
        }
      });
    }
  } else {
    // 다른 페이지에서 로그인 체크
    if (!checkAuth()) {
      window.location.href = 'login.html';
      return;
    }
  }

  // 프로필 정보 표시
  updateProfileUI();
});

// 인증 상태 설정
function setAuth(username, remember) {
  sessionStorage.setItem('username', username);
  sessionStorage.setItem('loggedIn', 'true');
  
  if (remember) {
    localStorage.setItem('username', username);
    localStorage.setItem('loggedIn', 'true');
  }
}

// 인증 상태 확인
function checkAuth() {
  // 세션 또는 로컬 스토리지에서 로그인 상태 확인
  const sessionLoggedIn = sessionStorage.getItem('loggedIn') === 'true';
  const localLoggedIn = localStorage.getItem('loggedIn') === 'true';
  
  if (sessionLoggedIn || localLoggedIn) {
    // 로그인 상태 복원
    if (!sessionLoggedIn && localLoggedIn) {
      const username = localStorage.getItem('username');
      sessionStorage.setItem('username', username);
      sessionStorage.setItem('loggedIn', 'true');
    }
    return true;
  }
  
  return false;
}

// 현재 사용자 가져오기
function getCurrentUser() {
  return sessionStorage.getItem('username') || localStorage.getItem('username') || 'Guest';
}

// 로그아웃
function logout() {
  sessionStorage.removeItem('username');
  sessionStorage.removeItem('loggedIn');
  localStorage.removeItem('username');
  localStorage.removeItem('loggedIn');
  window.location.href = 'login.html';
}

// 프로필 UI 업데이트
function updateProfileUI() {
  const username = getCurrentUser();
  if (username === 'Guest') return;

  // 사이드바에 프로필 정보 추가
  const sidebar = document.querySelector('.sidebar');
  if (sidebar) {
    let profileSection = document.querySelector('.profile-section');
    
    if (!profileSection) {
      profileSection = document.createElement('div');
      profileSection.className = 'profile-section';
      sidebar.insertBefore(profileSection, sidebar.querySelector('nav'));
    }
    
    profileSection.innerHTML = `
      <div class="profile-info">
        <div class="profile-avatar">${username.charAt(0).toUpperCase()}</div>
        <div class="profile-details">
          <strong class="profile-name">${username}</strong>
          <span class="profile-role">관리자</span>
        </div>
        <button class="profile-logout" onclick="logout()" title="로그아웃">로그아웃</button>
      </div>
    `;
  }
}

