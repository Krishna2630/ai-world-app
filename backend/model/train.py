import torch
import os
from model import WorldModel

model = WorldModel()

optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
loss_fn = torch.nn.MSELoss()

for _ in range(300):
    inputs = torch.randint(0, 1000, (32, 5))
    targets = torch.rand(32, 6)

    outputs = model(inputs)
    loss = loss_fn(outputs, targets)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

os.makedirs("backend/saved", exist_ok=True)
torch.save(model.state_dict(), "backend/saved/model.pth")

print("Model trained and saved!")