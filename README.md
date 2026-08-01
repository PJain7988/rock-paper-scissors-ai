# RPS Predictive Model

![Python](https://img.shields.io/badge/python-3.x-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

> A predictive machine learning model for Rock, Paper, Scissors that utilizes pattern recognition to adapt to adversarial strategies.

This repository contains a Python-based intelligent agent designed to play Rock, Paper, Scissors. Rather than relying on purely random moves, the AI analyzes the opponent's historical behavior to identify patterns and predict future moves, demonstrating core concepts in machine learning and sequential decision-making.

## 🚀 Features

- **Predictive AI Agent:** Employs historical data analysis to counter opponent strategies.
- **Automated Testing Environment:** Includes a robust test module to evaluate the AI's win rate against various baseline bots (e.g., random, statistical, pattern-based).
- **Modular Architecture:** Clean separation of concerns between game logic, AI models, and testing frameworks.

## 📁 Project Structure

```text
├── main.py            # Entry point for the application
├── RPS.py             # Core predictive model and AI logic
├── RPS_game.py        # Game mechanics and environment setup
└── test_module.py     # Automated tests and performance evaluation
```

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/rps-predictive-model.git
   cd rps-predictive-model
   ```

2. **Run the application:**
   No external dependencies are required. You can run the project directly using Python 3:
   ```bash
   python main.py
   ```

## 🎯 Usage

To evaluate the model's performance against the testing suite, run the test module:

```bash
python test_module.py
```

This will output the AI's win/loss/tie ratio against various standardized opponents, demonstrating its ability to adapt and overcome different play styles.

## 🧠 How it Works

The AI tracks the sequence of previous moves played by the opponent. By analyzing the frequency of specific move sequences (n-grams), the model calculates the probability of the opponent's next move. It then selects the move that theoretically guarantees a win against the highest-probability prediction.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
