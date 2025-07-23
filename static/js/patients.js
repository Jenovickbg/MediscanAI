// JS pour la gestion des patients avec modals et AJAX

document.addEventListener('DOMContentLoaded', function() {
    lucide.createIcons();

    // Ouvre le modal d'ajout
    document.getElementById('openAddPatientModal').onclick = function() {
        openPatientModal('ajouter');
    };

    // Recherche rapide
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const filter = this.value.toLowerCase();
            document.querySelectorAll('.patient-table tbody tr').forEach(row => {
                row.style.display = row.textContent.toLowerCase().includes(filter) ? '' : 'none';
            });
        });
    }
});

function openPatientModal(action, patientId = null) {
    fetch(action === 'ajouter' ? '/patients/ajouter/' : `/patients/modifier/${patientId}/`)
        .then(res => res.text())
        .then(html => {
            document.getElementById('patientModal').innerHTML = html;
            document.getElementById('patientModal').style.display = 'block';
            lucide.createIcons();
            bindPatientForm(action, patientId);
        });
}

function closePatientModal() {
    document.getElementById('patientModal').style.display = 'none';
}

function bindPatientForm(action, patientId) {
    const form = document.getElementById('patientForm');
    if (!form) return;
    form.onsubmit = function(e) {
        e.preventDefault();
        const url = action === 'ajouter' ? '/patients/ajouter/' : `/patients/modifier/${patientId}/`;
        const formData = new FormData(form);
        fetch(url, {
            method: 'POST',
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                location.reload();
            }
        });
    };
}

function openEditPatientModal(patientId) {
    openPatientModal('modifier', patientId);
}

function openDeletePatientModal(patientId) {
    fetch(`/patients/supprimer/${patientId}/`)
        .then(res => res.text())
        .then(html => {
            document.getElementById('deleteModal').innerHTML = html;
            document.getElementById('deleteModal').style.display = 'block';
            lucide.createIcons();
            bindDeleteForm(patientId);
        });
}

function closeDeleteModal() {
    document.getElementById('deleteModal').style.display = 'none';
}

function bindDeleteForm(patientId) {
    const form = document.getElementById('deleteForm');
    if (!form) return;
    form.onsubmit = function(e) {
        e.preventDefault();
        fetch(`/patients/supprimer/${patientId}/`, {
            method: 'POST',
            headers: { 'X-CSRFToken': getCSRFToken() }
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                location.reload();
            }
        });
    };
}

function openHistoriqueModal(patientId) {
    fetch(`/patients/historique/${patientId}/`)
        .then(res => res.text())
        .then(html => {
            document.getElementById('historiqueModal').innerHTML = html;
            document.getElementById('historiqueModal').style.display = 'block';
            lucide.createIcons();
        });
}

function closeHistoriqueModal() {
    document.getElementById('historiqueModal').style.display = 'none';
}

function openAddHistoriqueModal(patientId) {
    fetch(`/patients/ajouter-acte/${patientId}/`)
        .then(res => res.text())
        .then(html => {
            document.getElementById('addHistoriqueModal').innerHTML = html;
            document.getElementById('addHistoriqueModal').style.display = 'block';
            lucide.createIcons();
            bindHistoriqueForm(patientId);
        });
}

function closeAddHistoriqueModal() {
    document.getElementById('addHistoriqueModal').style.display = 'none';
}

function bindHistoriqueForm(patientId) {
    const form = document.getElementById('historiqueForm');
    if (!form) return;
    form.onsubmit = function(e) {
        e.preventDefault();
        fetch(`/patients/ajouter-acte/${patientId}/`, {
            method: 'POST',
            body: new FormData(form)
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                closeAddHistoriqueModal();
                openHistoriqueModal(patientId);
            }
        });
    };
}

function getCSRFToken() {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'csrftoken') return value;
    }
    return '';
} 