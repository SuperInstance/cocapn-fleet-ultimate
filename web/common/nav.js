// Shared navigation component for all fleet pages
function initNav() {
  const currentPage = window.location.pathname.split('/').pop() || 'index.html';
  const isLanding = currentPage === 'index.html' && window.location.pathname.includes('/landing/');
  
  const nav = document.createElement('nav');
  nav.className = 'fleet-nav';
  nav.innerHTML = `
    <div class="fleet-nav-inner">
      <a href="${isLanding ? '#' : '../landing/index.html'}" class="fleet-logo">
        <div class="fleet-logo-icon"></div>
        <span>Cocapn Fleet</span>
      </a>
      <ul class="nav-links">
        <li><a href="${isLanding ? '#features' : '../landing/index.html#features'}">Features</a></li>
        <li><a href="${isLanding ? '#architecture' : '../landing/index.html#architecture'}">Architecture</a></li>
        <li><a href="../demos/turbovec.html">Demos</a></li>
        <li><a href="../tutorials/index.html">Tutorials</a></li>
        <li><a href="https://github.com/SuperInstance/sunset-ecosystem" target="_blank">GitHub</a></li>
      </ul>
    </div>
  `;
  
  document.body.insertBefore(nav, document.body.firstChild);
}

// Intersection Observer for scroll animations
function initScrollAnimations() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animate-fade-in');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });
  
  document.querySelectorAll('.scroll-animate').forEach(el => {
    el.style.opacity = '0';
    observer.observe(el);
  });
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    initNav();
    initScrollAnimations();
  });
} else {
  initNav();
  initScrollAnimations();
}
