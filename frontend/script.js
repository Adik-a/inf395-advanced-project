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
            if (userNameDisplay) userNameDisplay.textContent = currentUser.fname || 'User';
        }
    } else {
        if (guestActions && userActions) {
            guestActions.style.display = 'flex';
            userActions.style.display = 'none';
        }
    }

    

    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry, index) => {
                if (entry.isIntersecting) {
                    
                    setTimeout(() => {
                        entry.target.style.opacity = '1';
                        entry.target.style.transform = 'translateY(0)';
                    }, 50 * index); // very short delay for each item

                    
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

    
    const badge = document.querySelector('.floating-badge');
    if (badge) {
        let posY = 0;
        let direction = 1;

    }
});


window.logoutUser = function (e) {
    if (e) e.preventDefault();
    localStorage.removeItem('qwork_currentUser');
    localStorage.removeItem('access_token');
    window.location.href = 'index.html';
};
