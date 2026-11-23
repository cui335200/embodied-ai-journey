import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import torchvision
import torchvision.transforms as transforms
device ="cuda" if torch.cuda.is_available() else "cpu"
print("device:",device)
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,0.5,0.5),(0.5,0.5,0.5))  
])
train_set = torchvision.datasets.CIFAR10("./data", train=True, download=True, transform=transform)
test_set = torchvision.datasets.CIFAR10("./data", train=False, download=True, transform=transform)

train_loader = DataLoader(train_set, batch_size=128, shuffle=True, num_workers=2)
test_loader = DataLoader(test_set, batch_size=256, shuffle=False, num_workers=2)

class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3,32,3,padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(32,64,3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(64,128,3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(128*4*4,256), nn.ReLU(),
            nn.Linear(256,10),
        )
    def forward(self, x):
        return self.classifier(self.features(x))
    
model = Net().to(device)
loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3) 
for epach in range(20):
    model.train()
    total,correct,running_loss = 0, 0, 0.0
    for imgs, labels in train_loader:
        imgs, labels = imgs.to(device), labels. to(device)

        logits = model(imgs)
        loss = loss_fn(logits, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        running_loss += loss.item() * imgs.size(0)
        correct += (logits.argmax(1) == labels).sum().item()
        total += imgs.size(0)

    print(f"epoch {epach+1:02d} loss={running_loss/total:.4f} acc={correct/total:.4f}")
model.eval()
total, correct = 0, 0
with torch.no_grad():
    for imgs, labels in test_loader:
        imgs, labels = imgs.to(device), labels.to(device)
        logits = model(imgs)
        correct += (logits.argmax(1) == labels).sum().item()
        total += imgs.size(0)
print(f"test accuracy={correct/total:.4f}")
torch.save(model.state_dict(), "cifar10_cnn.pt")