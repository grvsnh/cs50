# Terminal Games Suite

#### Video Demo:

_(To be added after recording the final video)_

#### Description:

Terminal Games Suite is a Python-based terminal application developed as the final project for CS50P. The project combines multiple classic games into a single interactive program using the `curses` library to provide a structured and visually clear text-based user interface. Rather than relying on simple input and print statements, the goal of this project was to create a responsive terminal application that feels complete, polished, and robust.

The application includes three games: **Tic Tac Toe**, **Rock Paper Scissors**, and a **Number Guessing Game**. All games are accessible through a centralized menu and are fully keyboard-driven. Special care was taken to ensure the interface remains centered, readable, and stable across different terminal sizes, while avoiding common `curses` runtime errors.

---

### Project Structure and Files

The project consists of the following files:

-   **`project.py`**  
    This file contains the main application logic, including the menu system, game logic, and terminal rendering code. The file is organized into clearly separated sections such as UI helpers, menus, individual games, and shared logic. Game logic (such as win detection and AI decision-making) is kept separate from rendering code wherever possible to improve clarity and testability.

-   **`test_project.py`**  
    This file contains automated tests written using `pytest`. Because `curses`-based interfaces cannot be easily tested automatically, the tests focus exclusively on pure logic functions, including Tic Tac Toe win detection, Tic Tac Toe AI behavior, and Rock Paper Scissors outcome logic. This ensures correctness without attempting to simulate terminal UI behavior.

-   **`requirements.txt`**  
    This file lists all external dependencies required to run and test the project, including `pytest` and its runtime dependencies, as well as `windows-curses` for Windows compatibility.

-   **`README.md`**  
    This file documents the project’s purpose, design decisions, and structure.

---

### Game Overview and Design Decisions

**Tic Tac Toe**  
Tic Tac Toe can be played either against another local player or against an AI opponent. The board is rendered using box-drawing characters to form a proper 3×3 grid. A visible cursor highlights the selected cell, ensuring usability even when cells are empty. The AI uses a simple strategy: it attempts to win, blocks the player when necessary, and otherwise selects a random valid move. This balances challenge and fairness.

**Rock Paper Scissors**  
Rock Paper Scissors is menu-driven and uses arrow keys for selection. A short “thinking” animation is displayed before the computer reveals its choice, improving the overall user experience.

**Number Guessing Game**  
The Number Guessing Game challenges the player to guess a randomly selected number between 1 and 100, providing immediate feedback and tracking attempts.

---

### Technical Notes and Disclaimer

All screen drawing is performed using bounds-safe helper functions to prevent crashes caused by small terminal sizes. The project is compatible with Linux and macOS by default and supports Windows through the `windows-curses` package.

**Disclaimer:** Some comments within the source code were generated with the assistance of AI tools and may contain minor inaccuracies. The program logic, structure, and behavior were implemented, tested, and verified by the author.

---

### Conclusion

Terminal Games Suite demonstrates structured Python programming, terminal UI development, basic AI logic, and automated testing. The project emphasizes stability, clarity, and user experience, making it a complete and well-documented final project for CS50P.
