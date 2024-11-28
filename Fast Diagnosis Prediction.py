# Example dataset
diagnosis_data = {
    "Fever": {
        "Cough": {
            "Shortness of Breath": "Pneumonia",
            "No Shortness of Breath": "Flu"
        },
        "No Cough": "Heat Exhaustion"
    },
    "No Fever": {
        "Headache": "Migraine",
        "No Headache": "Allergy"
    }
}

def diagnose(symptoms, decision_tree):
    if isinstance(decision_tree, str):
        return decision_tree  # Base case: Diagnosis is a string.
    
    for key, subtree in decision_tree.items():
        if key in symptoms:
            return diagnose(symptoms, subtree)
    return "Unknown Condition"

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QCheckBox, QPushButton, QLabel, QWidget

class DiagnosisApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fast Diagnosis Prediction")
        self.setGeometry(200, 200, 400, 300)
        
        # Symptoms checklist
        self.symptoms_checklist = [
            "Fever", "Cough", "Shortness of Breath", "Headache"
        ]
        self.checkboxes = []
        
        self.initUI()
    
    def initUI(self):
        central_widget = QWidget()
        layout = QVBoxLayout()
        
        # Add checkboxes
        for symptom in self.symptoms_checklist:
            checkbox = QCheckBox(symptom)
            self.checkboxes.append(checkbox)
            layout.addWidget(checkbox)
        
        # Diagnose button
        diagnose_button = QPushButton("Diagnose")
        diagnose_button.clicked.connect(self.get_diagnosis)
        layout.addWidget(diagnose_button)
        
        # Diagnosis label
        self.result_label = QLabel("Diagnosis will appear here.")
        layout.addWidget(self.result_label)
        
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
    
    def get_diagnosis(self):
        selected_symptoms = [
            checkbox.text() for checkbox in self.checkboxes if checkbox.isChecked()
        ]
        
        # Call the diagnosis function
        diagnosis = diagnose(selected_symptoms, diagnosis_data)
        self.result_label.setText(f"Diagnosis: {diagnosis}")

# Run the app
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DiagnosisApp()
    window.show()
    sys.exit(app.exec_())


# unchecked buttons not working