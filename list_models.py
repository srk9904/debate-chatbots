"""
Script to list all available Gemini models
Run this to see what models you have access to
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure API
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print("❌ GEMINI_API_KEY not found in .env file")
    exit(1)

genai.configure(api_key=api_key)

print("\n" + "="*60)
print("Available Gemini Models")
print("="*60 + "\n")

try:
    models = genai.list_models()
    
    generative_models = []
    for model in models:
        if 'generateContent' in model.supported_generation_methods:
            generative_models.append(model.name)
            print(f"✓ {model.name}")
            print(f"  Display Name: {model.display_name}")
            print(f"  Description: {model.description}")
            print(f"  Methods: {', '.join(model.supported_generation_methods)}")
            print()
    
    print("="*60)
    print(f"\nTotal models supporting generateContent: {len(generative_models)}")
    print("\nRecommended models to use:")
    for model in generative_models:
        if 'flash' in model.lower():
            print(f"  - {model} (Fast)")
        elif 'pro' in model.lower():
            print(f"  - {model} (Powerful)")
    print("="*60 + "\n")
    
except Exception as e:
    print(f"❌ Error listing models: {e}")
    print("\nTrying alternative method...")
    
    # Alternative: try common model names
    print("\nTesting common model names:")
    test_models = [
        'models/gemini-pro',
        'models/gemini-1.5-flash',
        'models/gemini-1.5-pro',
        'gemini-pro',
        'gemini-1.5-flash',
        'gemini-1.5-pro',
        'gemini-1.5-flash-latest',
        'gemini-1.5-pro-latest'
    ]
    
    for model_name in test_models:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Hi")
            print(f"✓ {model_name} - WORKS")
        except Exception as e:
            print(f"✗ {model_name} - {str(e)[:80]}")