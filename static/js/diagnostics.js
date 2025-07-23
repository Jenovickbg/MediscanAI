// Diagnostics JavaScript

// Variables globales
let currentPatientId = null;

// Fonctions pour les modals
function openSearchPatientModal() {
    document.getElementById('searchPatientModal').style.display = 'block';
    document.getElementById('patientSearch').focus();
}

function closeSearchPatientModal() {
    document.getElementById('searchPatientModal').style.display = 'none';
    document.getElementById('patientResults').innerHTML = '';
    document.getElementById('patientSearch').value = '';
}

// Recherche de patient
function searchPatient() {
    const query = document.getElementById('patientSearch').value.trim();
    if (!query) {
        showNotification('Veuillez entrer un terme de recherche', 'warning');
        return;
    }

    // Afficher un indicateur de chargement
    document.getElementById('patientResults').innerHTML = '<p>Recherche en cours...</p>';

    // Faire la requête AJAX
    fetch(`/diagnostics/recherche-patient/?q=${encodeURIComponent(query)}`)
        .then(response => response.text())
        .then(html => {
            // Extraire les résultats du HTML
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const results = doc.querySelectorAll('.patient-result-item');
            
            if (results.length > 0) {
                document.getElementById('patientResults').innerHTML = '';
                results.forEach(result => {
                    document.getElementById('patientResults').appendChild(result.cloneNode(true));
                });
            } else {
                document.getElementById('patientResults').innerHTML = '<p>Aucun patient trouvé</p>';
            }
        })
        .catch(error => {
            console.error('Erreur lors de la recherche:', error);
            document.getElementById('patientResults').innerHTML = '<p>Erreur lors de la recherche</p>';
        });
}

// Sélectionner un patient
function selectPatient(patientId, patientName) {
    currentPatientId = patientId;
    closeSearchPatientModal();
    
    // Rediriger vers la page d'upload
    window.location.href = `/diagnostics/upload/${patientId}/`;
}

// Recherche dans les frottis
function searchFrottis() {
    const query = document.getElementById('searchFrottis').value.toLowerCase();
    const cards = document.querySelectorAll('.frottis-card');
    
    cards.forEach(card => {
        const patientName = card.querySelector('h4').textContent.toLowerCase();
        const diagnostic = card.querySelector('.diagnostic').textContent.toLowerCase();
        
        if (patientName.includes(query) || diagnostic.includes(query)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

// Voir le détail d'un frottis
function viewFrottisDetail(frottisId) {
    window.location.href = `/diagnostics/detail/${frottisId}/`;
}

// Voir l'historique d'un patient
function viewPatientHistory(patientId) {
    window.location.href = `/diagnostics/historique/${patientId}/`;
}

// Notification
function showNotification(message, type = 'info') {
    // Créer l'élément de notification
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Styles de base
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        color: white;
        font-weight: 500;
        z-index: 10000;
        animation: slideIn 0.3s ease;
        max-width: 300px;
    `;
    
    // Couleurs selon le type
    switch(type) {
        case 'success':
            notification.style.backgroundColor = '#27ae60';
            break;
        case 'error':
            notification.style.backgroundColor = '#e74c3c';
            break;
        case 'warning':
            notification.style.backgroundColor = '#f39c12';
            break;
        default:
            notification.style.backgroundColor = '#3498db';
    }
    
    // Ajouter au DOM
    document.body.appendChild(notification);
    
    // Supprimer après 3 secondes
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

// Gestion du clavier pour la recherche
document.addEventListener('DOMContentLoaded', function() {
    // Recherche patient avec Entrée
    const patientSearch = document.getElementById('patientSearch');
    if (patientSearch) {
        patientSearch.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                searchPatient();
            }
        });
    }
    
    // Recherche frottis en temps réel
    const searchFrottisInput = document.getElementById('searchFrottis');
    if (searchFrottisInput) {
        searchFrottisInput.addEventListener('input', searchFrottis);
    }
    
    // Fermer modal en cliquant à l'extérieur
    const modal = document.getElementById('searchPatientModal');
    if (modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                closeSearchPatientModal();
            }
        });
    }
    
    // Fermer modal avec Échap
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeSearchPatientModal();
        }
    });
});

// CSS pour les animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style); 