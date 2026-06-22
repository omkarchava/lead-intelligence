import subprocess

subprocess.run(
    [
        "python",
        "training/build_dataset.py"
    ]
)

subprocess.run(
    [
        "python",
        "training/train_assignment.py"
    ]
)

subprocess.run(
    [
        "python",
        "training/train_conversion_time.py"
    ]
)