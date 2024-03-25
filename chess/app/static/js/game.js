$(document).ready(function() {
    function createChessBoard() {
        const board = document.getElementById('chessboard');
        // Убедитесь, что board не null
        if (!board) {
            console.error('Chessboard element not found');
            return;
        }
        for (let i = 0; i < 64; i++) {
            const square = document.createElement('div');
            const isBlack = (Math.floor(i / 8) + i) % 2 === 0;
            square.className = isBlack ? 'black' : 'white';

            // Вычисляем координаты
            const x = 'abcdefgh'[i % 8];
            const y = 8 - Math.floor(i / 8);
            square.setAttribute('data-coord', `${x}${y}`);

            board.appendChild(square);
        }

        // Функция для добавления фигуры на доску
        function addPiece(piece, position) {
            const pieceElement = document.createElement('img');
            pieceElement.src = '/static/figures/' + piece + '.png';
            pieceElement.className = 'chesspiece';
            pieceElement.draggable = true;

            // Вычисляем координаты
            const x = 'abcdefgh'[position % 8];
            const y = 8 - Math.floor(position / 8);
            const coord = `${x}${y}`;

            // Устанавливаем id фигуры на основе её позиции
            const pieceId = `${piece}-${coord}`;
            pieceElement.id = pieceId;

            // Устанавливаем атрибут data-coord для фигуры
            pieceElement.setAttribute('data-coord', coord);


            board.children[position].appendChild(pieceElement);
        }


        const pieces = ['pawn_white', 'pawn_black', 'rook_white', 'knight_white', 'bishop_white', 'queen_white', 'king_white', 'bishop_white', 'knight_white', 'rook_white', 'rook_black', 'knight_black', 'bishop_black', 'queen_black', 'king_black', 'bishop_black', 'knight_black', 'rook_black'];

        // Расстановка фигур на доске
        // Белые пешки
        for (let i = 8; i < 16; i++) {
            addPiece('pawn_white', i);
        }
        // Черные пешки
        for (let i = 48; i < 56; i++) {
            addPiece('pawn_black', i);
        }
        // Остальные фигуры
        addPiece('rook_white', 0);
        addPiece('knight_white', 1);
        addPiece('bishop_white', 2);
        addPiece('queen_white', 3);
        addPiece('king_white', 4);
        addPiece('bishop_white', 5);
        addPiece('knight_white', 6);
        addPiece('rook_white', 7);
        addPiece('rook_black', 56);
        addPiece('knight_black', 57);
        addPiece('bishop_black', 58);
        addPiece('queen_black', 59);
        addPiece('king_black', 60);
        addPiece('bishop_black', 61);
        addPiece('knight_black', 62);
        addPiece('rook_black', 63);

        let draggedElement = null;
        document.querySelectorAll('.chesspiece').forEach(piece => {
            piece.addEventListener('dragstart', (e) => {
                draggedElement = e.target;
                e.target.style.opacity = '0.1'; // Делаем фигуру полупрозрачной при перетаскивани
                e.dataTransfer.setDragImage(e.target, 75 / 2, 75 / 2);
                // Подсветка возможных ходов или клеток может быть добавлена здесь

            });

            piece.addEventListener('dragend', (e) => {
                e.target.style.opacity = ''; // Возвращаем нормальную прозрачность фигуре
                // Убираем подсветку клеток
                // здесь должна быть запись ходов


            });
        });

        document.querySelectorAll('#chessboard div').forEach(square => {
            square.addEventListener('dragover', (e) => {
                e.preventDefault(); // Необходимо для возможности drop
                // Подсветка клетки, если нужно
            });

            square.addEventListener('drop', (e) => {
                e.preventDefault();
                const targetSquare = e.target.closest('.black, .white'); // Находим клетку

                if (draggedElement && targetSquare) {
                    // Определяем координаты from и to
                    const fromCoord = draggedElement.parentElement.getAttribute('data-coord');
                    const toCoord = targetSquare.getAttribute('data-coord');

                    // Здесь AJAX запрос на сервер
                    fetch('http://127.0.0.1:8000/make_move', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': getCookie('csrftoken') // Получаем CSRF токен
                        },
                        body: JSON.stringify({from: fromCoord, to: toCoord})
                    })
                        .then(response => response.json())
                        .then(data => {
                            if (data.move_made) {
                                 console.log(data.message)
                                // Если ход возможен, перемещаем фигуру
                                while (targetSquare.firstChild) {
                                    targetSquare.removeChild(targetSquare.firstChild); // Съединение фигуры
                                }
                                targetSquare.appendChild(draggedElement);
                            } else {
                                console.log(data.message)
                            }
                        })
                        .catch(error => {
                            console.error('Error:', error);
                        })
                        .finally(() => {
                            draggedElement.style.opacity = ''; // Возвращаем нормальную прозрачность
                            draggedElement = null; // Сбрасываем ссылку на перетаскиваемый элемент
                        });
                }
            });
        });

        // Функция для получения значения CSRF токена
        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
    }


    createChessBoard();
});