document.addEventListener('DOMContentLoaded', () => {

    const currentUserStr = localStorage.getItem('qwork_currentUser');
    const guestActions = document.getElementById('guest-actions');
    const userActions = document.getElementById('user-actions');
    const userNameDisplay = document.getElementById('user-name-display');

    if (currentUserStr) {
        const currentUser = JSON.parse(currentUserStr);
        if (guestActions && userActions) {
            guestActions.style.display = 'none';
            userActions.style.display = 'flex';
            if (userNameDisplay) userNameDisplay.textContent = currentUser.first_name;
            document.getElementById('user-avatar').setAttribute('src', `https://ui-avatars.com/api/?name=${currentUser.f}&background=random`);
        }
    } else {
        if (guestActions && userActions) {
            guestActions.style.display = 'flex';
            userActions.style.display = 'none';
        }
    }

    

    const animatedElements = document.querySelectorAll('.animate-on-scroll');

    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const index = Array.from(animatedElements).indexOf(entry.target);
                    setTimeout(() => {
                        entry.target.style.opacity = '1';
                        entry.target.style.transform = 'translateY(0)';
                    }, 50 * index); 
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });

        
        animatedElements.forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px)';
            el.style.transition = 'opacity 0.6s cubic-bezier(0.16, 1, 0.3, 1), transform 0.6s cubic-bezier(0.16, 1, 0.3, 1)';
            observer.observe(el);
        });
    } else {
        
        animatedElements.forEach(el => {
            el.style.opacity = '1';
            el.style.transform = 'translateY(0)';
        });
    }

    
    // User Dropdown Toggle
    const profileTrigger = document.getElementById('profile-trigger');
    const userDropdown = document.getElementById('user-dropdown');

    if (profileTrigger && userDropdown) {
        profileTrigger.addEventListener('click', (e) => {
            e.stopPropagation();
            userDropdown.classList.toggle('active');
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', (e) => {
            if (userDropdown.classList.contains('active') && !userDropdown.contains(e.target)) {
                userDropdown.classList.remove('active');
            }
        });
    }
});


window.logoutUser = function (e) {
    if (e) e.preventDefault();
    localStorage.removeItem('qwork_currentUser');
    localStorage.removeItem('access_token');
    window.location.href = 'index.html';
};
