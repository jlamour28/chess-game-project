# ♟️ Advanced Chess Game - Pure JavaScript

A fully functional, professional chess game built entirely in JavaScript with no external dependencies. Features advanced AI, drag-and-drop gameplay, and responsive design that works on all devices.

## ✨ Features

- **🎮 Complete Chess Logic**: All rules implemented from scratch in pure JavaScript
- **🤖 Advanced AI Opponent**: Minimax algorithm with 3 difficulty levels (Easy/Medium/Hard)
- **🎯 Drag & Drop Interface**: Smooth, intuitive piece movement with visual feedback
- **📱 Mobile Responsive**: Touch support and adaptive design for all screen sizes
- **🎨 Professional UI**: Modern styling with animations and visual effects
- **⚡ Zero Installation**: Single HTML file - just open in any browser
- **🔄 Real-time Updates**: Live game status, move highlighting, and check detection
- **📝 Move History**: Complete game notation and move tracking
- **🎪 Game Modes**: Human vs Human and Human vs AI options

## 🚀 Quick Start

**Just open `advanced-chess.html` in any web browser and start playing!**

No installation, no dependencies, no setup required. The entire chess game runs in a single HTML file.

## 📁 Project Structure

```
Chess Game Project/
└── advanced-chess.html      # 🎯 Complete chess game (single file)
```

## 🎮 How to Play

### **Instant Setup:**
1. **Clone or download** the repository
   ```bash
   git clone https://github.com/JLamour28/Chess-game-project.git
   cd Chess-game-project
   ```

2. **Open `advanced-chess.html`** in any web browser (Chrome, Firefox, Safari, Edge)

3. **Start playing immediately!** 🎉

### **No Installation Required:**
- ✅ No Python installation needed
- ✅ No dependencies to install
- ✅ No setup or configuration
- ✅ Works on Windows, Mac, Linux
- ✅ Mobile and tablet friendly

## 🎯 Game Controls

### **Desktop:**
- **Drag & Drop**: Click and drag pieces to move them
- **Click to Move**: Click piece → click destination square
- **Game Modes**: Human vs Human or Human vs AI

### **Mobile:**
- **Touch Support**: Tap piece → tap destination square
- **Responsive Design**: Automatically adapts to screen size

## 🤖 AI Opponent

### **Difficulty Levels:**
- **🟢 Easy**: Fast responses, good for learning (depth: 2)
- **🟡 Medium**: Balanced challenge (depth: 3) - **Recommended**
- **🔴 Hard**: Deep analysis, strategic play (depth: 4)

### **AI Features:**
- **Smart Move Selection**: Uses minimax algorithm with position evaluation
- **Timeout Protection**: Won't hang on complex positions
- **Fallback System**: Random legal moves if AI fails

## 🛠️ Technical Details

### **Built With:**
- **Pure JavaScript**: No external libraries or frameworks
- **Chess Logic**: Complete rules implementation from scratch
- **AI Algorithm**: Minimax with alpha-beta pruning concepts
- **Responsive CSS**: Works on all device sizes

### **Key Components:**
- **ChessGame Class**: Game state and move validation
- **ChessUI Class**: Board rendering and user interaction
- **AI System**: Position evaluation and move selection

## 🐛 Endgame Stability

The game includes multiple safeguards for endgame scenarios:

### **Fixed Issues:**
- ✅ **Checkmate Detection**: Properly validates legal moves that escape check
- ✅ **Stalemate Detection**: Correctly identifies no-legal-move situations
- ✅ **AI Timeout Protection**: 3-second limit prevents hanging
- ✅ **Move Validation**: All moves checked for king safety
- ✅ **Undo Functionality**: Complete move history tracking

### **AI Safeguards:**
- **Depth Limiting**: Prevents infinite recursion
- **Fallback Moves**: Random legal moves if AI calculation fails
- **Position Evaluation**: Handles all endgame scenarios
- **Error Handling**: Graceful degradation on complex positions

## 🚀 Performance

### **Optimizations:**
- **Efficient AI**: Minimax algorithm with early termination
- **Fast Rendering**: Optimized DOM updates
- **Mobile Performance**: Touch-optimized for smooth interaction
- **Memory Management**: Proper event listener cleanup

## 📱 Browser Compatibility

**✅ Tested and working on:**
- Chrome/Chromium (Desktop & Mobile)
- Firefox (Desktop & Mobile)
- Safari (Desktop & iOS)
- Edge (Desktop & Mobile)

## 🔧 Customization

The game code is modular and easy to extend:

```javascript
// Example: Add new piece type
// Modify the piece creation and movement logic in ChessGame class

// Example: Adjust AI difficulty
// Modify the depth values in the depths object

// Example: Change visual theme
// Update CSS custom properties for colors and styling
```

## 📋 Game Rules Supported

- ✅ All standard chess moves (pawn, rook, bishop, knight, queen, king)
- ✅ Special moves (castling, en passant)
- ✅ Check and checkmate detection
- ✅ Stalemate and draw recognition
- ✅ Pawn promotion (auto-queen)
- ✅ Turn-based move validation

## 🎉 Ready to Play!

**Just open `advanced-chess.html` and enjoy a complete, professional chess experience with no setup required!**