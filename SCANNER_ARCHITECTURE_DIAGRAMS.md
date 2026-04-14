# Scanner Architecture: Visual Reference & Diagrams

## 🎯 System Overview Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                        MATH-SOLVE SYSTEM                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌──────────────━┐         ┌─────────────────────┐                 │
│  │   User        │         │   Problem Browser    │                 │
│  │   Uploads     │────────>│   (Practice View)    │                 │
│  │   Image       │         │   (Leaderboard)      │                 │
│  └——────────────┘         └─────────────────────┘                 │
│         │                                                             │
│         ↓                                                             │
│  ┌━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓         │
│  ┃          SCANNER WORKFLOW (7 LAYERS)                    ┃         │
│  ┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫         │
│  ┃                                                         ┃         │
│  ┃  ┌────────────────────────────────────────────────┐   ┃         │
│  ┃  │ 1. UPLOAD & VALIDATE                           │   ┃         │
│  ┃  │    scanner/views.py::upload_image_view()       │   ┃         │
│  ┃  │    → ScannedImage model created                │   ┃         │
│  ┃  │    → Validate: type, size, integrity           │   ┃         │
│  ┃  └────────────────────┬─────────────────────────┘   ┃         │
│  ┃                       ↓                              ┃         │
│  ┃  ┌────────────────────────────────────────────────┐   ┃         │
│  ┃  │ 2. PREPROCESS                                   │   ┃         │
│  ┃  │    math_solver/scanner/preprocessing.py        │   ┃         │
│  ┃  │    → Resize to max_width (1400px)              │   ┃         │
│  ┃  │    → Denoise (fastNlMeansDenoising)           │   ┃         │
│  ┃  │    → Normalize contrast (equalization)        │   ┃         │
│  ┃  │    → Adaptive thresholding                    │   ┃         │
│  ┃  │    OUTPUT: High-contrast PIL Image            │   ┃         │
│  ┃  └────────────────────┬─────────────────────────┘   ┃         │
│  ┃                       ↓                              ┃         │
│  ┃  ┌────────────────────────────────────────────────┐   ┃         │
│  ┃  │ 3. OCR                                          │   ┃         │
│  ┃  │    math_solver/scanner/ocr.py                  │   ┃         │
│  ┃  │    → Engine: Tesseract (default)               │   ┃         │
│  ┃  │    → Alt: EasyOCR (better handwriting)         │   ┃         │
│  ┃  │    OUTPUT: Raw text string                     │   ┃         │
│  ┃  └────────────────────┬─────────────────────────┘   ┃         │
│  ┃                       ↓                              ┃         │
│  ┃  ┌────────────────────────────────────────────────┐   ┃         │
│  ┃  │ 4. CLEAN & PARSE                                │   ┃         │
│  ┃  │    math_solver/scanner/parser.py               │   ┃         │
│  ┃  │    → clean_ocr_text(): normalize, remove noise │   ┃         │
│  ┃  │    → parse_expression(): convert to SymPy      │   ┃         │
│  ┃  │    OUTPUT: SymPy Expr or Eq object             │   ┃         │
│  ┃  └────────────────────┬─────────────────────────┘   ┃         │
│  ┃                       ↓                              ┃         │
│  ┃  ┌────────────────────────────────────────────────┐   ┃         │
│  ┃  │ 5. SOLVE                                        │   ┃         │
│  ┃  │    problems/solver.py (MathSolver) or          │   ┃         │
│  ┃  │    problems/ai_solver.py (AISolver)            │   ┃         │
│  ┃  │                                                 │   ┃         │
│  ┃  │    SymPy: Linear, quadratic, derivatives       │   ┃         │
│  ┃  │    AI: OpenAI GPT-4 or Anthropic Claude        │   ┃         │
│  ┃  │    OUTPUT: MathProblem created                 │   ┃         │
│  ┃  │    {solution, steps, equation_type}            │   ┃         │
│  ┃  └────────────────────┬─────────────────────────┘   ┃         │
│  ┃                       ↓                              ┃         │
│  ┃  ┌────────────────────────────────────────────────┐   ┃         │
│  ┃  │ 6. GENERATE CLUES (Progressive Hints)          │   ┃         │
│  ┃  │    problems/models.py::Clue                    │   ┃         │
│  ┃  │    → Create Clue objects from solution_steps   │   ┃         │
│  ┃  │    → Initially all hidden (is_revealed=False)  │   ┃         │
│  ┃  │    → Each clue is a hint, NOT the answer       │   ┃         │
│  ┃  │    OUTPUT: Clue objects in database            │   ┃         │
│  ┃  └────────────────────┬─────────────────────────┘   ┃         │
│  ┃                       ↓                              ┃         │
│  ┃  ┌────────────────────────────────────────────────┐   ┃         │
│  ┃  │ 7. INTERACTIVE DISPLAY                          │   ┃         │
│  ┃  │    templates/problems/solve_new.html           │   ┃         │
│  ┃  │    problems/views.py::solve_problem_view()     │   ┃         │
│  ┃  │                                                 │   ┃         │
│  ┃  │    → Show problem statement                    │   ┃         │
│  ┃  │    → Show original image (if scanned)          │   ┃         │
│  ┃  │    → Allow "Next Hint" button clicks           │   ┃         │
│  ┃  │    → Track: attempts, hints_used, points       │   ┃         │
│  ┃  │    → Submit answer                             │   ┃         │
│  ┃  │    → Show similar problems for practice        │   ┃         │
│  ┃  │    OUTPUT: Learning experience                 │   ┃         │
│  ┃  └────────────────────────────────────────────────┘   ┃         │
│  ┃                                                         ┃         │
│  └━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛         │
│         ↓                                                             │
│  ┌─────────────────────────────────────────────────┐               │
│  │   User Solves Problem                           │               │
│  │   → ProblemAttempt.solved = True                │               │
│  │   → Points earned = 100 - (10 * hints_used)     │               │
│  │   → User level increases                        │               │
│  └─────────────────────────────────────────────────┘               │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow Through Layers

```
USER INPUT (JPG)
    ↓
[Layer 1] Upload
    ↓
ScannedImage {
    image_file: <JPG>,
    validation_status: 'processing',
    processed_text: null
}
    ↓
[Layer 2] Preprocess
    ↓
PIL Image {
    Mode: 1-bit (threshold)
    High contrast, no noise
}
    ↓
[Layer 3] OCR
    ↓
Raw text: "2x+3=7" (might have errors)
    ↓
[Layer 4] Clean & Parse
    ↓
Cleaned: "2x + 3 = 7"
SymPy: Eq(2*x + 3, 7)
    ↓
[Layer 5] Solve
    ↓
MathProblem {
    extracted_text: "2x + 3 = 7",
    problem_type: 'algebra',
    difficulty: 'easy',
    solution_steps: [{
        'step': 'Move 3 to right',
        'hint': 'Subtract 3 from both sides',
        'formula': '2x = 4'
    }, {...}],
    final_answer: '2'
}
    ↓
[Layer 6] Generate Clues
    ↓
Clue objects (auto-created):
    Clue{step_number: 1, clue_text: "Move constant...", is_revealed: False}
    Clue{step_number: 2, clue_text: "Divide by coefficient...", is_revealed: False}
    Clue{step_number: 3, clue_text: "Write solution...", is_revealed: False}
    ↓
[Layer 7] Display
    ↓
HTML Render:
    Problem: "Solve: 2x + 3 = 7"
    Image: <original scan>
    Clue 1: [Locked]
    Clue 2: [Locked]
    Clue 3: [Locked]
    Button: "Next Hint"
    ↓
User clicks "Next Hint"
    ↓
Clue 1 revealed:
    Clue 1: "Move constant to right side" [Revealed]
    Clue 2: [Locked]
    Clue 3: [Locked]
    ↓
User submits: "x = 2"
    ↓
ProblemAttempt {
    solved: True,
    attempts_count: 2,
    hints_used: 1,
    points_earned: 90 (100 - 10*1),
    completed_at: now()
}
```

---

## 📦 Entry Points & Workflows

### Entry Point 1: Web Upload

```
Browser → GET /scanner/upload/
   ↓
Display upload.html (drag-drop UI)
   ↓
User drops image
   ↓
Browser → POST /scanner/upload/
          + image file
   ↓
scanner/views.py::upload_image_view()
   ├─ Layer 1: Create ScannedImage
   ├─ Layer 2: Preprocess
   ├─ Layer 3: OCR
   ├─ Layer 4: Parse
   ├─ Layer 5: Solve
   ├─ Layer 6: Auto-create Clues
   └─ Layer 7: Redirect to solve page
   ↓
Redirect to /problems/solve/123/
   ↓
Display solve_new.html with interactive interface
```

### Entry Point 2: AJAX Preview

```
User uploads in frontend
   ↓
JavaScript → POST /scanner/process-image-ajax/
             + image file
   ↓
scanner/views.py::process_image_ajax()
   ├─ Layer 2: Preprocess
   ├─ Layer 3: OCR
   └─ Layer 4: Parse (STOP)
   ↓
Return JSON {
    extracted_text: "2x + 3 = 7",
    problem_type: 'algebra',
    difficulty: 'easy'
}
   ↓
JavaScript shows preview:
    "Found: Algebra problem (Easy)"
    "Text: 2x + 3 = 7"
    [Confirm] [Re-scan]
   ↓
User clicks [Confirm]
   ↓
Continue to Layer 5 (solve) via another request
```

### Entry Point 3: REST API

```
External app/mobile → POST /api/scan/
                      {image: <file>} OR
                      {text: "2x + 3 = 7"}
   ↓
math_solver/api/views.py::ScanSolveAPIView
   ├─ If image: Layer 2→3→4
   ├─ If text: Go straight to Layer 4
   ├─ Layer 5: Solve
   └─ Return JSON response immediately
   ↓
Return JSON {
    success: True,
    expression: "2x + 3 = 7",
    cleaned: "2x + 3 = 7",
    parsed: "Eq(2*x + 3, 7)",
    steps: [...],
    solver_used: 'sympy'
}
```

### Entry Point 4: QR Code

```
User scans QR code
   → Links to /problems/solve/123/
   ↓
problems/views.py::solve_problem_view()
   ├─ Fetch MathProblem from database
   ├─ Get or create ProblemAttempt
   ├─ Fetch Clues
   └─ Render solve_new.html
   ↓
(Assumes problem already exists from layers 1-6)
```

---

## 🗄️ Database Schema Diagram

```
                    ┌─────────────────────┐
                    │   django.auth.User  │
                    ├─────────────────────┤
                    │ id (PK)             │
                    │ username            │
                    │ email               │
                    │ first_name          │
                    │ last_name           │
                    │ is_superuser        │
                    │ is_staff            │
                    │ points              │
                    │ level               │
                    └──────────┬──────────┘
                               │
                ┌──────────────┼──────────────┐
                │              │              │
                ↓              ↓              ↓
    ┌─────────────────┐ ┌──────────────┐ ┌────────────────┐
    │ ScannedImage    │ │ MathProblem  │ │ ProblemAttempt │
    ├─────────────────┤ ├──────────────┤ ├────────────────┤
    │ id              │ │ id           │ │ id             │
    │ user_id (FK)    │ │ user_id (FK) │ │ user_id (FK)   │
    │ image_file      │ │ extracted... │ │ problem_id(FK) │
    │ processed_text  │ │ problem_type │ │ attempts_count │
    │ validation...   │ │ difficulty   │ │ hints_used     │
    │ error_message   │ │ solution...  │ │ solved         │
    │ created_at      │ │ final_answer │ │ started_at     │
    │ updated_at      │ │ created_at   │ │ completed_at   │
    │                 │ │ is_active    │ │ points_earned  │
    └─────────────────┘ └──────┬───────┘ └────────────────┘
                                │
                                │ (1:N)
                                ↓
                        ┌──────────────────┐
                        │      Clue        │
                        ├──────────────────┤
                        │ id               │
                        │ problem_id (FK)  │
                        │ step_number      │
                        │ clue_text        │
                        │ formula          │
                        │ is_revealed      │
                        │ revealed_at      │
                        └──────────────────┘
```

---

## 🔗 View/Model/Template Connections

```
VIEWS → MODELS → TEMPLATES

[scanner/views.py]
    ↓
upload_image_view()
    ├─ Creates: ScannedImage
    ├─ Creates: MathProblem
    └─ Renders: scanner/upload.html
    
process_image_ajax()
    ├─ Reads: ScannedImage
    └─ Returns: JSON

[problems/views.py]
    ↓
solve_problem_view()
    ├─ Reads: MathProblem
    ├─ Reads/Creates: ProblemAttempt
    ├─ Reads: Clue
    ├─ Renders: problems/solve_new.html
    └─ Context: {
        problem,
        attempt,
        clues,
        similar_problems,
        user_problems_solved
    }

practice_view()
    ├─ Reads: MathProblem (filtered)
    ├─ Reads: ProblemAttempt
    └─ Renders: problems/practice.html

leaderboard_view()
    ├─ Reads: User (sorted by points)
    ├─ Reads: ProblemAttempt (for stats)
    └─ Renders: problems/leaderboard.html
```

---

## ⚙️ Function Call Sequence Diagram

```
upload_image_view() ─────────────────────────────────────────────────────┐
│                                                                          │
│  validate_file_type()                                                   │
│  validate_file_size()                                                   │
│  validate_image_integrity() ─ PIL.Image.open().verify()                 │
│  │                                                                       │
│  ScannedImage.objects.create()                                          │
│  │                                                                       │
│  preprocess_image() ─ [Layer 2]                                         │
│      ├─ PIL.Image.open()                                                │
│      ├─ resize()                                                        │
│      ├─ cv2.fastNlMeansDenoisingColored()                              │
│      ├─ cv2.cvtColor(..., cv2.COLOR_BGR2GRAY)                          │
│      ├─ cv2.equalizeHist()                                             │
│      └─ cv2.adaptiveThreshold()                                        │
│  │                                                                       │
│  extract_text_from_image() ─ [Layer 3]                                 │
│      └─ ocr_from_image()                                                │
│          └─ pytesseract.image_to_string() OR easyocr.Reader().readtext()
│  │                                                                       │
│  validate_math_content()                                                │
│  │                                                                       │
│  detect_problem_type()                                                  │
│  estimate_difficulty()                                                  │
│  │                                                                       │
│  clean_ocr_text() ─ [Layer 4]                                           │
│      └─ _replace_unicode_fractions()                                    │
│  │                                                                       │
│  parse_expression() ─ [Layer 4]                                         │
│      └─ sympify()                                                       │
│  │                                                                       │
│  SolverManager.solve_problem() ─ [Layer 5]                             │
│      ├─ MathSolver.solve_problem()                                     │
│      │   ├─ solve_linear_equation()                                    │
│      │   ├─ solve_quadratic_equation()                                 │
│      │   └─ sympify() / solve()                                        │
│      └─ AISolver.solve() (if fallback needed)                          │
│  │                                                                       │
│  MathProblem.objects.create()                                           │
│      └─ MathProblem.save() ─ TRIGGER [Layer 6]                         │
│          └─ generate_clues_from_solution()                             │
│              └─ Clue.objects.create() (for each step)                  │
│  │                                                                       │
└─ redirect('problems:solve', problem_id=math_problem.id)                │
   │                                                                      │
   → solve_problem_view() [Layer 7]                                      │
       └─ render('problems/solve_new.html', context)                     │
```

---

## 🎯 Problem Type Detection Flow

```
extract_text  "2x^2 + 3x + 1 = 0"
    ↓
detect_problem_type()
    ├─ Check keywords:
    │  ├─ Contains "sin|cos|tan|angle|degree" → trigonometry
    │  ├─ Contains "derivative|integral|limit|slope" → calculus
    │  ├─ Contains "triangle|circle|square|angle" → geometry
    │  ├─ Contains "solve|x^2|quadratic|parabola" → algebra
    │  └─ Default → arithmetic
    ↓
Result: 'algebra'
    ↓
estimate_difficulty(text, problem_type)
    ├─ Check length of equation
    ├─ Count of operators
    ├─ Presence of advanced functions
    ↓
Result: 'medium' or 'hard'
```

---

## 🎓 Information Flow: Upload to Learn

```
UPLOAD PHASE
─────────────
1. Student scans/uploads image
   ↓
2. Image validated (file type, size, integrity)
   ↓
3. Image preprocessed (denoise, threshold)
   ↓
4. OCR extracts text
   ↓
5. Text cleaned and parsed to SymPy expression
   ↓
6. Problem type and difficulty detected
   ↓
7. Problem solved using SymPy or AI
   ↓
STORED: MathProblem, ScannedImage


LEARNING PHASE
──────────────
1. Problem displayed to student
   ↓
2. Clues generated and displayed (hidden)
   ↓
3. Student clicks "Next Hint"
   ↓
4. One clue revealed (progress tracked)
   ↓
5. Student tries to solve
   ↓
6. Student submits answer
   ↓
7. Answer checked for correctness
   ↓
8. If correct:
   - Mark attempt as solved
   - Calculate points (100 - 10*hints)
   - Add to user score
   - Suggest similar problems for practice
   - Update leaderboard
   ↓
LEARNED: Student developed problem-solving skills
EARNED: Points, level, achievement badges
```

---

## 🚀 Optimization Opportunities (Architecture)

```
Current Architecture
────────────────────
Views (100+ lines)
    ├─ Contains layer logic 1-7
    ├─ Handles errors inconsistently
    └─ Hard to test/reuse


Proposed Architecture
─────────────────────
UploadWorkflow (orchestrator)
    ├─ Layer 1: _create_record()
    ├─ Layer 2: _preprocess()
    ├─ Layer 3: _extract_text()
    ├─ Layer 4: _clean_and_parse()
    └─ Layer 5: _solve()
         └─ Uses SolverManager
         
SolverManager (unified solver)
    ├─ Try SymPy first
    └─ Fall back to AI

View (20 lines)
    └─ Just calls UploadWorkflow

Benefits:
- 80% code reduction in views
- Single reusable workflow
- Better error handling
- Easier testing
- Same logic everywhere (web, API, AJAX)
```

---

## 📊 Performance Considerations

```
Layer        | Time Cost    | Bottleneck              | Optimization
─────────────┼──────────────┼────────────────────────┼──────────────
1. Upload    | 0.1s         | Network                | Compression
2. Preprocess| 2-3s         | Image size              | Resize first
3. OCR       | 3-5s         | Tesseract/EasyOCR      | Use Tesseract
4. Parse     | 0.1s         | Regex                  | -
5. Solve     | 0.5-2s       | SymPy (slow for hard)  | Use AI for complex
6. Clues     | 0.1s         | Database                | Batch insert
7. Display   | 0.2s         | Rendering              | Cache

Total: 6-12 seconds end-to-end

Optimization: Async processing
- Layers 1-4: Do in view (quick)
- Layers 5-6: Offload to Celery task (show "Processing...")
- Layer 7: Show as soon as MathProblem created
```

---

## 🔒 Security Checkpoints

```
Layer 1: UPLOAD
  ├─ File extension whitelist
  ├─ File size limit (5MB)
  ├─ MIME type validation
  └─ PIL integrity check
     
Layer 2: PREPROCESS
  ├─ Memory limits for large images
  └─ Timeout protection

Layer 3: OCR
  ├─ Tesseract sandbox
  └─ Output length limits

Layer 4: PARSE
  ├─ SymPy sandbox
  └─ Expression size limits

Layer 5: SOLVE
  ├─ API key rotation (for AI)
  ├─ Rate limiting
  └─ Cost monitoring (AI calls)

Layer 6-7: DISPLAY
  ├─ XSS protection (escape clue_text)
  └─ CSRF tokens on forms
```

---

## 📈 Monitoring & Metrics

Track these to ensure system health:

```
OCR Metrics:
  - accuracy: % of text correctly extracted
  - confidence: Average OCR confidence score
  - fallbacks: # of EasyOCR used vs Tesseract

Solver Metrics:
  - success_rate: % of problems solved
  - avg_time: Time to solve
  - solver_choice: % SymPy vs AI

Learning Metrics:
  - hint_usage: Avg hints per problem
  - solve_rate: % of users solving
  - attempt_count: Avg attempts per problem

System Metrics:
  - upload_time: End-to-end time
  - memory_usage: Per request
  - error_rate: % of failed uploads
```

---

Generated: 2026-02-08
Purpose: Visual reference for scanner architecture
