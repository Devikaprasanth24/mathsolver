# Scanner & Problem-Solving Workflow Guide

## 📊 Workflow Architecture

Your math-solve project implements a **7-step intelligent problem-solving pipeline**:

```
[1] Student uploads image
         ↓
[2] Image preprocessing (resize, denoise, normalize, threshold)
         ↓
[3] OCR text extraction (Tesseract/EasyOCR)
         ↓
[4] Text cleaning & parsing (remove noise, convert to valid math expression)
         ↓
[5] Solve math problem (SymPy/AI model)
         ↓
[6] Generate step-by-step solution (human-readable reasoning, breakdown)
         ↓
[7] Interactive display to student (expand/collapse steps, re-try, similar problems)
```

---

## 🏗️ Architecture Layers

### Layer 1: Image Upload & Validation
**File:** `scanner/views.py` → `upload_image_view()`

**Flow:**
```python
1. User uploads image via scanner/upload.html
2. Validate file type (jpg, png, gif, bmp, webp)
3. Validate file size (max 5MB)
4. Validate image integrity (PIL.Image.verify())
5. Create ScannedImage record (status='processing')
6. Proceed to Layer 2
```

**Models:**
- `ScannedImage`: Tracks image, extracted text, validation status, errors

---

### Layer 2: Image Preprocessing
**File:** `math_solver/scanner/preprocessing.py` → `preprocess_image()`

**Pipeline:**
```
Input Image (PIL/Path/NumPy)
    ↓
1. Load as RGB
    ↓
2. Resize to max_width (default 1400px) keeping aspect ratio
    ↓
3. Denoise using fastNlMeansDenoisingColored
    ↓
4. Convert to grayscale
    ↓
5. Normalize contrast (equalization)
    ↓
6. Apply adaptive thresholding (GAUSSIAN_C)
    ↓
Output: PIL Image (high contrast, ready for OCR)
```

**Key Functions:**
- `preprocess_image()`: Main preprocessing pipeline
- `_pil_to_cv()`: Convert PIL Image → OpenCV format
- `_cv_to_pil()`: Convert OpenCV → PIL Image

**Parameters:**
- `max_width`: Resize constraint (default 1400px)
- `denoise`: Enable noise reduction (default True)
- `to_gray`: Convert to grayscale (default True)

---

### Layer 3: OCR Text Extraction
**File:** `math_solver/scanner/ocr.py` → `ocr_from_image()`

**Features:**
```python
# Support for multiple OCR engines
- Tesseract (default, via pytesseract)
- EasyOCR (optional, better for handwriting)

# Parameters:
- image: Path or PIL.Image input
- engine: 'tesseract' or 'easyocr'
- lang: Language code (default 'eng')

# Tesseract config:
- PSM 6: Assumes uniform block of text
- Lang: English (extensible)

# Output: Raw text string
```

**Integration Points:**
- Used by `scanner/views.py` → `upload_image_view()`
- Used by `scanner/views.py` → `process_image_ajax()`
- Used by `math_solver/api/views.py` → `ScanSolveAPIView`

---

### Layer 4: Text Cleaning & Parsing
**File:** `math_solver/scanner/parser.py`

**Pipeline:**

```python
Raw OCR Text (noisy, incomplete)
    ↓
1. clean_ocr_text(): Strip and normalize
    - Replace unicode fractions (½ → 1/2)
    - Normalize operators (× → *, ÷ → /)
    - Normalize hyphens (—, – → -)
    - Handle exponents (^ → **)
    - Remove non-math characters
    - Compress whitespace
    ↓
2. parse_expression(): Convert to SymPy
    - Detect equation vs expression (check for =)
    - If equation: Parse left & right, return Eq(L, R)
    - If expression: Return sympify(text)
    - Raise ValueError if parsing fails
    ↓
Output: SymPy Expr or Eq object
```

**Functions:**
- `clean_ocr_text(text)`: Returns cleaned string
- `parse_expression(text)`: Returns SymPy object or raises ValueError
- `_replace_unicode_fractions(s)`: Helper for fraction normalization

---

### Layer 5: Problem Solving
**Files:** `problems/solver.py`, `problems/ai_solver.py`

#### Option A: SymPy Solver (Deterministic)
**Class:** `MathSolver` in `problems/solver.py`

**Supported Problem Types:**
```python
- Linear equations (ax + b = c)
- Quadratic equations (ax² + bx + c = 0)
- Algebraic simplification
- Factorization
- Derivatives
- Integrals
- Limit calculations
```

**Main Methods:**
- `solve_linear_equation()`: Solve Ax + B = C
- `solve_quadratic_equation()`: Solve ax² + bx + c = 0
- `simplify_expression()`: Simplify algebraic expressions
- `factorize_expression()`: Factor polynomials
- `solve_problem()`: Auto-detect type and solve

**Output Format:**
```python
{
    'solution': value,
    'steps': [
        'Step 1: Move constants to right',
        'Step 2: Divide by coefficient',
        'Step 3: Simplify'
    ],
    'equation_type': 'linear'
}
```

#### Option B: AI Solver (Flexible)
**Class:** `AISolver` in `problems/ai_solver.py`

**Supported Providers:**
- OpenAI (GPT-4)
- Anthropic (Claude 3)

**Flow:**
```
Problem text
    ↓
1. Craft detailed prompt with problem context
    ↓
2. Call AI API with max_tokens=1500
    ↓
3. Parse response (JSON or text)
    ↓
4. Extract:
   - formula
   - steps (array with step_number, hint)
   - final_answer
    ↓
Output: Structured solution dict
```

**Fallback:** Uses `_mock_solution()` if API fails

---

### Layer 6: Generate Step-by-Step Solution
**File:** `problems/solver.py` → `ClueGenerator` class

**Two-Step Process:**

#### Step 6a: Create Clue Objects in Database
**Function:** `generate_clues_for_problem(problem)`

```python
Input: MathProblem object with solution_steps

1. For each step in solution_steps:
   - Create Clue object
   - step_number: Position in sequence
   - clue_text: Guidance (not the answer)
   - formula: Optional formula used
   - is_revealed: False (initially hidden)
   - revealed_at: None

2. Store in database for progressive revealing
```

**Model:** `Clue` in `problems/models.py`
- `problem` (FK to MathProblem)
- `step_number` (unique with problem)
- `clue_text` (the hidden hint)
- `formula` (optional math formula)
- `is_revealed` (boolean)
- `revealed_at` (timestamp)

#### Step 6b: Progressive Clue Revealing
**Function:** `get_next_clue(attempt, problem)`

```
User clicks "Next Hint" button
    ↓
1. Query Clue.objects.filter(is_revealed=False)
    ↓
2. Get first unrevealed clue
    ↓
3. Mark as revealed:
   - is_revealed = True
   - revealed_at = now()
   - attempt.hints_used += 1
    ↓
4. Return to user via AJAX
    ↓
5. Display clue (formula shown optionally)
```

---

### Layer 7: Interactive Display & Learning
**Files:** `templates/problems/solve_new.html`, `templates/problems/solve.html`

**Key Features:**

#### A. Problem Statement Display
```html
<div class="problem-container">
    <h2>{{ problem.extracted_text }}</h2>
    {% if problem.original_image %}
        <img src="{{ problem.original_image.url }}" />
    {% endif %}
</div>
```

#### B. Expandable Clues (Alpine.js)
```html
<div x-data="{ open: false }" class="clue-card">
    <button @click="open = !open">
        Click to reveal clue {{ clue.step_number }}
    </button>
    
    <template x-if="open">
        <div>
            <p>{{ clue.clue_text }}</p>
            {% if clue.formula %}
                <code>{{ clue.formula }}</code>
            {% endif %}
        </div>
    </template>
</div>
```

#### C. Hint Management
```python
# Attempt tracking
- attempts_count: Track solve attempts
- hints_used: Count of revealed clues
- Progress percentage: (revealed_clues / total_clues) * 100
- Points calculation: max(10, 100 - (hints_used * 10))
```

#### D. Answer Submission
```python
User submits answer
    ↓
1. Check answer correctness
2. If correct:
   - Mark attempt as solved
   - Calculate points based on hints
   - Add points to user balance
   - Update user level
3. Redirect to:
   - Success page
   - Similar problems (for practice)
   - Leaderboard
```

#### E. Similar Problems (Re-try Feature)
```python
# Recommendation logic
1. Get problems with same type
2. Get problems with same difficulty
3. Get problems with same category
4. Exclude already solved
5. Return top 3-5 recommendations
```

---

## 🔗 Entry Points (Where Workflow Starts)

### Entry Point 1: Web Upload
```
URL: /scanner/upload/ → POST
Handler: scanner/views.py::upload_image_view()
Flow: Layers 1→2→3→4→5→6→7
Result: Redirect to problems/solve/{problem_id}/
```

### Entry Point 2: AJAX Processing
```
URL: /scanner/process-image-ajax/ → POST (AJAX)
Handler: scanner/views.py::process_image_ajax()
Returns: JSON{success, extracted_text, problem_type, difficulty}
Flow: Layers 1→2→3→4
Result: JSON response (preview before saving)
```

### Entry Point 3: REST API (for mobile/external)
```
URL: /api/scan/ → POST
Handler: math_solver/api/views.py::ScanSolveAPIView
Accepts: image file OR text input
Returns: JSON{expression, cleaned, parsed, steps}
Flow: Layers 2→3→4→5
Result: Complete solve pipeline in single endpoint
```

### Entry Point 4: QR Code Scan
```
User scans QR → Links to /problems/solve/{problem_id}/
Handler: problems/views.py::solve_problem_view()
Flow: Starts at Layer 7 (skips 1-6 if problem already exists)
```

---

## 🗄️ Database Schema

### Core Models

```python
# Represents uploaded image metadata
ScannedImage
├── user (FK User)
├── image_file (ImageField)
├── processed_text (TextField)
├── validation_status (pending|processing|valid|invalid|error)
└── error_message (TextField)

# Represents parsed & solved math problem
MathProblem
├── original_image (ImageField, optional)
├── extracted_text (TextField) ← From Layer 4
├── problem_type (algebra|calculus|geometry|...)
├── difficulty (easy|medium|hard)
├── solution_steps (JSONField) ← From Layer 5
├── final_answer (TextField)
├── created_by (FK User)
└── is_active (Boolean)

# Tracks student's progress on a problem
ProblemAttempt
├── user (FK User)
├── problem (FK MathProblem)
├── attempts_count (Integer)
├── hints_used (Integer)
├── solved (Boolean)
├── started_at (DateTime)
├── completed_at (DateTime)
├── points_earned (Integer)
└── unique_together (user, problem)

# Progressive hints shown to student
Clue
├── problem (FK MathProblem)
├── step_number (Integer)
├── clue_text (TextField) ← Human-readable hint
├── formula (TextField) ← Optional math formula
├── is_revealed (Boolean)
├── revealed_at (DateTime)
└── unique_together (problem, step_number)

# Similar problems for practice
PracticeProblem
├── base_problem (FK MathProblem)
└── similar_problems (M2M MathProblem)

# Student feedback
StudentFeedback
├── user (FK User)
├── problem (FK MathProblem, optional)
├── feedback_type (difficulty|clarity|suggestion|bug|positive)
├── title (CharField)
├── message (TextField)
├── rating (1-5)
├── is_resolved (Boolean)
└── resolution_notes (TextField)
```

---

## 📈 Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│ 1. UPLOAD                                                     │
│    /scanner/upload/ ──POST──> ScannedImage(status='processing')
│                                          │
├──────────────────────────────────────────┤
│ 2. PREPROCESS (Layer 2)                  │
│    Resize + Denoise + Normalize          │
│    PIL Image → Threshold Image           │
│                                          │
├──────────────────────────────────────────┤
│ 3. OCR (Layer 3)                         │
│    Threshold Image → RAW TEXT           │
│                                          │
├──────────────────────────────────────────┤
│ 4. CLEAN & PARSE (Layer 4)              │
│    RAW TEXT → SymPy Expression/Equation  │
│                                          │
├──────────────────────────────────────────┤
│ 5. SOLVE (Layer 5)                      │
│    SymPy/AI → SOLUTION STEPS            │
│                                          │
├──────────────────────────────────────────┤
│ 6. GENERATE CLUES (Layer 6)             │
│    SOLUTION STEPS → Clue objects         │
│    (Hidden, progressively revealed)      │
│                                          │
├──────────────────────────────────────────┤
│ 7. INTERACTIVE DISPLAY (Layer 7)        │
│    Clues + Problem Statement             │
│    + Answer Sheet + Similar Problems     │
│                                          │
└─────────────────────────────────────────────────────────────┘
     │
     └──> User solves → ProblemAttempt(solved=True)
              │
              └──> Points earned & added to user profile
```

---

## 🔧 Implementation Checklist

### ✅ Currently Implemented
- [x] Layer 1: Image upload with validation
- [x] Layer 2: Image preprocessing (OpenCV)
- [x] Layer 3: OCR (Tesseract/EasyOCR)
- [x] Layer 4: Text cleaning & parsing (SymPy)
- [x] Layer 5a: SymPy solver for math problems
- [x] Layer 5b: AI solver (OpenAI, Anthropic)
- [x] Layer 6: Clue generation & progressive revealing
- [x] Layer 7: Interactive solve interface with Alpine.js

### ⚠️ Needs Enhancement
- [ ] Deduplicate views (views.py vs views_enhanced.py)
- [ ] Unify solver implementations (single entry point)
- [ ] Improve similar problems recommendation algorithm
- [ ] Add retry attempts tracking
- [ ] Add problem difficulty auto-calibration
- [ ] Add student feedback loop to problem quality

### 🚀 Future Enhancements
- [ ] Handwriting recognition (for handwritten math)
- [ ] LaTeX equation rendering
- [ ] Multi-language OCR support
- [ ] Real-time collaborative problem solving
- [ ] Explanation quality scoring
- [ ] Difficulty prediction model

---

## 💡 Key Integration Points

### When Scanner Workflow Completes:
1. **MathProblem created** with:
   - extracted_text
   - problem_type (auto-detected)
   - difficulty (auto-estimated)
   - solution_steps (from solver)

2. **Clues generated** with:
   - Progressive hint hierarchy
   - Formula information
   - Initially all hidden (is_revealed=False)

3. **User redirected** to:
   - problems/solve/{problem_id}/
   - Presents Layer 7 interactive interface

4. **Student can**:
   - Read problem statement
   - Request hints one-by-one
   - Submit answer when ready
   - See similar problems for practice
   - Earn points based on hints used

---

## 🎯 Success Metrics

1. **OCR Accuracy**: Clean text extraction rate
2. **Solve Success Rate**: Problems correctly identified and solved
3. **Clue Quality**: Students find hints helpful (via feedback)
4. **Attempt Success**: Percentage of students solving after using hints
5. **Time to Solve**: Average time from hint request to answer submission
6. **User Engagement**: Repeat attempts, similar problems explored

---

## 📚 References & Dependencies

```
Python Packages:
- Pillow (PIL): Image processing
- OpenCV (cv2): Advanced image operations
- pytesseract: OCR engine (requires Tesseract binary)
- easyocr: Alternative OCR (optional)
- sympy: Symbolic mathematics
- requests: HTTP client for AI APIs
- openai: OpenAI API client
- anthropic: Anthropic API client

Django Apps:
- django.contrib.auth: User authentication
- django.contrib.contenttypes: Content framework
- rest_framework: API framework
- django_htmx: HTMX integration
- corsheaders: CORS middleware

Frontend:
- Alpine.js: Interactive UI components
- Tailwind CSS: Styling
- HTMX: Server-driven HTML updates
```

---

## 📞 Support & Debugging

### Common Issues:

**1. OCR Produces Incorrect Text**
- Check image quality (preprocessing may need adjustment)
- Try EasyOCR engine (better for handwriting)
- Verify image is math content (validation layer)

**2. Parsing Fails**
- Enable debug logs: `try: parse_expression() except: log(error)`
- User can manually correct OCR output
- Fall back to text input for QR code scanning

**3. Solver Not Finding Solution**
- Check if problem_type is correctly detected
- Try AI solver if SymPy fails
- Log solution attempts for debugging

**4. Clues Not Appearing**
- Verify ClueGenerator.generate_clues() was called
- Check database for Clue objects created
- Ensure template references correct context variable

---

Generated: 2026-02-08
Version: 1.0
Project: Math-Solve Scanner & Problem-Solving Platform
