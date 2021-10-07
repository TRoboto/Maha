from tqdm import tqdm

from maha.datasets import load_dataset
from maha.rexy import Expression, capture_group

names = load_dataset("names")[:20]
cleaned_names = []
for name in tqdm(names, desc="Loading names"):
    if name.cleaned_name not in cleaned_names:
        cleaned_names.append(name.cleaned_name)

print("Number of total cleaned names:", len(cleaned_names))
print(cleaned_names)

# cache the cleaned names
exp = Expression(capture_group(*cleaned_names), pickle=True)
exp.compile()
print(exp)
