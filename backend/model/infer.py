import torch
from backend.model.model import WorldModel
from backend.utils.tokenizer import tokenize

model = WorldModel()
model.load_state_dict(torch.load("backend/saved/model.pth"))
model.eval()

def predict(prompt):
    tokens = tokenize(prompt)

    # pad / trim
    if len(tokens) < 5:
        tokens += [0] * (5 - len(tokens))
    else:
        tokens = tokens[:5]

    x = torch.tensor(tokens).unsqueeze(0)

    with torch.no_grad():
        out = model(x).squeeze().numpy()

    return {
        "tree_density": float(out[0]),
        "rock_density": float(out[1]),
        "house_density": float(out[2]),
        "river_count": int(abs(out[3]) * 3),
        "height_scale": float(out[4]),
        "roughness": float(out[5])
    }