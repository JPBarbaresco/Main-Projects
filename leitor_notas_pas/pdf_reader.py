import re
import tkinter as tk
import json
from tkinter import ttk, messagebox
from pdfminer.high_level import extract_text
from tabulate import tabulate


def sort(list):
    if len(list) == 1 or len(list) == 0:
        return list
    pivot = list[0]
    less_than = []
    more_than = []
    for item in list:
        if item != pivot:
            if item[1]+item[2] <= pivot[1]+pivot[2]:
                less_than.append(item)
            elif item[1]+item[2] > pivot[1]+pivot[2]:
                more_than.append(item)
    
    less_than = sort(less_than)
    more_than = sort(more_than)

    return less_than + [pivot] + more_than

def busca(search : list) -> str:
    error_message = "input invalido"
    if search[-1].lower() == 'nome':
        ## alerta de vibe code (reza p q funcione) ##
        # Build a frequency count of candidate matches for each search token
        possible_counts = {}
        for name in search[:-1]:
            token = name.lower()
            for candidate in test_grades:
                if token in candidate[0].lower().split():
                    possible_counts[candidate] = possible_counts.get(candidate, 0) + 1

        # Print candidates that matched at least half of the tokens
        threshold = max(1, len(search[:-1]))
        resoults = []
        for candidate, count in possible_counts.items():
            if count >= threshold:
                resoults.append(list(candidate) + [position_map[candidate]])
        
        ## alerta finalizado (estamos a salvo (por enquanto...)) ##

    elif search[-1].lower() == 'score' or search[-1].lower() == 'redacao':
        try:
            resoults = []
            for candidate in test_grades:
                if float(search[0]) <= (candidate[1] if search[-1].lower() == 'score' else candidate[2]) <= float(search[0])+(10 if search[-1].lower() == 'score' else 1):
                    resoults.append(list(candidate) + [position_map[candidate]])
            
        except:
            return error_message

    elif search[-1].lower() == 'final':
        try:
            resoults = []
            for candidate in test_grades:
                if float(search[0]) <= (candidate[1] + candidate[2]) <= float(search[0])+10:
                    resoults.append(list(candidate) + [position_map[candidate]])
            
        except:
            return error_message
    
    elif search[-1].lower() == 'posicao':
        try:
            maximun = max([int(search[0]), int(search[1])])
            minimum = min([int(search[0]), int(search[1])])
            resoults = []
            if len(search) >= 3:
                for i in range(-maximun, (-minimum)+1):
                    resoults.append(list(test_grades[i]) + [-i])
            else:
                resoults.append(list(test_grades[-int(search[0])]) + [int(search[0])])
            
        except:
            return error_message
    
    else:
        return error_message

    return "Numero de resultados: " + str(len(resoults)) + '\n\n' + tabulate(resoults, ["nome", "EB", "redacao", "posicao geral"], "presto")


# So rodar isso na primeira vez
print("extracting text...")

text = extract_text(r"C:\Users\joaop\.vscode\dot.py_files\leitor_notas_pas\notas_pas1_2025.pdf")

data = {'text': text}
with open('text.json', 'w') as f:
    json.dump(data, f)

print("\nextracted text")
# So rodar isso na primeira vez

with open("text.json", 'r') as f:
    loaded_text = json.load(f)

rule = re.compile(r"(\d+),\s+([A-Za-z\s]+),\s+([\d.]+),\s+([\d.]+),\s+([\d.]+),\s+([\d.]+),\s+([\d.]+)")
print("\nprocessing text...")
candidates = rule.findall(text)
print("\nprocessed text")

test_grades : list = []

print("\nprocessing info...")

for candidate in candidates:
    # print(candidate)
    names = candidate[1].split()
    name = " ".join(names)
    test_score = float(candidate[4])
    try:
        eassay_score = float(candidate[6])
    except:
        eassay_score = float(candidate[6][:-1])

    test_grades.append((name, test_score, eassay_score))

print("\nsorting by grades...")
test_grades = sort(test_grades)
print("\nsorted by grades")

position_map = {candidate: len(test_grades)-i for i, candidate in enumerate(test_grades)}

print("escaping the matrix...")
for i in range(-len(test_grades), 0):
    # print(test_grades[i], -i)
    pass


################################################################### ALERTA DE VIBE CODE ##############################################################

# Calculate statistics
media = sum(i[1] for i in test_grades) / len(test_grades)
media_redacao = sum(i[2] for i in test_grades) / len(test_grades)

# Create GUI
root = tk.Tk()
root.title("Leitor de Notas - PAS")
root.geometry("1000x750")

# Statistics Frame
stats_frame = ttk.LabelFrame(root, text="Estatísticas", padding=10)
stats_frame.pack(fill="x", padx=10, pady=5)

ttk.Label(stats_frame, text=f"Média Geral: {media:.2f}", font=("Arial", 15)).pack(side="left", padx=20)
ttk.Label(stats_frame, text=f"Média Redação: {media_redacao:.2f}", font=("Arial", 15)).pack(side="left", padx=20)
ttk.Label(stats_frame, text=f"Total de Candidatos: {len(test_grades)}", font=("Arial", 15)).pack(side="left", padx=20)

# Search Frame
search_frame = ttk.LabelFrame(root, text="Buscar", padding=10)
search_frame.pack(fill="x", padx=10, pady=5)

ttk.Label(search_frame, text="Tipo:", font=("Arial", 12)).pack(side="left", padx=5)
search_type = ttk.Combobox(search_frame, values=["nome", "score", "redacao", "final", "posicao"], font=("Arial", 12), width=15, state="readonly")
search_type.pack(side="left", padx=5)
search_type.set("nome")

ttk.Label(search_frame, text="Busca:", font=("Arial", 12)).pack(side="left", padx=5)
search_entry = ttk.Entry(search_frame, width=30)
search_entry.pack(side="left", padx=5)

def perform_search():
    search_term = search_entry.get().strip()
    search_cat = search_type.get()
    
    if not search_term:
        messagebox.showwarning("Aviso", "Digite um termo de busca")
        return
    
    search_input = search_term.split() + [search_cat]
    result = busca(search_input)
    
    results_text.config(state="normal")
    results_text.delete("1.0", "end")
    results_text.insert("1.0", result)
    results_text.config(state="disabled")

def copy_to_clipboard():
    """Copy the current search results to clipboard"""
    results = results_text.get("1.0", "end-1c")
    if results.strip():
        root.clipboard_append(results)
        messagebox.showinfo("Sucesso", "Resultados copiados para a área de transferência!")
    else:
        messagebox.showwarning("Aviso", "Não há resultados para copiar")

search_btn = ttk.Button(search_frame, text="Buscar", command=perform_search)
search_btn.pack(side="left", padx=5)

copy_btn = ttk.Button(search_frame, text="Copiar", command=copy_to_clipboard)
copy_btn.pack(side="left", padx=5)

# Results Frame
results_frame = ttk.LabelFrame(root, text="Resultados", padding=10)
results_frame.pack(fill="both", expand=True, padx=10, pady=5)

results_text = tk.Text(results_frame, font=("Courier", 20), state="disabled", height=20)
results_text.pack(fill="both", expand=True)

root.mainloop()

################################################################### ALERTA DE VIBE CODE ##############################################################
