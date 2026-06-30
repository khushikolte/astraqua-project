import torch
import torch.nn as nn
import torch.optim as optim

from models.scenario_model import ScenarioModel

from training.generate_data import (
    generate_gps_lost_samples,
    generate_comms_down_samples,
    generate_battery_critical_samples
)


DEVICE="cpu"


def train_model(generator,name):

    X,y = generator()

    X=torch.tensor(X)
    y=torch.tensor(y)

    model=ScenarioModel()

    criterion=nn.BCELoss()

    optimizer=optim.Adam(
        model.parameters(),
        lr=1e-3
    )

    for epoch in range(50):

        optimizer.zero_grad()

        outputs=model(X)

        loss=criterion(outputs,y)

        loss.backward()

        optimizer.step()

        if epoch%10==0:

            print(f"{name} Epoch {epoch+1} Loss {loss.item():.4f}")

    scripted=torch.jit.script(model)

    scripted.save(f"models/{name}.pt")

    print(f"\nSaved models/{name}.pt\n")


if __name__=="__main__":

    train_model(generate_gps_lost_samples,"gps_lost")

    train_model(generate_comms_down_samples,"comms_down")

    train_model(generate_battery_critical_samples,"battery_critical")