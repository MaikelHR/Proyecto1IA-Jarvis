// ==========================================
// JARVIS IA - FRONTEND APPLICATION
// ==========================================

// Configuration
const API_BASE_URL = 'http://localhost:8000';

// Global state
const state = {
    currentTab: 'dashboard',
    selectedModel: null,
    modelsData: [],
    isRecording: false,
    mediaRecorder: null,
    audioChunks: [],
    webcamStream: null
};

// ==========================================
// INITIALIZATION
// ==========================================

document.addEventListener('DOMContentLoaded', () => {
    initializeTabs();
    checkAPIStatus();
    loadModels();
    checkVoiceService();
    checkFaceService();
    initializeEventListeners();
});

// ==========================================
// TAB NAVIGATION
// ==========================================

function initializeTabs() {
    const navTabs = document.querySelectorAll('.nav-tab');
    
    navTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const tabName = tab.dataset.tab;
            switchTab(tabName);
        });
    });
}

function switchTab(tabName) {
    // Update nav tabs
    document.querySelectorAll('.nav-tab').forEach(tab => {
        tab.classList.toggle('active', tab.dataset.tab === tabName);
    });
    
    // Update content sections
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.toggle('active', content.id === tabName);
    });
    
    state.currentTab = tabName;
}

// ==========================================
// API STATUS CHECK
// ==========================================

async function checkAPIStatus() {
    const statusIndicator = document.getElementById('apiStatus');
    
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();
        
        if (response.ok) {
            statusIndicator.classList.add('online');
            statusIndicator.querySelector('.status-text').textContent = 'API Conectada';
            
            // Update dashboard stats
            document.getElementById('modelCount').textContent = data.models_loaded || '9';
            document.getElementById('apiVersion').textContent = data.version || 'v1.0';
        } else {
            throw new Error('API not responding');
        }
    } catch (error) {
        console.error('API Status Error:', error);
        statusIndicator.classList.add('offline');
        statusIndicator.querySelector('.status-text').textContent = 'API Desconectada';
        
        showNotification('Error al conectar con el backend. Asegúrate de que el servidor esté corriendo.', 'error');
    }
}

// ==========================================
// ML MODELS
// ==========================================

async function loadModels() {
    const modelsList = document.getElementById('modelsList');
    
    console.log('🔄 Iniciando carga de modelos...');
    console.log('📡 API URL:', `${API_BASE_URL}/predictions/datasets`);
    
    try {
        const response = await fetch(`${API_BASE_URL}/predictions/datasets`);
        console.log('📥 Response status:', response.status);
        console.log('📥 Response ok:', response.ok);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const models = await response.json();
        console.log('✅ Modelos recibidos:', models.length);
        console.log('📊 Datos de modelos:', models);
        console.log('📊 Tipo de datos:', typeof models, Array.isArray(models) ? 'ES ARRAY' : 'NO ES ARRAY');
        
        // Verificar que sea un array
        if (!Array.isArray(models)) {
            console.error('❌ ERROR: La respuesta no es un array');
            throw new Error('La respuesta del API no es un array');
        }
        
        if (models.length === 0) {
            console.warn('⚠️ ADVERTENCIA: El array de modelos está vacío');
            showNotification('No hay modelos disponibles', 'warning');
            return;
        }
        
        state.modelsData = models;
        
        console.log('🗑️ Limpiando lista de modelos...');
        modelsList.innerHTML = '';
        
        console.log('🔨 Creando elementos de modelo...');
        models.forEach((model, index) => {
            console.log(`  ${index + 1}. ${model.name} (${model.key})`);
            
            const modelItem = document.createElement('div');
            modelItem.className = 'model-item';
            modelItem.innerHTML = `
                <h4>${model.name}</h4>
                <p>${model.task}</p>
            `;
            
            modelItem.addEventListener('click', () => selectModel(model));
            modelsList.appendChild(modelItem);
        });
        
        console.log('✅ Elementos de modelo creados:', models.length);
        
        // Auto-select first model
        if (models.length > 0) {
            console.log('🎯 Auto-seleccionando primer modelo:', models[0].name);
            selectModel(models[0]);
        }
    } catch (error) {
        console.error('❌ Error loading models:', error);
        console.error('❌ Error details:', error.message);
        console.error('❌ Error stack:', error.stack);
        modelsList.innerHTML = '<p class="error">Error al cargar modelos</p>';
    }
}

function selectModel(modelOrEvent) {
    // Determinar si recibimos un modelo o un evento
    let model;
    let targetElement = null;
    
    if (modelOrEvent.currentTarget) {
        // Es un evento de click
        targetElement = modelOrEvent.currentTarget;
        // Encontrar el modelo por el índice
        const modelItems = document.querySelectorAll('.model-item');
        const index = Array.from(modelItems).indexOf(targetElement);
        model = state.modelsData[index];
    } else {
        // Es un objeto modelo directo
        model = modelOrEvent;
    }
    
    console.log('🎯 Seleccionando modelo:', model.name);
    state.selectedModel = model;
    
    // Update UI
    document.querySelectorAll('.model-item').forEach(item => {
        item.classList.remove('active');
    });
    
    if (targetElement) {
        targetElement.classList.add('active');
    } else {
        // Si no hay elemento target, activar el primero
        const firstItem = document.querySelector('.model-item');
        if (firstItem) firstItem.classList.add('active');
    }
    
    // Show model info
    displayModelInfo(model);
}

function displayModelInfo(model) {
    const modelInfo = document.getElementById('modelInfo');
    const predictionForm = document.getElementById('predictionForm');
    const predictionResult = document.getElementById('predictionResult');
    
    predictionResult.style.display = 'none';
    
    modelInfo.innerHTML = `
        <h3>${model.name}</h3>
        <p>${model.description}</p>
        
        <div class="model-info-grid">
            <div class="info-badge">
                <strong>Tipo de Tarea</strong>
                <span>${model.task}</span>
            </div>
            <div class="info-badge">
                <strong>Variable Objetivo</strong>
                <span>${model.target}</span>
            </div>
            <div class="info-badge">
                <strong>Dataset</strong>
                <span>${model.key}</span>
            </div>
        </div>
        
        ${model.voice_commands && model.voice_commands.length > 0 ? `
            <div style="margin-top: 1.5rem;">
                <h4>🎤 Comandos de Voz</h4>
                <ul style="list-style: none; padding-left: 0;">
                    ${model.voice_commands.map(cmd => `
                        <li style="padding: 0.5rem; background: var(--bg-tertiary); margin: 0.5rem 0; border-radius: 0.5rem;">
                            "${cmd}"
                        </li>
                    `).join('')}
                </ul>
            </div>
        ` : ''}
    `;
    
    // Show prediction form
    predictionForm.style.display = 'block';
    predictionForm.innerHTML = `
        <h4>📊 Realizar Predicción</h4>
        <p style="color: var(--text-secondary); margin-bottom: 1.5rem;">
            Completa los siguientes campos para obtener una predicción
        </p>
        <div class="form-grid" id="dynamicForm"></div>
        <button class="btn btn-primary btn-large" onclick="makePrediction()">
            <i class="fas fa-chart-line"></i>
            Predecir
        </button>
    `;
    
    // Load example data for the model
    loadExampleForm(model.key);
}

function loadExampleForm(modelKey) {
    const dynamicForm = document.getElementById('dynamicForm');
    
    // Example form fields for each model
    const formFields = {
        'telco_churn': [
            { name: 'gender', type: 'select', label: 'Género', options: ['Male', 'Female'] },
            { name: 'senior_citizen', type: 'number', label: 'Senior Citizen (0/1)', value: 0 },
            { name: 'partner', type: 'select', label: 'Pareja', options: ['Yes', 'No'] },
            { name: 'dependents', type: 'select', label: 'Dependientes', options: ['Yes', 'No'] },
            { name: 'tenure', type: 'number', label: 'Tiempo de servicio (meses)', value: 12 },
            { name: 'phone_service', type: 'select', label: 'Servicio telefónico', options: ['Yes', 'No'] },
            { name: 'multiple_lines', type: 'select', label: 'Múltiples líneas', options: ['Yes', 'No', 'No phone service'] },
            { name: 'internet_service', type: 'select', label: 'Servicio de internet', options: ['DSL', 'Fiber optic', 'No'] },
            { name: 'online_security', type: 'select', label: 'Seguridad online', options: ['Yes', 'No', 'No internet service'] },
            { name: 'online_backup', type: 'select', label: 'Backup online', options: ['Yes', 'No', 'No internet service'] },
            { name: 'device_protection', type: 'select', label: 'Protección de dispositivo', options: ['Yes', 'No', 'No internet service'] },
            { name: 'tech_support', type: 'select', label: 'Soporte técnico', options: ['Yes', 'No', 'No internet service'] },
            { name: 'streaming_t_v', type: 'select', label: 'Streaming TV', options: ['Yes', 'No', 'No internet service'] },
            { name: 'streaming_movies', type: 'select', label: 'Streaming películas', options: ['Yes', 'No', 'No internet service'] },
            { name: 'contract', type: 'select', label: 'Contrato', options: ['Month-to-month', 'One year', 'Two year'] },
            { name: 'paperless_billing', type: 'select', label: 'Facturación sin papel', options: ['Yes', 'No'] },
            { name: 'payment_method', type: 'select', label: 'Método de pago', options: ['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'] },
            { name: 'monthly_charges', type: 'number', label: 'Cargo mensual ($)', value: 70.35, step: 0.01 },
            { name: 'total_charges', type: 'number', label: 'Cargo total ($)', value: 1397.475, step: 0.01 }
        ],
        'wine_quality': [
            { name: 'fixed_acidity', type: 'number', label: 'Acidez fija', value: 7.0, step: 0.1 },
            { name: 'volatile_acidity', type: 'number', label: 'Acidez volátil', value: 0.27, step: 0.01 },
            { name: 'citric_acid', type: 'number', label: 'Ácido cítrico', value: 0.36, step: 0.01 },
            { name: 'residual_sugar', type: 'number', label: 'Azúcar residual', value: 20.7, step: 0.1 },
            { name: 'chlorides', type: 'number', label: 'Cloruros', value: 0.045, step: 0.001 },
            { name: 'free_sulfur_dioxide', type: 'number', label: 'Dióxido de azufre libre', value: 45.0, step: 0.1 },
            { name: 'total_sulfur_dioxide', type: 'number', label: 'Dióxido de azufre total', value: 170.0, step: 0.1 },
            { name: 'density', type: 'number', label: 'Densidad', value: 1.001, step: 0.001 },
            { name: 'p_h', type: 'number', label: 'pH', value: 3.0, step: 0.01 },
            { name: 'sulphates', type: 'number', label: 'Sulfatos', value: 0.45, step: 0.01 },
            { name: 'alcohol', type: 'number', label: 'Alcohol (%)', value: 8.8, step: 0.1 },
            { name: 'type', type: 'select', label: 'Tipo de vino', options: ['white', 'red'] }
        ],
        'bitcoin_price': [
            { name: 'Open', type: 'number', label: 'Precio Apertura ($)', value: 2763.24, step: 0.01 },
            { name: 'High', type: 'number', label: 'Precio Máximo ($)', value: 2889.62, step: 0.01 },
            { name: 'Low', type: 'number', label: 'Precio Mínimo ($)', value: 2720.61, step: 0.01 },
            { name: 'Volume', type: 'text', label: 'Volumen', value: '860,575,000' },
            { name: 'Market Cap', type: 'text', label: 'Market Cap', value: '45,535,800,000' }
        ],
        'body_fat': [
            { name: 'Density', type: 'number', label: 'Densidad corporal', value: 1.0708, step: 0.0001 },
            { name: 'Age', type: 'number', label: 'Edad', value: 23 },
            { name: 'Weight', type: 'number', label: 'Peso (lbs)', value: 154.25, step: 0.01 },
            { name: 'Height', type: 'number', label: 'Altura (inches)', value: 67.75, step: 0.01 },
            { name: 'Neck', type: 'number', label: 'Cuello (cm)', value: 36.2, step: 0.1 },
            { name: 'Chest', type: 'number', label: 'Pecho (cm)', value: 93.1, step: 0.1 },
            { name: 'Abdomen', type: 'number', label: 'Abdomen (cm)', value: 85.2, step: 0.1 },
            { name: 'Hip', type: 'number', label: 'Cadera (cm)', value: 94.5, step: 0.1 },
            { name: 'Thigh', type: 'number', label: 'Muslo (cm)', value: 59.0, step: 0.1 },
            { name: 'Knee', type: 'number', label: 'Rodilla (cm)', value: 37.3, step: 0.1 },
            { name: 'Ankle', type: 'number', label: 'Tobillo (cm)', value: 21.9, step: 0.1 },
            { name: 'Biceps', type: 'number', label: 'Bíceps (cm)', value: 32.0, step: 0.1 },
            { name: 'Forearm', type: 'number', label: 'Antebrazo (cm)', value: 27.4, step: 0.1 },
            { name: 'Wrist', type: 'number', label: 'Muñeca (cm)', value: 17.1, step: 0.1 }
        ],
        'car_prices': [
            { name: 'year', type: 'number', label: 'Año', value: 2015 },
            { name: 'mileage', type: 'number', label: 'Kilometraje', value: 36000 },
            { name: 'state', type: 'text', label: 'Estado', value: 'CA' },
            { name: 'make', type: 'text', label: 'Marca', value: 'Toyota' },
            { name: 'model', type: 'text', label: 'Modelo', value: 'Camry' }
        ],
        'stroke_risk': [
            { name: 'gender', type: 'select', label: 'Género', options: ['Male', 'Female', 'Other'] },
            { name: 'age', type: 'number', label: 'Edad', value: 67 },
            { name: 'hypertension', type: 'select', label: 'Hipertensión', options: ['0', '1'] },
            { name: 'heart_disease', type: 'select', label: 'Enfermedad cardíaca', options: ['0', '1'] },
            { name: 'ever_married', type: 'select', label: 'Casado/a', options: ['Yes', 'No'] },
            { name: 'work_type', type: 'select', label: 'Tipo de trabajo', options: ['Private', 'Self-employed', 'Govt_job', 'children', 'Never_worked'] },
            { name: 'residence_type', type: 'select', label: 'Tipo de residencia', options: ['Urban', 'Rural'] },
            { name: 'avg_glucose_level', type: 'number', label: 'Nivel promedio de glucosa', value: 228.69, step: 0.01 },
            { name: 'bmi', type: 'number', label: 'IMC', value: 36.6, step: 0.1 },
            { name: 'smoking_status', type: 'select', label: 'Estado de fumador', options: ['formerly smoked', 'never smoked', 'smokes', 'Unknown'] }
        ],
        'hepatitis_c': [
            { name: 'age', type: 'number', label: 'Edad', value: 32 },
            { name: 'sex', type: 'select', label: 'Sexo', options: ['m', 'f'] },
            { name: 'alb', type: 'number', label: 'Albumina', value: 38.5, step: 0.1 },
            { name: 'alp', type: 'number', label: 'Fosfatasa alcalina', value: 52.5, step: 0.1 },
            { name: 'alt', type: 'number', label: 'ALT', value: 7.7, step: 0.1 },
            { name: 'ast', type: 'number', label: 'AST', value: 22.1, step: 0.1 },
            { name: 'bil', type: 'number', label: 'Bilirrubina', value: 7.5, step: 0.1 },
            { name: 'che', type: 'number', label: 'Colinesterasa', value: 6.93, step: 0.01 },
            { name: 'chol', type: 'number', label: 'Colesterol', value: 3.23, step: 0.01 },
            { name: 'crea', type: 'number', label: 'Creatinina', value: 106.0, step: 0.1 },
            { name: 'ggt', type: 'number', label: 'GGT', value: 12.1, step: 0.1 },
            { name: 'prot', type: 'number', label: 'Proteína total', value: 69.0, step: 0.1 }
        ],
        'cirrhosis_status': [
            { name: 'n_days', type: 'number', label: 'Días de observación', value: 400 },
            { name: 'status', type: 'select', label: 'Estado', options: ['C', 'CL', 'D'] },
            { name: 'drug', type: 'select', label: 'Medicamento', options: ['D-penicillamine', 'Placebo'] },
            { name: 'age', type: 'number', label: 'Edad (días)', value: 21464 },
            { name: 'sex', type: 'select', label: 'Sexo', options: ['M', 'F'] },
            { name: 'ascites', type: 'select', label: 'Ascitis', options: ['Y', 'N'] },
            { name: 'hepatomegaly', type: 'select', label: 'Hepatomegalia', options: ['Y', 'N'] },
            { name: 'spiders', type: 'select', label: 'Arañas vasculares', options: ['Y', 'N'] },
            { name: 'edema', type: 'select', label: 'Edema', options: ['Y', 'N', 'S'] },
            { name: 'bilirubin', type: 'number', label: 'Bilirrubina', value: 14.5, step: 0.1 },
            { name: 'cholesterol', type: 'number', label: 'Colesterol', value: 261.0, step: 0.1 },
            { name: 'albumin', type: 'number', label: 'Albumina', value: 2.60, step: 0.01 },
            { name: 'copper', type: 'number', label: 'Cobre', value: 156.0, step: 0.1 },
            { name: 'alk_phos', type: 'number', label: 'Fosfatasa alcalina', value: 1718.0, step: 0.1 },
            { name: 'sgot', type: 'number', label: 'SGOT', value: 137.95, step: 0.01 },
            { name: 'tryglicerides', type: 'number', label: 'Triglicéridos', value: 172.0, step: 0.1 },
            { name: 'platelets', type: 'number', label: 'Plaquetas', value: 190.0, step: 0.1 },
            { name: 'prothrombin', type: 'number', label: 'Protrombina', value: 12.2, step: 0.1 },
            { name: 'stage', type: 'number', label: 'Etapa', value: 4.0 }
        ],
        'avocado_prices': [
            { name: 'total_volume', type: 'number', label: 'Volumen total', value: 64236.62, step: 0.01 },
            { name: 'plu_4046', type: 'number', label: 'PLU 4046', value: 1036.74, step: 0.01 },
            { name: 'plu_4225', type: 'number', label: 'PLU 4225', value: 54454.85, step: 0.01 },
            { name: 'plu_4770', type: 'number', label: 'PLU 4770', value: 48.16, step: 0.01 },
            { name: 'total_bags', type: 'number', label: 'Bolsas totales', value: 8696.87, step: 0.01 },
            { name: 'small_bags', type: 'number', label: 'Bolsas pequeñas', value: 8603.62, step: 0.01 },
            { name: 'large_bags', type: 'number', label: 'Bolsas grandes', value: 93.25, step: 0.01 },
            { name: 'x_large_bags', type: 'number', label: 'Bolsas extragrandes', value: 0.0, step: 0.01 },
            { name: 'type', type: 'select', label: 'Tipo', options: ['conventional', 'organic'] },
            { name: 'year', type: 'number', label: 'Año', value: 2015 },
            { name: 'region', type: 'text', label: 'Región', value: 'Albany' }
        ]
    };
    
    const fields = formFields[modelKey] || [];
    
    if (fields.length === 0) {
        dynamicForm.innerHTML = '<p style="color: var(--text-muted);">Formulario no disponible para este modelo</p>';
        return;
    }
    
    dynamicForm.innerHTML = fields.map(field => {
        if (field.type === 'select') {
            return `
                <div class="form-group">
                    <label for="${field.name}">${field.label}</label>
                    <select id="${field.name}" name="${field.name}">
                        ${field.options.map(opt => `<option value="${opt}">${opt}</option>`).join('')}
                    </select>
                </div>
            `;
        } else {
            return `
                <div class="form-group">
                    <label for="${field.name}">${field.label}</label>
                    <input 
                        type="${field.type}" 
                        id="${field.name}" 
                        name="${field.name}" 
                        value="${field.value || ''}"
                        step="${field.step || 'any'}"
                        required
                    >
                </div>
            `;
        }
    }).join('');
}

async function makePrediction() {
    if (!state.selectedModel) {
        showNotification('Selecciona un modelo primero', 'error');
        return;
    }
    
    // Gather form data
    const formData = {};
    const inputs = document.querySelectorAll('#dynamicForm input, #dynamicForm select');
    
    inputs.forEach(input => {
        const value = input.value;
        formData[input.name] = isNaN(value) ? value : parseFloat(value);
    });
    
    console.log('📤 Sending prediction request:', {
        model: state.selectedModel.key,
        features: formData
    });
    console.log('📤 Request body:', JSON.stringify({ features: formData }, null, 2));
    
    try {
        const response = await fetch(`${API_BASE_URL}/predictions/${state.selectedModel.key}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ features: formData })
        });
        
        console.log('📥 Response status:', response.status);
        const result = await response.json();
        console.log('📥 Response data:', result);
        
        if (response.ok) {
            displayPredictionResult(result);
        } else {
            console.error('❌ Error from API:', result);
            const errorMsg = result.detail?.message || result.detail || result.message || 'Error desconocido';
            showNotification(`Error: ${errorMsg}`, 'error');
        }
    } catch (error) {
        console.error('Prediction error:', error);
        showNotification('Error al realizar la predicción', 'error');
    }
}

function displayPredictionResult(result) {
    const resultDiv = document.getElementById('predictionResult');
    
    resultDiv.style.display = 'block';
    resultDiv.innerHTML = `
        <div class="result-header">
            <i class="fas fa-check-circle"></i>
            <h3>Resultado de la Predicción</h3>
        </div>
        
        <div>
            <strong>Modelo:</strong> ${result.dataset}
        </div>
        
        <div class="result-value">
            ${formatPredictionValue(result.prediction, result.task_type)}
        </div>
        
        ${result.confidence ? `
            <div>
                <strong>Confianza:</strong>
                <div class="confidence-bar">
                    <div class="confidence-fill" style="width: ${result.confidence * 100}%">
                        ${(result.confidence * 100).toFixed(1)}%
                    </div>
                </div>
            </div>
        ` : ''}
        
        <div style="margin-top: 1rem; color: var(--text-secondary);">
            <strong>Tipo de tarea:</strong> ${result.task_type}
        </div>
    `;
    
    // Scroll to result
    resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function formatPredictionValue(value, taskType) {
    if (taskType === 'regression') {
        return `$${parseFloat(value).toFixed(2)}`;
    }
    return value;
}

// ==========================================
// VOICE COMMANDS
// ==========================================

function initializeEventListeners() {
    // Voice
    document.getElementById('recordBtn')?.addEventListener('click', startRecording);
    document.getElementById('stopBtn')?.addEventListener('click', stopRecording);
    
    // Face
    document.getElementById('startCameraBtn')?.addEventListener('click', startCamera);
    document.getElementById('stopCameraBtn')?.addEventListener('click', stopCamera);
    document.getElementById('captureBtn')?.addEventListener('click', capturePhoto);
    document.getElementById('fileInput')?.addEventListener('change', handleFileUpload);
}

async function checkVoiceService() {
    try {
        const response = await fetch(`${API_BASE_URL}/voice/status`);
        const data = await response.json();
        
        const statusEl = document.getElementById('voiceServiceStatus');
        const dashboardStatus = document.getElementById('voiceStatus');
        
        if (data.available) {
            statusEl.innerHTML = '<span class="status-badge online">✓ Disponible</span>';
            dashboardStatus.textContent = '✓ Activo';
        } else {
            statusEl.innerHTML = '<span class="status-badge offline">✗ No configurado</span>';
            dashboardStatus.textContent = '✗ No config.';
        }
    } catch (error) {
        console.error('Voice service check error:', error);
    }
}

async function startRecording() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        
        state.mediaRecorder = new MediaRecorder(stream);
        state.audioChunks = [];
        
        state.mediaRecorder.ondataavailable = (event) => {
            state.audioChunks.push(event.data);
        };
        
        state.mediaRecorder.onstop = processAudio;
        
        state.mediaRecorder.start();
        state.isRecording = true;
        
        // Update UI
        document.getElementById('recordBtn').style.display = 'none';
        document.getElementById('stopBtn').style.display = 'inline-flex';
        document.getElementById('voiceVisualizer').classList.add('recording');
        document.getElementById('voiceStatusPanel').innerHTML = `
            <p class="info-text" style="color: var(--danger-color);">
                <i class="fas fa-record-vinyl"></i>
                Grabando... Di tu comando ahora
            </p>
        `;
        
    } catch (error) {
        console.error('Error starting recording:', error);
        showNotification('Error al acceder al micrófono', 'error');
    }
}

function stopRecording() {
    if (state.mediaRecorder && state.isRecording) {
        state.mediaRecorder.stop();
        state.mediaRecorder.stream.getTracks().forEach(track => track.stop());
        state.isRecording = false;
        
        // Update UI
        document.getElementById('recordBtn').style.display = 'inline-flex';
        document.getElementById('stopBtn').style.display = 'none';
        document.getElementById('voiceVisualizer').classList.remove('recording');
        document.getElementById('voiceStatusPanel').innerHTML = `
            <p class="info-text">
                <i class="fas fa-spinner fa-spin"></i>
                Procesando audio...
            </p>
        `;
    }
}

async function processAudio() {
    const audioBlob = new Blob(state.audioChunks, { type: 'audio/webm' });
    
    // Convert to base64
    const reader = new FileReader();
    reader.readAsDataURL(audioBlob);
    
    reader.onloadend = async () => {
        const base64Audio = reader.result.split(',')[1];
        
        try {
            const response = await fetch(`${API_BASE_URL}/voice/command`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    audio_base64: base64Audio,
                    language_code: 'es-ES'
                })
            });
            
            const result = await response.json();
            
            displayVoiceResult(result);
        } catch (error) {
            console.error('Voice processing error:', error);
            showNotification('Error al procesar el audio. Verifica que Google Speech-to-Text esté configurado.', 'error');
            resetVoiceUI();
        }
    };
}

function displayVoiceResult(result) {
    const transcriptBox = document.getElementById('transcriptBox');
    const transcriptText = document.getElementById('transcriptText');
    const commandRecognized = document.getElementById('commandRecognized');
    const detectedModel = document.getElementById('detectedModel');
    
    transcriptBox.style.display = 'block';
    transcriptText.textContent = result.transcript;
    
    if (result.command_recognized && result.dataset_key) {
        commandRecognized.style.display = 'block';
        detectedModel.textContent = result.dataset_key;
        
        showNotification('¡Comando reconocido! Puedes ir a la sección de Modelos ML para ejecutarlo.', 'success');
    } else {
        commandRecognized.style.display = 'none';
        showNotification('Comando no reconocido. Intenta de nuevo con un comando válido.', 'warning');
    }
    
    resetVoiceUI();
}

function resetVoiceUI() {
    document.getElementById('voiceStatusPanel').innerHTML = `
        <p class="info-text">
            <i class="fas fa-info-circle"></i>
            Presiona "Iniciar Grabación" y di un comando
        </p>
    `;
}

// ==========================================
// FACE RECOGNITION
// ==========================================

async function checkFaceService() {
    try {
        const response = await fetch(`${API_BASE_URL}/face/status`);
        const data = await response.json();
        
        const statusEl = document.getElementById('faceServiceStatus');
        const dashboardStatus = document.getElementById('faceStatus');
        
        if (data.available) {
            statusEl.innerHTML = '<span class="status-badge online">✓ Disponible</span>';
            dashboardStatus.textContent = '✓ Activo';
        } else {
            statusEl.innerHTML = '<span class="status-badge offline">✗ No configurado</span>';
            dashboardStatus.textContent = '✗ No config.';
        }
    } catch (error) {
        console.error('Face service check error:', error);
    }
}

async function startCamera() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ 
            video: { facingMode: 'user' } 
        });
        
        const video = document.getElementById('webcam');
        video.srcObject = stream;
        state.webcamStream = stream;
        
        // Update UI
        document.getElementById('startCameraBtn').style.display = 'none';
        document.getElementById('captureBtn').style.display = 'inline-flex';
        document.getElementById('stopCameraBtn').style.display = 'inline-flex';
        
    } catch (error) {
        console.error('Error starting camera:', error);
        showNotification('Error al acceder a la cámara', 'error');
    }
}

function stopCamera() {
    if (state.webcamStream) {
        state.webcamStream.getTracks().forEach(track => track.stop());
        state.webcamStream = null;
        
        const video = document.getElementById('webcam');
        video.srcObject = null;
        
        // Update UI
        document.getElementById('startCameraBtn').style.display = 'inline-flex';
        document.getElementById('captureBtn').style.display = 'none';
        document.getElementById('stopCameraBtn').style.display = 'none';
    }
}

async function capturePhoto() {
    const video = document.getElementById('webcam');
    const canvas = document.getElementById('canvas');
    
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0);
    
    canvas.toBlob(async (blob) => {
        await analyzeEmotion(blob);
    }, 'image/jpeg');
}

async function handleFileUpload(event) {
    const file = event.target.files[0];
    if (file) {
        await analyzeEmotion(file);
    }
}

async function analyzeEmotion(imageBlob) {
    const formData = new FormData();
    formData.append('file', imageBlob);
    
    showNotification('Analizando emociones...', 'info');
    
    try {
        const response = await fetch(`${API_BASE_URL}/face/emotion/upload`, {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (response.ok) {
            displayEmotionResult(result, imageBlob);
        } else {
            showNotification(`Error: ${result.detail}`, 'error');
        }
    } catch (error) {
        console.error('Emotion analysis error:', error);
        showNotification('Error al analizar emociones', 'error');
    }
}

function displayEmotionResult(result, imageBlob) {
    document.getElementById('emotionPlaceholder').style.display = 'none';
    document.getElementById('emotionResults').style.display = 'block';
    
    // Show captured image
    const img = document.getElementById('capturedImage');
    img.src = URL.createObjectURL(imageBlob);
    
    // Display dominant emotion
    const emotionIcons = {
        'felicidad': 'fa-smile-beam',
        'tristeza': 'fa-sad-tear',
        'enojo': 'fa-angry',
        'sorpresa': 'fa-surprise',
        'miedo': 'fa-flushed',
        'disgusto': 'fa-grimace',
        'neutral': 'fa-meh',
        'desprecio': 'fa-meh-rolling-eyes'
    };
    
    const dominantEmotion = result.dominant_emotion_es || result.dominant_emotion;
    const iconClass = emotionIcons[dominantEmotion?.toLowerCase()] || 'fa-smile';
    
    document.getElementById('dominantEmotion').innerHTML = `
        <i class="fas ${iconClass}"></i>
        <span>${dominantEmotion}</span>
    `;
    document.getElementById('emotionConfidence').textContent = `${(result.confidence * 100).toFixed(1)}%`;
    document.getElementById('faceCount').textContent = result.num_faces;
    
    // Display emotion bars
    const emotionsBar = document.getElementById('emotionsBar');
    const emotions = result.emotions_es || result.emotions;
    
    emotionsBar.innerHTML = Object.entries(emotions)
        .sort((a, b) => b[1] - a[1])
        .map(([emotion, value]) => `
            <div class="emotion-bar">
                <div class="emotion-bar-label">
                    <span>${emotion}</span>
                    <span>${(value * 100).toFixed(1)}%</span>
                </div>
                <div class="emotion-bar-fill-container">
                    <div class="emotion-bar-fill" style="width: ${value * 100}%">
                        ${(value * 100).toFixed(0)}%
                    </div>
                </div>
            </div>
        `).join('');
    
    showNotification('¡Análisis completado exitosamente!', 'success');
}

// ==========================================
// UTILITIES
// ==========================================

function showNotification(message, type = 'info') {
    // Simple console notification for now
    // You can implement a toast/notification system here
    console.log(`[${type.toUpperCase()}]`, message);
    
    const colors = {
        'success': '#10b981',
        'error': '#ef4444',
        'warning': '#f59e0b',
        'info': '#06b6d4'
    };
    
    console.log(`%c${message}`, `color: ${colors[type]}; font-weight: bold;`);
}
