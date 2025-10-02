# 🔒 Guía de Seguridad para GitHub

## ⚠️ Información Sensible - NO Subir

### 🚫 Archivos que NUNCA debes subir a GitHub

1. **`.env`** - Contiene tus API keys y tokens
   ```
   ZAI_API_KEY=9ee8a4ca6dfb42e683ccf8ca9a56dcc8...  ← SENSIBLE
   TELEGRAM_BOT_TOKEN=8059773501:AAF_kQRPb7J...    ← SENSIBLE
   TELEGRAM_CHAT_ID=1847600914                     ← SENSIBLE
   ```

2. **`.envsource`** - Configuración local

3. **`agents/*.json`** - Pueden contener información personal en las instrucciones

4. **`venv/`** - Entorno virtual (muy pesado)

5. **`__pycache__/`** - Archivos compilados de Python

### ✅ Ya Protegido

El archivo `.gitignore` ya está configurado para proteger toda esta información.

## 🛡️ Verificar Antes de Subir

### Checklist de Seguridad

```bash
# 1. Verificar que .gitignore existe
cat .gitignore

# 2. Verificar qué archivos se subirán
git status

# 3. Verificar que .env NO aparece
git status | grep .env
# Debe estar vacío o decir "nothing to commit"

# 4. Ver qué archivos están siendo ignorados
git status --ignored
```

### Comandos Seguros

```bash
# Inicializar repositorio
git init

# Agregar archivos (respeta .gitignore)
git add .

# Verificar qué se agregó
git status

# Commit
git commit -m "Initial commit"

# Subir a GitHub
git remote add origin https://github.com/tu-usuario/tu-repo.git
git push -u origin main
```

## 🔍 Qué Pasa Si Ya Subiste Información Sensible

### ⚠️ Si ya subiste .env a GitHub

**URGENTE - Sigue estos pasos:**

1. **Rotar tus credenciales INMEDIATAMENTE**
   - Genera nueva API key en Z.AI
   - Crea nuevo bot de Telegram con @BotFather
   - Actualiza tu `.env` local

2. **Eliminar del historial de Git**
   ```bash
   # Eliminar .env del historial
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch .env" \
     --prune-empty --tag-name-filter cat -- --all
   
   # Forzar push
   git push origin --force --all
   ```

3. **Verificar en GitHub**
   - Ve a tu repositorio en GitHub
   - Verifica que `.env` no aparezca
   - Revisa el historial de commits

## 📋 Archivos Seguros para Subir

### ✅ Estos archivos SÍ puedes subirlos

- ✅ `README.md`
- ✅ `requirements.txt`
- ✅ `.gitignore`
- ✅ `.env.example` (plantilla sin datos reales)
- ✅ `*.py` (código fuente)
- ✅ `Documentos/*.md` (documentación)
- ✅ `demos/*.py` (demos)
- ✅ `agents/.gitkeep` (mantiene carpeta vacía)

### ❌ Estos archivos NO

- ❌ `.env`
- ❌ `.envsource`
- ❌ `agents/*.json` (pueden tener info personal)
- ❌ `venv/`
- ❌ `__pycache__/`

## 🔐 Mejores Prácticas

### 1. Usar Variables de Entorno

```python
import os
from dotenv import load_dotenv

load_dotenv()

# ✅ CORRECTO - Lee de .env
api_key = os.getenv('ZAI_API_KEY')

# ❌ INCORRECTO - Hardcoded
api_key = "9ee8a4ca6dfb42e683ccf8ca9a56dcc8..."
```

### 2. Proporcionar Archivo de Ejemplo

Incluye `.env.example` con valores de ejemplo:

```bash
ZAI_API_KEY=tu_api_key_aqui
TELEGRAM_BOT_TOKEN=tu_bot_token_aqui
```

### 3. Documentar en README

```markdown
## Configuración

1. Copia `.env.example` a `.env`
2. Completa con tus valores reales
3. Nunca subas `.env` a GitHub
```

### 4. Revisar Antes de Commit

```bash
# Siempre revisa qué vas a subir
git diff --staged

# Verifica que no haya API keys
git diff --staged | grep -i "api_key\|token\|password"
```

## 🚨 Señales de Alerta

### ⚠️ Si ves esto en `git status`:

```bash
Changes to be committed:
  modified:   .env          ← ¡PELIGRO!
  modified:   .envsource    ← ¡PELIGRO!
```

**DETENTE** - No hagas commit. Ejecuta:

```bash
git reset HEAD .env
git reset HEAD .envsource
```

## 📝 Plantilla de README para GitHub

```markdown
## 🔑 Configuración

1. Clona el repositorio
2. Copia `.env.example` a `.env`
3. Obtén tu API key de Z.AI: https://z.ai
4. Completa `.env` con tus credenciales
5. **NUNCA** subas `.env` a GitHub

⚠️ El archivo `.env` contiene información sensible y está en `.gitignore`
```

## ✅ Checklist Final Antes de Publicar

- [ ] `.gitignore` existe y está configurado
- [ ] `.env.example` creado (sin datos reales)
- [ ] `.env` NO aparece en `git status`
- [ ] `agents/*.json` NO aparecen en `git status`
- [ ] `venv/` NO aparece en `git status`
- [ ] README incluye instrucciones de configuración
- [ ] No hay API keys hardcoded en el código
- [ ] Probado: `git status` no muestra archivos sensibles

## 🔗 Recursos

- **GitHub Security:** https://docs.github.com/en/code-security
- **Git Secrets:** https://github.com/awslabs/git-secrets
- **Dotenv:** https://github.com/theskumar/python-dotenv

## ⚡ Resumen Rápido

```bash
# ✅ HACER
git add .                    # .gitignore protege archivos sensibles
git commit -m "mensaje"
git push

# ❌ NO HACER
git add .env                 # NUNCA agregues .env
git add agents/*.json        # Pueden tener info personal
```

**Recuerda:** Una vez que subes algo a GitHub, queda en el historial. Es mejor prevenir que tener que limpiar después.
