// Upload et Analyse JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const imageInput = document.getElementById('imageInput');
    const uploadPlaceholder = document.querySelector('.upload-placeholder');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const resultsSection = document.getElementById('resultsSection');

    // Drag & Drop
    const fileUploadArea = document.querySelector('.file-upload-area');
    
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        fileUploadArea.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        fileUploadArea.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        fileUploadArea.addEventListener(eventName, unhighlight, false);
    });

    function highlight(e) {
        fileUploadArea.classList.add('drag-over');
    }

    function unhighlight(e) {
        fileUploadArea.classList.remove('drag-over');
    }

    fileUploadArea.addEventListener('drop', handleDrop, false);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        imageInput.files = files;
        updateFileDisplay();
    }

    // Sélection de fichier
    imageInput.addEventListener('change', updateFileDisplay);

    function updateFileDisplay() {
        const file = imageInput.files[0];
        if (file) {
            uploadPlaceholder.innerHTML = `
                <i data-lucide="check-circle"></i>
                <p>${file.name}</p>
                <span>${(file.size / 1024 / 1024).toFixed(2)} MB</span>
            `;
            uploadPlaceholder.classList.add('file-selected');
            analyzeBtn.disabled = false;
        } else {
            uploadPlaceholder.innerHTML = `
                <i data-lucide="upload-cloud"></i>
                <p>Cliquez ou glissez une image ici</p>
                <span>Formats acceptés: JPG, PNG, GIF</span>
            `;
            uploadPlaceholder.classList.remove('file-selected');
            analyzeBtn.disabled = true;
        }
        lucide.createIcons();
    }

    // Soumission du formulaire
    uploadForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(uploadForm);
        const file = imageInput.files[0];
        
        if (!file) {
            showNotification('Veuillez sélectionner une image', 'warning');
            return;
        }

        // Vérifier la taille du fichier (max 10MB)
        if (file.size > 10 * 1024 * 1024) {
            showNotification('Le fichier est trop volumineux (max 10MB)', 'error');
            return;
        }

        // Afficher le chargement
        analyzeBtn.disabled = true;
        analyzeBtn.innerHTML = '<i data-lucide="loader-2" class="spinning"></i> Analyse en cours...';
        
        // Envoyer la requête
        fetch(window.location.href, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                displayResults(data);
                showNotification('Analyse terminée avec succès', 'success');
            } else {
                const errorMessage = data.error || 'Erreur lors de l\'analyse';
                showNotification(errorMessage, 'error');
                console.error('Erreur détaillée:', data);
            }
        })
        .catch(error => {
            console.error('Erreur:', error);
            showNotification('Erreur de connexion lors de l\'analyse', 'error');
        })
        .finally(() => {
            analyzeBtn.disabled = false;
            analyzeBtn.innerHTML = '<i data-lucide="play"></i> Analyser le frottis';
        });
    });
});

// Afficher les résultats
function displayResults(data) {
    const resultsSection = document.getElementById('resultsSection');
    const diagnosticResult = document.getElementById('diagnosticResult');
    const confidenceBadge = document.getElementById('confidenceBadge');
    const analysisDate = document.getElementById('analysisDate');

    // Afficher le diagnostic
    diagnosticResult.innerHTML = `
        <div class="diagnostic ${data.diagnostic.toLowerCase()}">
            ${data.diagnostic}
        </div>
    `;

    // Afficher la confiance
    confidenceBadge.textContent = `${data.confiance}%`;
    confidenceBadge.className = `confidence-badge ${getConfidenceClass(data.confiance)}`;

    // Afficher la date
    analysisDate.textContent = new Date().toLocaleString('fr-FR');

    // Afficher la section résultats
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

// Classe CSS pour la confiance
function getConfidenceClass(confidence) {
    if (confidence >= 90) return 'high';
    if (confidence >= 75) return 'medium';
    return 'low';
}

// Sauvegarder les résultats
function saveResults() {
    showNotification('Résultats sauvegardés', 'success');
    setTimeout(() => {
        window.location.href = '/diagnostics/';
    }, 1500);
}

// Nouvelle analyse
function newAnalysis() {
    document.getElementById('uploadForm').reset();
    document.getElementById('resultsSection').style.display = 'none';
    updateFileDisplay();
}

// Notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
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
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
} 