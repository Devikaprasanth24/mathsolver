
import re

def format_tokens(t_list):
    return ''.join([f"{t:g}" if isinstance(t, float) else str(t) for t in t_list])

def solve_complex_arithmetic(problem_text):
    try:
        print(f"DEBUG: problem_text='{problem_text}'")
        clean_text = re.sub(r'^(calculate|solve|evaluate|find)\s+', '', problem_text, flags=re.IGNORECASE).strip()
        print(f"DEBUG: clean_text='{clean_text}'")
        
        # Allow digits, +, -, *, /, (, ), ., =, and spaces
        if not re.match(r'^[\d\+\-\*\/\(\)\.\=\s]+$', clean_text):
            print("DEBUG: Regex match failed!")
            offenders = re.sub(r'[\d\+\-\*\/\(\)\.\=\s]', '', clean_text)
            print(f"DEBUG: Offenders: '{offenders}'")
            return None
        
        text = clean_text.replace(' ', '').replace('=', '')
        print(f"DEBUG: processing text='{text}'")

        if not any(op in text for op in ['+', '-', '*', '/']):
            print("DEBUG: No operators found!")
            return None

        tokens = []
        i = 0
        while i < len(text):
            char = text[i]
            if char in '+-*/()':
                tokens.append(char)
                i += 1
            elif char.isdigit() or char == '.':
                j = i
                while j < len(text) and (text[j].isdigit() or text[j] == '.'):
                    j += 1
                try:
                    tokens.append(float(text[i:j]))
                except:
                    print(f"DEBUG: Failed to parse float '{text[i:j]}'")
                    return None
                i = j
            else:
                print(f"DEBUG: Unexpected char '{char}'")
                i += 1
        
        print(f"DEBUG: tokens={tokens}")
        
        steps = []
        current_tokens = tokens.copy()
        step_count = 1
        
        # Pass 1: Multiplication and Division
        print("DEBUG: Starting Pass 1 (M/D)")
        while '*' in current_tokens or '/' in current_tokens:
            idx = -1
            op = ''
            for k, t in enumerate(current_tokens):
                if t in ('*', '/'):
                    idx = k
                    op = t
                    break
            if idx > 0 and idx < len(current_tokens) - 1:
                n1 = current_tokens[idx-1]
                n2 = current_tokens[idx+1]
                res = n1 * n2 if op == '*' else n1 / n2
                old_segment = f"{format_tokens([n1])}{op}{format_tokens([n2])}"
                new_tokens = current_tokens[:idx-1] + [res] + current_tokens[idx+2:]
                current_tokens = new_tokens
                print(f"DEBUG: Step {step_count}: {old_segment}={res}")
                step_count += 1
            else:
                print(f"DEBUG: Pass 1 break, malformed at idx {idx}")
                break
        
        # Pass 2: Addition and Subtraction
        print("DEBUG: Starting Pass 2 (A/S)")
        while '+' in current_tokens or '-' in current_tokens:
            idx = -1
            op = ''
            for k, t in enumerate(current_tokens):
                if t in ('+', '-'):
                    idx = k
                    op = t
                    break
            if idx > 0 and idx < len(current_tokens) - 1:
                n1 = current_tokens[idx-1]
                n2 = current_tokens[idx+1]
                res = n1 + n2 if op == '+' else n1 - n2
                old_segment = f"{format_tokens([n1])}{op}{format_tokens([n2])}"
                new_tokens = current_tokens[:idx-1] + [res] + current_tokens[idx+2:]
                current_tokens = new_tokens
                print(f"DEBUG: Step {step_count}: {old_segment}={res}")
                step_count += 1
            else:
                print(f"DEBUG: Pass 2 break, malformed at idx {idx}")
                break
        
        print(f"DEBUG: Final Answer: {current_tokens}")
        return True
    except Exception as e:
        print(f"DEBUG: Exception: {e}")
        return None

if __name__ == "__main__":
    solve_complex_arithmetic("1+2-3+5-2=")
    solve_complex_arithmetic("25% of 200")
