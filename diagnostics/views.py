from django.shortcuts import render
from .forms import BloodSmearForm
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import os
from openai import OpenAI, OpenAIError

# Paramètres image
img_height = 150
img_width = 150

# Charger le modèle .keras une seule fois
model_path = os.path.join('ml_model', 'malaria-cnn-v1.keras')
mon_modele = load_model(model_path)

# Fonction de prétraitement
def preprocess_image(image_file):
    image = Image.open(image_file).convert('RGB')
    image = image.resize((img_width, img_height))
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=0)
    return image

# Fonction pour interroger ChatGPT (ou fallback)
def get_chatgpt_interpretation(prediction_result, patient_info):
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        prompt = f"""
        Un patient a subi une analyse de frottis sanguins pour détecter le paludisme.
        Le modèle de deep learning a retourné le résultat suivant : {prediction_result}.
        
        Veuillez interpréter ce résultat médical et donner les recommandations suivantes :
        1. Interprétation des résultats (explique ce que cela signifie).
        2. Orientations médicales possibles (quelles étapes le médecin devrait-il suivre ?).
        3. Produits ou médicaments recommandés (si applicable, quel traitement est recommandé ?).
        """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un médecin spécialiste en diagnostic biologique."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("⚠️ Erreur avec OpenAI :", e)
        if prediction_result[0] > 0.5:
            return (
                "⚠️ *Interprétation générée automatiquement (API indisponible)*\n\n"
                "Le modèle suggère une **forte probabilité de présence du paludisme**. "
                "Un test rapide de confirmation est recommandé. Consultez un professionnel de santé immédiatement."
            )
        else:
            return (
                "⚠️ *Interprétation générée automatiquement (API indisponible)*\n\n"
                "Le modèle **ne détecte pas de signes significatifs de paludisme**. "
                "Cependant, une surveillance des symptômes et un avis médical restent recommandés."
            )

# Vue principale
def analyser_frottis(request):
    prediction = None
    interpretation = None
    if request.method == 'POST':
        form = BloodSmearForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            patient_id = form.cleaned_data['patient_id']
            image_traitée = preprocess_image(image)
            resultat = mon_modele.predict(image_traitée)
            prediction = resultat[0]

            patient_info = f"ID patient : {patient_id}, Sexe : Masculin, Âge : 35 ans"  # à adapter dynamiquement plus tard
            interpretation = get_chatgpt_interpretation(prediction, patient_info)

            form.save()

            return render(request, 'diagnostics/analyse.html', {
                'form': BloodSmearForm(),
                'prediction': prediction,
                'interpretation': interpretation,
                'patient_id': patient_id
            })
    else:
        form = BloodSmearForm()

    return render(request, 'diagnostics/analyse.html', {
        'form': form,
        'prediction': prediction,
        'interpretation': interpretation
    })
