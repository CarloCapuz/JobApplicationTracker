// Job Application Tracker JavaScript

// Global variables
let allApplications = [];
let filteredApplications = [];
let activeStatusFilter = 'all';

// Utility functions
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        background-color: ${type === 'success' ? '#4caf50' : '#f44336'};
        color: white;
        border-radius: 8px;
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Add CSS animations for notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style);

// Load summary statistics
function loadSummary() {
    fetch('/api/summary')
        .then(response => response.json())
        .then(data => {
            document.getElementById('total-count').textContent = data.total;
            document.getElementById('waiting-count').textContent = data.by_status['Waiting for hearback'] || 0;
            document.getElementById('denied-count').textContent = data.by_status['Denied'] || 0;
            document.getElementById('interview-count').textContent = data.by_status['Interview'] || 0;
            document.getElementById('interview2-count').textContent = data.by_status['Interview 2'] || 0;
            document.getElementById('interview3-count').textContent = data.by_status['Interview 3'] || 0;
            document.getElementById('offer-count').textContent = data.by_status['Offer'] || 0;
        })
        .catch(error => {
            console.error('Error loading summary:', error);
        });
}

// Load all applications
function loadApplications() {
    const sortBy = document.getElementById('sort-select').value;
    const order = document.getElementById('order-select').value;
    
    fetch(`/api/applications?sort=${sortBy}&order=${order}`)
        .then(response => response.json())
        .then(data => {
            allApplications = data;
            filteredApplications = [...allApplications];
            renderApplications();
        })
        .catch(error => {
            console.error('Error loading applications:', error);
        });
}

// Filter applications based on search input
function applyFilters() {
    const searchTerm = document.getElementById('search-input').value.toLowerCase().trim();
    
    // Start from all apps
    filteredApplications = [...allApplications];
    
    // Apply status filter (if not 'all')
    if (activeStatusFilter !== 'all') {
        filteredApplications = filteredApplications.filter(app => app.status === activeStatusFilter);
    }

    // Apply search filter
    if (searchTerm !== '') {
        filteredApplications = filteredApplications.filter(app => {
            return app.company_name.toLowerCase().includes(searchTerm) ||
                   app.job_role.toLowerCase().includes(searchTerm) ||
                   app.status.toLowerCase().includes(searchTerm) ||
                   (app.notes ? app.notes.toLowerCase().includes(searchTerm) : false);
        });
    }
    
    renderApplications();
}

// Clear search
function clearSearch() {
    document.getElementById('search-input').value = '';
    applyFilters();
}

// Render applications to the DOM
function renderApplications() {
    const grid = document.querySelector('.applications-grid');
    
    if (filteredApplications.length === 0) {
        grid.innerHTML = `
            <div class="empty-state">
                <h2>No applications found</h2>
                <p>Try adjusting your search criteria or add a new application.</p>
                <a href="/add" class="btn btn-primary">Add New Application</a>
            </div>
        `;
        return;
    }
    
    grid.innerHTML = filteredApplications.map(app => `
        <div class="application-card fade-in" data-status="${app.status}" data-app-id="${app.id}">
            <div class="card-header">
                <h3>${app.company_name}</h3>
                <span class="status-badge status-${app.status.toLowerCase().replace(' ', '-')}">
                    ${app.status}
                </span>
            </div>
            
            <div class="card-content">
                <p><strong>Position:</strong> ${app.job_role}</p>
                <p><strong>Applied:</strong> ${app.applied_date}</p>
                ${app.url ? `<p><strong>URL:</strong> <a href="${app.url}" target="_blank" class="url-link">View Job Posting</a></p>` : ''}
                ${app.notes && app.notes.trim() !== '' ? `
                <div class="notes-section">
                    <p><strong>Notes:</strong></p>
                    <p class="notes-text">${app.notes.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')}</p>
                </div>` : ''}
                <p><strong>Last Updated:</strong> ${app.last_updated}</p>
            </div>
            
            <div class="card-actions">
                <a href="/edit/${app.id}" class="btn btn-secondary">Edit</a>
                <button onclick="deleteApplication(${app.id})" class="btn btn-danger">Delete</button>
            </div>
        </div>
    `).join('');
}

// Sort functionality
function sortApplications() {
    loadApplications();
}

// Delete application functionality
function deleteApplication(appId) {
    if (confirm('Are you sure you want to delete this job application? This action cannot be undone.')) {
        fetch(`/delete/${appId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                showNotification('Application deleted successfully!');
                // Refresh data
                loadSummary();
                loadApplications();
            } else {
                showNotification('Error deleting application: ' + result.message, 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Error deleting application', 'error');
        });
    }
}

// Form submission for adding new applications
document.addEventListener('DOMContentLoaded', function() {
    const addForm = document.getElementById('application-form');
    if (addForm && window.location.pathname === '/add') {
        addForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const data = Object.fromEntries(formData);
            
            // Validate required fields
            if (!data.company_name || !data.job_role || !data.applied_date || !data.status) {
                showNotification('Please fill in all required fields', 'error');
                return;
            }
            
            fetch('/add', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(result => {
                if (result.success) {
                    showNotification('Job application added successfully!');
                    setTimeout(() => {
                        window.location.href = '/';
                    }, 1000);
                } else {
                    showNotification('Error adding application: ' + result.message, 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('Error adding application', 'error');
            });
        });
    }
    
    // Summary header click filters
    const summaryHeader = document.getElementById('summary-header');
    if (summaryHeader && window.location.pathname === '/') {
        summaryHeader.addEventListener('click', (e) => {
            const card = e.target.closest('.summary-card.clickable');
            if (!card) return;
            const status = card.getAttribute('data-status');
            setStatusFilter(status);
        });
    }
});

// Add fade out animation
const fadeOutStyle = document.createElement('style');
fadeOutStyle.textContent = `
    @keyframes fadeOut {
        from { opacity: 1; transform: scale(1); }
        to { opacity: 0; transform: scale(0.8); }
    }
`;
document.head.appendChild(fadeOutStyle);

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    // Load summary and applications on main page
    if (window.location.pathname === '/') {
        loadSummary();
        loadApplications();
    }
    
    // Add data attributes to cards for easier selection
    const cards = document.querySelectorAll('.application-card');
    cards.forEach(card => {
        const editLink = card.querySelector('a[href*="/edit/"]');
        if (editLink) {
            const appId = editLink.href.match(/\/edit\/(\d+)/)[1];
            card.setAttribute('data-app-id', appId);
        }
    });
});

// Set status filter and update UI
function setStatusFilter(status) {
    activeStatusFilter = status || 'all';
    updateSummaryActiveState();
    applyFilters();
}

function updateSummaryActiveState() {
    const cards = document.querySelectorAll('.summary-card.clickable');
    cards.forEach(card => {
        const cardStatus = card.getAttribute('data-status');
        if ((activeStatusFilter === 'all' && cardStatus === 'all') || cardStatus === activeStatusFilter) {
            card.classList.add('active');
        } else {
            card.classList.remove('active');
        }
    });
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + N to add new application
    if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
        e.preventDefault();
        window.location.href = '/add';
    }
    
    // Escape to go back to list
    if (e.key === 'Escape' && window.location.pathname !== '/') {
        window.location.href = '/';
    }
});

// Auto-save form data to localStorage (for better UX)
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('application-form');
    if (form) {
        // Load saved data
        const savedData = localStorage.getItem('jobApplicationForm');
        if (savedData && window.location.pathname === '/add') {
            try {
                const data = JSON.parse(savedData);
                Object.keys(data).forEach(key => {
                    const input = form.querySelector(`[name="${key}"]`);
                    if (input && input.type !== 'radio') {
                        input.value = data[key];
                    } else if (input && input.type === 'radio') {
                        const radio = form.querySelector(`[name="${key}"][value="${data[key]}"]`);
                        if (radio) radio.checked = true;
                    }
                });
            } catch (e) {
                console.log('No saved form data');
            }
        }
        
        // Save data on input change
        form.addEventListener('input', function() {
            const formData = new FormData(form);
            const data = Object.fromEntries(formData);
            localStorage.setItem('jobApplicationForm', JSON.stringify(data));
        });
        
        // Clear saved data on successful submission
        form.addEventListener('submit', function() {
            localStorage.removeItem('jobApplicationForm');
        });
    }
});

// Add smooth scrolling for better UX
document.documentElement.style.scrollBehavior = 'smooth';

// Add loading states for better UX
function addLoadingState(element) {
    element.classList.add('loading');
    element.style.pointerEvents = 'none';
}

function removeLoadingState(element) {
    element.classList.remove('loading');
    element.style.pointerEvents = 'auto';
}

// Enhanced form validation
function validateForm(form) {
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.style.borderColor = '#f44336';
            isValid = false;
        } else {
            field.style.borderColor = '';
        }
    });
    
    return isValid;
}

// Add form validation styling
const validationStyle = document.createElement('style');
validationStyle.textContent = `
    .form-group input:invalid {
        border-color: #f44336 !important;
    }
    
    .form-group input:valid {
        border-color: #4caf50 !important;
    }
`;
document.head.appendChild(validationStyle);

