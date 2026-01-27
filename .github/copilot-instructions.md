# Copilot Instructions for ECE AI Finance Project

## Project Overview

This is an educational repository for the 2026 ECE Ing4 Finance & Symbolic AI course. It hosts 14 distinct group projects exploring AI approaches (symbolic, constraint programming, metaheuristics, machine learning) applied to real-world problems in healthcare, optimization, and bioinformatics.

**Key dates:**
- Checkpoint: 20 January 2026
- Final presentation: 2 February 2026
- PR deadline: 31 January 2026

## Repository Structure

Each group **must** work exclusively within its own subdirectory:

```
/groupe-XX-nom-sujet/
├── README.md                # Project documentation (installation, tests, usage)
├── src/                     # Source code
├── docs/                    # Technical documentation
├── slides/                  # Presentation slides (PDF or link)
└── [language-specific dirs] # Requirements, notebooks, data, etc.
```

**Important:** No code at the repository root. All work is isolated within `groupe-XX-*` subdirectories.

## Project Domains & Technology Choices

Projects fall into these AI paradigms - match technologies accordingly:

| Domain | Approach | Example Tech |
|--------|----------|--------------|
| **Scheduling/Rostering** | Constraint Programming (CSP) | OR-Tools CP-SAT, MiniZinc, IBM CP Optimizer |
| **Epidemiological Modeling** | Genetic Algorithms, Simulation | DEAP/PyGAD, NumPy/SciPy, Plotly |
| **Kidney Exchange** | Graph Optimization, MILP | NetworkX, Gurobi/PuLP, OR-Tools |
| **Molecular Identification** | Cheminformatics, ML | RDKit, BioPython, scikit-learn |
| **Job-Shop Scheduling** | CSP with Interval Variables | OR-Tools CP-SAT, iZinc |
| **Hospital Optimization** | Metaheuristics | OR-Tools, custom SA/TS implementations |
| **University Timetabling** | CSP with Logic Programming | MiniZinc, Choco, OR-Tools CP-SAT |
| **Medical Expert Systems** | Logic Programming, Inference | Prolog, PyKE, CLIPS |
| **Wordle Solver** | CSP + LLM Integration | OR-Tools, OpenAI function calling |
| **Synthetic Biology** | SMT Solvers | Z3, BioModelAnalyzer |
| **Minesweeper** | CSP with Sum Constraints | OR-Tools CP-SAT, python-constraint |
| **Medical Ontologies** | Semantic Web | RDFLib, Protégé, SPARQL |
| **Stable Marriage** | Graph Matching Algorithms | NetworkX, Gale-Shapley, OR-Tools CSP |
| **Blockchain Health** | Distributed Systems | Hyperledger Fabric, web3.py |

## Developer Workflows

### Initial Setup (per group)
1. **Fork** the main repository (you have no write access)
2. **Create subdirectory** `groupe-XX-nom-sujet/` with all code inside
3. **Set up environment:**
   - Create `requirements.txt` (Python), `package.json` (Node), or equivalent
   - Document environment setup in README.md
4. **Create development branch** from `main` for collaborative work

### Testing & Validation
- **Each project should include:**
  - Unit tests demonstrating the solver/algorithm works
  - A sample input/dataset in `data/` or `examples/`
  - A test command documented in README: `python -m pytest` or `npm test`
- **No generic tests** - tests must validate domain-specific constraints (e.g., nurse roster meets all shift requirements)

### Pull Request Process
- **Minimum 2 days before presentation** (by 31 January)
- PR must include: working code, complete README, and technical docs
- All members identified with GitHub usernames

## Code Patterns & Conventions

### Constraint Satisfaction Problems (CSP)
When using OR-Tools CP-SAT or similar solvers:
```python
from ortools.sat.python import cp_model

model = cp_model.CpModel()
# Define variables with domain() or IntVar()
# Add constraints via model.Add()
solver = cp_model.CpSolver()
status = solver.Solve(model)
```
- **Convention:** Separate variable definition, constraint building, and solving phases
- **Validation:** Always verify solutions satisfy constraints; print constraint violations
- See: Projects 1 (Nurse Rostering), 5 (Job-Shop), 7 (Timetabling), 11 (Minesweeper)

### Graph-Based Problems
When modeling as graphs (Kidney Exchange, Stable Marriage):
```python
import networkx as nx
# Build directed/undirected graph with attributes
# Use algorithms: maximum_matching(), find_cycle(), shortest_path()
# Visualize with nx.draw() or Graphviz
```
- **Convention:** Represent nodes as problem entities, edges as compatibility/preference
- See: Projects 3 (Kidney Exchange), 13 (Stable Marriage)

### Machine Learning / Evolutionary Algorithms
When optimizing parameters (Epidemiological Modeling):
```python
from deap import base, creator, tools, algorithms
# Define fitness, individual, population
# Run eaSimple() or custom loop
# Track convergence with statistics
```
- **Convention:** Log fitness across generations; visualize with Matplotlib
- See: Project 2 (COVID modeling with Genetic Algorithms)

### Logic & Rule-Based Systems
For expert systems / symbolic reasoning:
- **Prolog:** Use SWI-Prolog with Python subprocess or PyProlog
- **Python:** PyKE for rule engines, SymPy for symbolic math
- **Convention:** Separate knowledge base (rules/facts) from inference engine
- See: Project 8 (Medical Expert Systems), Project 12 (Ontologies)

### Data Handling
- Use **Pandas** for tabular data (shift rosters, patient records, etc.)
- Use **NumPy/SciPy** for numerical simulation (epidemiology, molecular dynamics)
- Always include sample datasets in `data/` directory (CSV, JSON, or synthetic)

## Key Files & Exemplars

Refer to the main README.md for detailed problem descriptions, references, and suggested approaches for each of the 14 projects. It contains:
- Problem context and NP-complexity notes
- Academic references with DOIs
- Technology recommendations
- Constraint/algorithm sketches

When implementing, **read the full problem description** in README.md before starting code.

## Testing & Documentation Standards

**README per subdirectory must include:**
1. **Problem statement** (1-2 paragraphs)
2. **Installation:** `pip install -r requirements.txt` or equivalent
3. **Running the code:** How to execute the main script/solver
4. **Tests:** How to run tests and what they validate
5. **Example output:** Show a sample result (solution, visualization, metrics)
6. **Technologies used** (libraries, versions, solver configs)

**Example test validation (Nurse Rostering):**
```bash
# Must verify: each nurse works ≤ 40 hours/week, all shifts covered, no back-to-back night shifts
python test_roster.py
```

## Common Pitfalls

- **Forgetting group subdirectory:** Code at repository root will be rejected
- **No test data:** Solver works perfectly in theory but no sample to validate
- **Hardcoded parameters:** Make instance/parameter files; don't embed in code
- **Solver without logging:** Always print objective value, status, solution summary
- **Incomplete README:** Installation must work from scratch; include Python version, dependencies
- **LLM-integrated projects:** Clarify API dependencies (OpenAI, local model); handle rate limits gracefully

## Git Workflow for Collaborative Development

```bash
# In your forked repo
git checkout -b groupe-01-feature
# ... make changes in groupe-01-*/ only
git add groupe-01-*/
git commit -m "Implement CSP model for nurse rostering"
git push origin groupe-01-feature
# Create PR to main branch of original repo
```

**Branch naming:** `groupe-XX-feature-name` (e.g., `groupe-03-kidney-graph-search`)

## Integration Checkpoints

- **20 January:** Checkpoint review - core algorithm/solver implemented and tested
- **31 January:** PR open - full code + docs + tests running
- **2 February:** Final presentation - slides + live demo

Code quality criteria for evaluation:
- Algorithm correctness (respects all constraints, finds valid solutions)
- Performance (completes within reasonable time for test instances)
- Documentation (README + inline comments explain choices)
- Collaboration (meaningful Git history, all members contributing)

---

**Repository owner:** alexistbECE  
**Course:** ECE Ing4 Finance & Symbolic/Exploratory AI  
**Updated:** January 2026
