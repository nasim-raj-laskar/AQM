import os
from pathlib import Path

# Define project structure relative to current directory
PROJECT_STRUCTURE = {
    "edge": [
        "main.py",
        "config.json"
    ],
    "backend/app/routes": [
        "__init__.py",
        "sensor_routes.py"
    ],
    "backend/app/services": [
        "model_service.py",
        "llm_service.py",
        "metrics_service.py"
    ],
    "backend/app/utils": [
        "data_validator.py",
        "logger.py"
    ],
    "backend/app/database": [
        "__init__.py",
        "db_connection.py",
        "crud.py"
    ],
    "backend/app/models": [
        "model.pkl",
        "model_trainer.py"
    ],
    "backend": [
        "requirements.txt",
        "Dockerfile"
    ],
    "backend/app": [
        "__init__.py",
        "main.py",
        "config.py"
    ],
    "dashboard": [
        "main_dashboard.py"
    ],
    "dashboard/components": [
        "charts.py",
        "metrics_card.py",
        "llm_section.py"
    ],
    "dashboard/utils": [
        "api_client.py",
        "theme.py"
    ],
    "monitoring/grafana": [
        "grafana_setup.yaml",
        "prometheus.yml"
    ],
    "monitoring/exporters": [
        "backend_metrics_exporter.py",
        "system_metrics_exporter.py"
    ],
    "tests": [
        "test_model_service.py",
        "test_routes.py",
        "test_data_validator.py"
    ],
    "scripts": [
        "generate_synthetic_data.py",
        "train_model.py"
    ]
}

# Root-level files (already at project root)
ROOT_FILES = [
    ".env",
    ".gitignore",
    "README.md",
    "requirements.txt"
]

def create_structure():
    """Creates the internal project structure from current directory."""
    base_path = Path(".").resolve()
    print(f" Creating folders inside: {base_path}")

    for folder, files in PROJECT_STRUCTURE.items():
        folder_path = base_path / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        for file in files:
            file_path = folder_path / file
            if not file_path.exists():
                file_path.touch()
                print(f"Created file: {file_path.relative_to(base_path)}")

    # Create root-level files
    for file in ROOT_FILES:
        file_path = base_path / file
        if not file_path.exists():
            file_path.touch()
            print(f" Created root file: {file}")

    print("\nStructure creation complete!")

if __name__ == "__main__":
    create_structure()
