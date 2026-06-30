import torch

from training.generate_data import (
    generate_gps_lost_samples,
    generate_comms_down_samples,
    generate_battery_critical_samples
)


def evaluate(model_path,generator):

    model=torch.jit.load(model_path)

    model.eval()

    X,y=generator(500)

    X=torch.tensor(X)

    y=torch.tensor(y)

    with torch.no_grad():

        predictions=model(X)

    binary=(predictions>0.5).float()

    accuracy=(binary==y).float().mean()

    print(f"{model_path}")

    print(f"Accuracy {accuracy.item()*100:.2f}%")

    print()


if __name__=="__main__":

    evaluate(
        "models/gps_lost.pt",
        generate_gps_lost_samples
    )

    evaluate(
        "models/comms_down.pt",
        generate_comms_down_samples
    )

    evaluate(
        "models/battery_critical.pt",
        generate_battery_critical_samples
    )